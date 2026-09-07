"""Embedding recall for requirement signal candidates.

This module builds a lightweight local JSON cache for embeddings and retrieves
the most semantically similar requirement rows for a query.
"""

import hashlib
import json
import math
import time
import urllib.error
import urllib.request
from pathlib import Path


def normalize(value):
    return "" if value is None else str(value).replace("\u3000", " ").strip()


def embedding_text(signal):
    parts = [
        normalize(getattr(signal, "chinese_name", "")),
        normalize(getattr(signal, "signal_name", "")),
    ]
    return "\n".join(part for part in parts if part)


INDEX_SCHEMA = "name-signal-v3"


def cache_key(model, text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{INDEX_SCHEMA}:{model}:{digest}"


def load_cache(path):
    path = Path(path)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_cache(path, cache):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def request_embeddings(texts, model, base_url, api_key, timeout, dimensions):
    body = json.dumps(
        {"model": model, "input": texts, "dimensions": dimensions},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/embeddings",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Embedding request failed: HTTP {exc.code} {exc.reason}: {detail}") from exc
    data = sorted(payload["data"], key=lambda item: item["index"])
    return [item["embedding"] for item in data]


def get_embeddings(texts, model, base_url, api_key, timeout, cache_path, batch_size=10, dimensions=1024):
    cache = load_cache(cache_path)
    embeddings = [None] * len(texts)
    missing = []
    missing_indexes = []

    for index, text in enumerate(texts):
        key = cache_key(model, text)
        if key in cache:
            embeddings[index] = cache[key]
        else:
            missing.append(text)
            missing_indexes.append(index)

    for start in range(0, len(missing), batch_size):
        batch = missing[start : start + batch_size]
        batch_indexes = missing_indexes[start : start + batch_size]
        batch_embeddings = request_embeddings(batch, model, base_url, api_key, timeout, dimensions)
        for text, index, embedding in zip(batch, batch_indexes, batch_embeddings):
            cache[cache_key(model, text)] = embedding
            embeddings[index] = embedding
        save_cache(cache_path, cache)
        time.sleep(0.05)

    return embeddings


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


class EmbeddingRetriever:
    def __init__(self, signals, embeddings, model, base_url, api_key, timeout, cache_path, dimensions):
        self.signals = signals
        self.embeddings = embeddings
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.cache_path = cache_path
        self.dimensions = dimensions

    @classmethod
    def build(cls, signals, model, base_url, api_key, timeout, cache_path, dimensions=1024):
        texts = [embedding_text(signal) for signal in signals]
        embeddings = get_embeddings(texts, model, base_url, api_key, timeout, cache_path, dimensions=dimensions)
        return cls(signals, embeddings, model, base_url, api_key, timeout, cache_path, dimensions)

    def search(self, query, top_k=20):
        query = normalize(query)
        if not query:
            return []
        query_embedding = get_embeddings(
            [query],
            self.model,
            self.base_url,
            self.api_key,
            self.timeout,
            self.cache_path,
            dimensions=self.dimensions,
        )[0]
        scored = [
            (cosine_similarity(query_embedding, embedding), signal)
            for signal, embedding in zip(self.signals, self.embeddings)
            if embedding
        ]
        scored.sort(key=lambda item: item[0], reverse=True)
        return [{"score": score, "signal": signal} for score, signal in scored[:top_k]]
