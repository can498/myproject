"""Map text cases to requirement SignalName values with an LLM.

This is a minimal signal-grounding script:
text fragment -> candidate Chinese names -> LLM chooses one SignalName.
It does not contain hardcoded domain mapping rules.
"""

import argparse
import json
import os
import re
import socket
import ssl
import time
import urllib.error
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def default_provider_from_env():
    explicit = os.environ.get("LLM_PROVIDER") or os.environ.get("API_PROVIDER")
    if explicit:
        return explicit.lower()
    return "qwen"


DEFAULT_PROVIDER = default_provider_from_env()
PROVIDER_DEFAULTS = {
    "qwen": {
        "model": os.environ.get("QWEN_MODEL", "qwen3.7-plus"),
        "base_url": os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "api_key": os.environ.get("QWEN_API_KEY") or os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY"),
    },
    "openai": {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": os.environ.get("OPENAI_API_KEY"),
    },
    "transformers": {
        "model": os.environ.get("LOCAL_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        "base_url": "",
        "api_key": "local",
    },
}


def provider_defaults(provider):
    provider = ("" if provider is None else str(provider)).strip().lower() or "qwen"
    return PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["qwen"])


DEFAULTS = provider_defaults(DEFAULT_PROVIDER)
POSITION_CODES = ("FL", "FR", "RL", "RR")


def default_requirement_file():
    for path in [
        PROJECT_ROOT / "demo" / "需求1-1_完整版_AI.xlsx"
    ]:
        if path.exists():
            return path
    return PROJECT_ROOT / "需求1-1.xlsx"


SYSTEM_PROMPT = """你是汽车 HIL 测试用例的信号映射助手。你的任务只有一个：根据用例短语，从候选需求信号里选出最匹配的 SignalName。只能依据 candidates 里的 Name In Chinese 做判断，禁止编造候选之外的 SignalName。短语表达“已进入/已挂入/已生效”时，优先选择表示状态已经有效的候选，而不是仅表示原始状态值的候选。短语表达“实际高度/实际位置/实际值”时，必须选择对应实际测量量的候选，不能选择执行器电流、阀控制、请求或目标类候选。短语表达“已挂入X挡/已进入Y挡”时，优先选择“整车实际挡位有效”这类有效状态候选。短语表达“实际空簧高度在调节中/停止调节/继续变化/停止变化”时，仍然表示四个角的实际空簧高度信号，应选择高度信号并展开到对应位置，不能选择模式状态、阀电流或锁止控制候选。只返回 JSON，不要解释。"""

USER_PROMPT_TEMPLATE = """输入如下：
{
  "text": "...",
  "role": "write|read",
  "candidates": [
    {"signalName": "...", "chineseName": "..."}
  ]
}

要求：1. 只从 candidates 里选一个最匹配的 signalName。2. 主要依据 chineseName 语义，不要编造。3. 如果无法判断，返回空字符串。4. 只返回 JSON，格式如下：
{"signalName":"...","reason":"..."}
"""

VALUE_PROMPT = """你是汽车 HIL 信号取值解析助手。任务：根据用例短语和已选定信号的 Description，提取 write/read 指令等号后的 value。
要求：1. SignalName 已经选定，不要重新匹配信号。2. 优先根据 Description 中的枚举、编码、物理值解释 value。3. 如果短语里有明确数值，例如 0km/h、25mm、x2，返回可直接比较/写入的值，例如 0、25、x2。4. 如果短语是 P挡/D挡/N挡/R挡，返回 P/D/N/R，除非 Description 明确要求数字编码。5. 如果 Description 说明“标准0x0、运动0x1”这类枚举，要返回对应编码。6. 保留小数，不要把 4.9 拆成 4 或 9。7. 如果短语表达过程状态而不是数值，例如“处于变化中”“开始调节”“停止变化”“停止调节”，返回短语中的核心状态值。8. 如果无法确定，返回空字符串。9. 只返回 JSON，格式如下：
{"value":"..."}
"""

MULTI_VALUE_PROMPT = """你是汽车 HIL 多信号取值解析助手。任务：根据用例短语、上下文参数和已经选定的多个信号，分别提取每个 read/write 指令等号后的 value。
要求：1. SignalName 已经选定，不要重新匹配信号。2. 结合上下文中的参数名、参数值、括号说明理解每个信号对应的位置和值。3. 如果短语描述左右差、前后差、同轴差、某侧偏高/偏低/保持目标高度等关系，要给每个已选信号分别填写 value，不要把阈值本身直接当成所有信号的 value。4. 如果上下文中给出了“指定...高度/模式”这类参数名，输出应使用该参数名表达相对值。5. 如果无法判断某个信号的 value，返回空字符串。6. 只返回 JSON，格式如下：
{"values":[{"signalName":"...","value":"..."}]}
"""


def normalize_text(value):
    return "" if value is None else str(value).replace("\u3000", " ").strip()


def split_text_items(value): 
    text = normalize_text(value)
    if not text or text == "/":
        return []
    text = re.sub(r"(?<!^)(?<![\r\n])\s*(\d+[、.．)])", r"\n\1", text)
    text = re.sub(r"^\s*\d+[、.．)]\s*", "", text, flags=re.M)
    return [item.strip() for item in re.split(r"[;\r\n]+", text) if item.strip()]


def char_ngrams(text, min_n=2, max_n=3):
    text = re.sub(r"\s+", "", normalize_text(text))
    grams = set()
    for n in range(min_n, max_n + 1):
        grams.update(text[i : i + n] for i in range(max(0, len(text) - n + 1)))
    return {gram for gram in grams if gram}


def overlap_score(left, right):
    left_grams = char_ngrams(left)
    right_grams = char_ngrams(right)
    if not left_grams or not right_grams:
        return 0.0
    return len(left_grams & right_grams) / len(left_grams)


def normalize_inferred_value(value):
    return normalize_text(value)


def should_expand_positions(text, signal_name):
    if any(pos in normalize_text(text).upper() for pos in POSITION_CODES):
        return False
    if re.search(r"高度|四轮|各轮|前后|左右|空簧|悬架", normalize_text(text)):
        return True
    return positional_signature(signal_name) is not None


def load_requirement_catalog(requirement_path):
    workbook = load_workbook(requirement_path, data_only=True, read_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    signal_col = None
    chinese_col = None
    description_col = None
    headers = [sheet.cell(1, col).value for col in range(1, sheet.max_column + 1)]
    for idx, header in enumerate(headers):
        text = normalize_text(header)
        if text == "SignalName":
            signal_col = idx
        elif text == "Name In Chinese":
            chinese_col = idx
        elif text.startswith("Description"):
            description_col = idx

    if signal_col is None or chinese_col is None:
        raise ValueError("Cannot find exact columns: SignalName and Name In Chinese")

    catalog = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if signal_col is None or chinese_col is None:
            continue
        signal = normalize_text(row[signal_col]) if signal_col < len(row) else ""
        chinese = normalize_text(row[chinese_col]) if chinese_col < len(row) else ""
        description = normalize_text(row[description_col]) if description_col is not None and description_col < len(row) else ""
        if signal and chinese:
            catalog.append({"signalName": signal, "chineseName": chinese, "description": description})
    return catalog


def top_candidates(text, catalog, top_k=20, query_variants=None):
    queries = [text] + [query for query in (query_variants or []) if normalize_text(query)]
    scored = [
        (max(overlap_score(query, item["chineseName"]) for query in queries), item)
        for item in catalog
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    positive = [(score, item) for score, item in scored if score > 0]
    if not positive:
        return catalog[:top_k]
    cutoff = positive[min(top_k, len(positive)) - 1][0]
    # Keep tied candidates together; their input order must not decide the signal.
    return [item for score, item in positive if score >= cutoff]


def has_direct_name_overlap(text, catalog):
    """Whether the source phrase itself has enough information for normal recall."""
    return any(overlap_score(text, item["chineseName"]) > 0 for item in catalog)


def positional_signature(signal_name):
    for pos in POSITION_CODES:
        if pos in signal_name:
            return signal_name.replace(pos, "{POS}", 1)
    if "XX" in signal_name:
        return signal_name.replace("XX", "{POS}", 1)
    return None


def expand_positional_signal(text, signal_name, catalog):
    if not should_expand_positions(text, signal_name):
        return [signal_name]
    signature = positional_signature(signal_name)
    if not signature:
        return [signal_name]
    known = {item["signalName"] for item in catalog}
    text = normalize_text(text)
    positions = POSITION_CODES
    if "前轴" in text:
        positions = ("FL", "FR")
    elif "后轴" in text:
        positions = ("RL", "RR")
    expanded = [signature.replace("{POS}", pos) for pos in positions]
    expanded = [item for item in expanded if item in known]
    return expanded if len(expanded) >= 2 else [signal_name]


LOCAL_PIPELINES = {}

# 允许命令行使用简写 ``qwen2.5-7b``；实际从 Hugging Face 加载
# Qwen2.5 的指令微调版本。也可以直接传本地模型目录。
LOCAL_MODEL_ALIASES = {
    "qwen2.5-7b": "Qwen/Qwen2.5-7B-Instruct",
    "qwen2.5-7b-instruct": "Qwen/Qwen2.5-7B-Instruct",
}


def local_chat_completion(messages, model, timeout):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = normalize_text(model) or "Qwen/Qwen2.5-7B-Instruct"
    model_name = LOCAL_MODEL_ALIASES.get(model_name.lower(), model_name)
    if model_name not in LOCAL_PIPELINES:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        local_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype,
            device_map="auto",
            trust_remote_code=True,
        )
        local_model.eval()
        LOCAL_PIPELINES[model_name] = (tokenizer, local_model)
    tokenizer, local_model = LOCAL_PIPELINES[model_name]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([prompt], return_tensors="pt").to(local_model.device)
    with torch.no_grad():
        generated = local_model.generate(
            **inputs,
            max_new_tokens=int(os.environ.get("LOCAL_MAX_NEW_TOKENS", "512")),
            do_sample=False,
            temperature=None,
            top_p=None,
            pad_token_id=tokenizer.eos_token_id,
        )
    output_ids = generated[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(output_ids, skip_special_tokens=True).strip()


def chat_completion(messages, model, base_url, api_key, timeout, retries=4):
    if normalize_text(base_url).lower() in {"transformers", "local", "hf"}:
        return local_chat_completion(messages, model, timeout)

    import urllib.request

    body = json.dumps(
        {"model": model, "messages": messages, "temperature": 0.0, "response_format": {"type": "json_object"}},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    last_error = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionResetError, ssl.SSLError) as error:
            last_error = error
            if attempt >= retries:
                raise RuntimeError(
                    f"API connection failed: {error}. "
                    f"provider/base-url may be unreachable. Current base-url: {base_url}"
                ) from error
            time.sleep(1.5 * (attempt + 1))
    return payload["choices"][0]["message"]["content"]


def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end >= start:
        text = text[start : end + 1]
    return json.loads(text)


def llm_restate_signal_name(text, role, model, base_url, api_key, timeout, cache=None, context=""):
    """Turn a test phrase into a canonical Chinese signal-name query for recall only."""
    context = normalize_text(context)
    cache_key = ("restate", normalize_text(text), role, context)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    messages = [
        {
            "role": "system",
            "content": (
                "Rewrite the Chinese automotive HIL test phrase as the most likely "
                "canonical Chinese signal name. This is only for candidate retrieval, "
                "not a final signal selection. Keep the measured/requested object and "
                "state semantics, remove values and test verbs, and return JSON only: "
                '{"targetChineseName":"..."}.'
            ),
        },
        {"role": "user", "content": json.dumps({"text": text, "role": role, "context": context}, ensure_ascii=False)},
    ]
    try:
        data = extract_json(chat_completion(messages, model, base_url, api_key, timeout))
        result = normalize_text(data.get("targetChineseName"))
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError):
        result = ""
    if cache is not None:
        cache[cache_key] = result
    return result


def stable_signal_cache_key(text, role, semantic_query, context=""):
    key_text = normalize_text(semantic_query) or normalize_text(text)
    if not key_text:
        return None
    return ("stable_signal", role, key_text, normalize_text(context))


def exact_chinese_name_matches(text, catalog):
    text = normalize_text(text)
    matches = []
    for item in catalog:
        chinese_name = normalize_text(item.get("chineseName"))
        if len(chinese_name) >= 4 and chinese_name in text:
            matches.append(item)
    matches.sort(key=lambda item: len(normalize_text(item.get("chineseName"))), reverse=True)
    return matches


def llm_pick_signal(text, role, candidates, model, base_url, api_key, timeout, cache=None, context=""):
    context = normalize_text(context)
    cache_key = (
        "pick",
        normalize_text(text),
        role,
        context,
        tuple(item.get("signalName", "") for item in candidates),
    )
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    candidate_view = [
        {
            "signalName": item.get("signalName", ""),
            "chineseName": item.get("chineseName", ""),
        }
        for item in candidates
    ]
    payload = {
        "text": text,
        "role": role,
        "context": context,
        "candidates": candidate_view,
        "instruction": USER_PROMPT_TEMPLATE,
        "output": {"signalName": "", "reason": ""},
    }
    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n"
                "Map the Chinese HIL test phrase to exactly one listed requirement signal. "
                "If context is provided, use it only to understand the current fragment's "
                "original sentence and omitted timing/condition information. "
                "Use the semantic meaning of chineseName only; do not apply any "
                "domain-specific substitution rule and do not invent a signalName. "
                "When a phrase says a gear is already engaged, already entered, "
                "or already effective, prefer a candidate whose chineseName means "
                "the actual gear state is valid/effective over a candidate that only "
                "means the raw actual gear position. "
                "Return JSON only."
            ),
        },
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    content = chat_completion(messages, model, base_url, api_key, timeout)
    data = extract_json(content)
    signal_name = normalize_text(data.get("signalName"))
    if signal_name and any(item["signalName"] == signal_name for item in candidates):
        if cache is not None:
            cache[cache_key] = signal_name
        return signal_name
    if cache is not None:
        cache[cache_key] = ""
    return ""


def llm_infer_value(text, role, signal, model, base_url, api_key, timeout, cache=None, context=""):
    placeholder = re.search(r"指定[^，。；;\r\n（）()]*", normalize_text(text))
    if placeholder:
        return placeholder.group(0)
    context = normalize_text(context)
    cache_key = ("value", normalize_text(text), role, signal.get("signalName", ""), context)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    payload = {
        "text": text,
        "role": role,
        "context": context,
        "signal": {
            "signalName": signal.get("signalName", ""),
            "chineseName": signal.get("chineseName", ""),
            "description": signal.get("description", ""),
        },
        "instruction": VALUE_PROMPT,
        "output": {"value": ""},
    }
    messages = [
        {
            "role": "system",
            "content": (
                VALUE_PROMPT
                + "\nIf the text does not contain an explicit value, use context to infer "
                "the value for the selected signal and its position. For enumerations in "
                "Description, return the corresponding code/value. Return the minimal "
                "core value only, not the whole sentence. Remove timing words, test verbs, "
                "time-window words such as within/during, signal names, and surrounding "
                "conditions from the value."
            ),
        },
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    content = chat_completion(messages, model, base_url, api_key, timeout)
    data = extract_json(content)
    value = normalize_inferred_value(data.get("value"))
    if value and re.search(r"[,，;；。]", value):
        verify_messages = [
            {
                "role": "system",
                "content": (
                    "Return the atomic value for the selected HIL signal. The answer must "
                    "be the smallest standalone value that can appear after '=' in a HIL "
                    "command. Do not return a sentence, clause, timing word, test action, "
                    "signal name, punctuation, or explanation. Use Description only to "
                    "map a stated meaning to its encoded value. Return JSON only: "
                    '{"value":"..."}.'
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "text": text,
                        "context": context,
                        "candidateValue": value,
                        "signal": {
                            "signalName": signal.get("signalName", ""),
                            "chineseName": signal.get("chineseName", ""),
                            "description": signal.get("description", ""),
                        },
                    },
                    ensure_ascii=False,
                ),
            },
        ]
        try:
            verified = extract_json(chat_completion(verify_messages, model, base_url, api_key, timeout))
            value = normalize_inferred_value(verified.get("value")) or value
        except (RuntimeError, ValueError, KeyError, json.JSONDecodeError):
            pass
    if cache is not None:
        cache[cache_key] = value
    return value


def llm_infer_values_for_signals(text, role, signals, model, base_url, api_key, timeout, cache=None, context=""):
    context = normalize_text(context)
    signal_view = [
        {
            "signalName": signal.get("signalName", ""),
            "chineseName": signal.get("chineseName", ""),
        }
        for signal in signals
    ]
    cache_key = (
        "multi_value",
        normalize_text(text),
        role,
        tuple(item["signalName"] for item in signal_view),
        context,
    )
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    payload = {
        "text": text,
        "role": role,
        "context": context,
        "signals": signal_view,
        "instruction": MULTI_VALUE_PROMPT,
        "output": {"values": [{"signalName": "", "value": ""}]},
    }
    messages = [
        {
            "role": "system",
            "content": (
                MULTI_VALUE_PROMPT
                + "\nReturn only the minimal value text that should appear after '='. "
                "Do not return full sentences or explanations. Preserve parameter names "
                "from context when they are needed to express relative expected values."
            ),
        },
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    try:
        data = extract_json(chat_completion(messages, model, base_url, api_key, timeout))
        allowed = {item["signalName"] for item in signal_view}
        values = {}
        for item in data.get("values", []):
            signal_name = normalize_text(item.get("signalName"))
            if signal_name in allowed:
                values[signal_name] = normalize_inferred_value(item.get("value"))
    except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        values = {}
    if cache is not None:
        cache[cache_key] = values
    return values


def chunks(items, size):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def fallback_pick_signal(text, role, catalog, model, base_url, api_key, timeout, cache=None, batch_size=80, context=""):
    for batch in chunks(catalog, batch_size):
        signal_name = llm_pick_signal(text, role, batch, model, base_url, api_key, timeout, cache, context=context)
        if signal_name:
            return signal_name
    return ""


def has_candidate_evidence(text, candidates):
    text = normalize_text(text)
    return any(overlap_score(text, item["chineseName"]) > 0 for item in candidates)


def focus_candidates_by_text(text, role, candidates):
    """Prefer candidates whose Chinese name matches the measured object in text."""
    text = normalize_text(text)
    if role == "read" and re.search(r"(?:实际)?[^，,；;。]*高度", text):
        height_candidates = [
            item for item in candidates
            if "高度" in normalize_text(item.get("chineseName"))
        ]
        if height_candidates:
            return height_candidates
    return candidates


def select_signal_name(text, role, catalog, model, base_url, api_key, timeout, top_k=20, cache=None, context=""):
    semantic_query = llm_restate_signal_name(text, role, model, base_url, api_key, timeout, cache, context=context)
    stable_key = stable_signal_cache_key(text, role, semantic_query, context)
    exact_matches = exact_chinese_name_matches(text, catalog)
    exact_names = {item["signalName"] for item in exact_matches}
    if cache is not None and stable_key in cache and not exact_names:
        return cache[stable_key], exact_matches or catalog
    if top_k is None or top_k <= 0:
        candidates = catalog
    elif has_direct_name_overlap(text, catalog):
        candidates = top_candidates(text, catalog, top_k=top_k, query_variants=[semantic_query])
    else:
        candidates = top_candidates(text, catalog, top_k=top_k, query_variants=[semantic_query])
    candidates = focus_candidates_by_text(text, role, candidates)
    if top_k and top_k > 0 and not has_candidate_evidence(text, candidates):
        return "", candidates
    signal_name = llm_pick_signal(text, role, candidates, model, base_url, api_key, timeout, cache, context=context)
    if not signal_name:
        signal_name = fallback_pick_signal(text, role, catalog, model, base_url, api_key, timeout, cache, context=context)
    if signal_name and cache is not None and stable_key is not None:
        cache[stable_key] = signal_name
    return signal_name, candidates


def map_text_item(item, role, catalog, model, base_url, api_key, timeout, top_k=20, cache=None, context="", signal_text=None):
    text = normalize_text(item)
    if not text or text == "/":
        return []
    signal_source = normalize_text(signal_text) or text
    signal_name, candidates = select_signal_name(signal_source, role, catalog, model, base_url, api_key, timeout, top_k=top_k, cache=cache, context=context)
    if not signal_name:
        return [{"text": text, "role": role, "signalName": "", "candidates": candidates}]
    catalog_by_name = {item["signalName"]: item for item in catalog}
    rows = []
    expanded_names = expand_positional_signal(signal_source, signal_name, catalog)
    base_signal = catalog_by_name.get(signal_name, {})
    expanded_signals = [catalog_by_name.get(expanded_name, {"signalName": expanded_name}) for expanded_name in expanded_names]
    per_signal_values = {}
    if len(expanded_signals) > 1:
        per_signal_values = llm_infer_values_for_signals(
            text,
            role,
            expanded_signals,
            model,
            base_url,
            api_key,
            timeout,
            cache,
            context=context,
        )
    shared_value = llm_infer_value(
        text,
        role,
        base_signal,
        model,
        base_url,
        api_key,
        timeout,
        cache,
        context=context,
    )
    for expanded_name in expanded_names:
        signal = catalog_by_name.get(expanded_name, {})
        chinese_name = normalize_text(signal.get("chineseName"))
        value = per_signal_values.get(expanded_name) or shared_value
        rows.append({
            "text": text,
            "role": role,
            "signalName": expanded_name,
            "chineseName": chinese_name,
            "value": value,
        })
    return rows


def map_text_cell(value, role, catalog, model, base_url, api_key, timeout, top_k=20, cache=None, context=""):
    rows = []
    for item in split_text_items(value):
        fixed = fixed_commands(item)
        if fixed:
            rows.extend(
                {"text": item, "role": role, "signalName": "__COMMAND__", "chineseName": "", "value": command}
                for command in fixed
            )
            continue
        text = normalize_text(item)
        item_context = "\n".join(part for part in [normalize_text(context), f"原句：{text}"] if part)
        wait_hits = list(re.finditer(
            r"(?:\u7b49\u5f85|\u7b49\u5019|wait|\u6301\u7eed)\s*\d+(?:\.\d+)?\s*(?:ms|\u6beb\u79d2|s|\u79d2|sec|second|seconds|min|\u5206\u949f)?|\d+(?:\.\d+)?\s*(?:ms|\u6beb\u79d2|s|\u79d2|sec|second|seconds|min|\u5206\u949f)\s*\u540e",
            text,
            re.I,
        ))
        if not wait_hits:
            rows.extend(map_text_item(text, role, catalog, model, base_url, api_key, timeout, top_k=top_k, cache=cache, context=context))
            continue
        cursor = 0
        for hit in wait_hits:
            prefix = text[cursor:hit.start()].strip(" ,，、；;")
            if prefix:
                fragment_context = "\n".join([item_context, f"当前片段：{prefix}"])
                rows.extend(map_text_item(prefix, role, catalog, model, base_url, api_key, timeout, top_k=top_k, cache=cache, context=fragment_context, signal_text=text))
            rows.append({"text": hit.group(0), "role": role, "signalName": "__WAIT__", "chineseName": "", "value": ""})
            cursor = hit.end()
        suffix = text[cursor:].strip(" ,，、；;")
        if suffix:
            fragment_context = "\n".join([item_context, f"当前片段：{suffix}"])
            rows.extend(map_text_item(suffix, role, catalog, model, base_url, api_key, timeout, top_k=top_k, cache=cache, context=fragment_context, signal_text=text))
    return rows


def fixed_commands(value):
    text = re.sub(r"\s+", "", normalize_text(value))
    if "初始状态检测" in text or "整车上电" in text or re.search(r"power\s*up|powerup", text, re.I):
        return ["POWERUP"]
    if "整车下电" in text or re.search(r"power\s*down|powerdown", text, re.I):
        return ["POWERDOWN"]
    return []


def extract_wait_commands(value):
    text = normalize_text(value)
    commands = []
    patterns = [
        r"(?:\u7b49\u5f85|\u7b49\u5019|wait|\u6301\u7eed)\s*(\d+(?:\.\d+)?)\s*(ms|\u6beb\u79d2|s|\u79d2|sec|second|seconds|min|\u5206\u949f)?",
        r"(\d+(?:\.\d+)?)\s*(ms|\u6beb\u79d2|s|\u79d2|sec|second|seconds|min|\u5206\u949f)\s*\u540e",
    ]
    seen = set()
    for pattern in patterns:
        for amount, unit in re.findall(pattern, text, re.I):
            unit_text = normalize_text(unit).lower()
            normalized_unit = "ms" if unit_text in {"ms", "\u6beb\u79d2"} else "s"
            if unit_text in {"min", "\u5206\u949f"}:
                amount = str(float(amount) * 60).rstrip("0").rstrip(".")
            command = f"wait={amount}{normalized_unit}"
            if command not in seen:
                seen.add(command)
                commands.append(command)
    return commands


def remove_wait_clauses(value):
    text = normalize_text(value)
    text = re.sub(
        r"(?:[,，；;]?\s*)(?:等待|等待中|wait|持续)\s*\d+(?:\.\d+)?\s*(?:ms|毫秒|s|秒|sec|second|seconds|min|分钟)?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(?:[,，；;]?\s*)\d+(?:\.\d+)?\s*(?:ms|毫秒|s|秒|sec|second|seconds|min|分钟)\s*(?:后|内)",
        "",
        text,
        flags=re.I,
    )
    return text


def normalize_command_value(text, value):
    source = normalize_text(value) or normalize_text(text)
    source = remove_wait_clauses(source).strip(" ,，、；;。")
    if not source:
        return ""
    source = re.split(r"[，,；;。]\s*", source)[-1].strip()
    with_comparator = re.sub(
        r"^.*?(?:为|是|处于|保持为|变为|显示为|=|==)\s*",
        "",
        source,
        count=1,
    ).strip()
    if with_comparator and with_comparator != source:
        return with_comparator
    without_subject = re.sub(
        r"^(?:检测|检验|确认|读取|观察|查看)?[^，,；;。]*(?:高度|状态|模式|挡位|车速|信号|值)\s*",
        "",
        source,
        count=1,
    ).strip()
    without_subject = re.sub(r"^(?:也|仍|仍然|依然)\s*", "", without_subject)
    return without_subject or source


def render_commands(mapped_rows, role):
    commands = []
    for row in mapped_rows:
        signal_name = normalize_text(row.get("signalName"))
        if signal_name == "__COMMAND__":
            command = normalize_text(row.get("value"))
            if command:
                commands.append(command)
            continue
        if signal_name == "__WAIT__":
            commands.extend(extract_wait_commands(row.get("text")))
            continue
        if not signal_name:
            continue
        text = normalize_text(row.get("text"))
        value = normalize_text(row.get("value"))
        if role == "write":
            commands.append(f"write#{signal_name}={value or '指定值'}")
        else:
            commands.append(f"read#{signal_name}={normalize_command_value(text, value)}")
    return commands


def set_cell_value(sheet, row, col, value):
    cell = sheet.cell(row, col)
    if isinstance(cell, MergedCell):
        return
    cell.value = value


def find_hil_columns(sheet):
    for col in range(1, sheet.max_column + 1):
        value = normalize_text(sheet.cell(1, col).value)
        if "HIL" in value:
            return {"initial": col, "step_id": col + 1, "action": col + 2, "expected": col + 3}
    return {"initial": 8, "step_id": 9, "action": 10, "expected": 11}


def unmerge_hil_output_cells(sheet, hil_columns, first_row=3):
    output_cols = set(hil_columns.values())
    ranges_to_unmerge = []
    for merged in sheet.merged_cells.ranges:
        if merged.max_row < first_row:
            continue
        if any(col in output_cols for col in range(merged.min_col, merged.max_col + 1)):
            ranges_to_unmerge.append(str(merged))
    for merged_range in ranges_to_unmerge:
        sheet.unmerge_cells(merged_range)


def case_ranges(sheet):
    starts = [row for row in range(3, sheet.max_row + 1) if sheet.cell(row, 1).value]
    merged_by_start = {
        merged.min_row: merged.max_row
        for merged in sheet.merged_cells.ranges
        if merged.min_col == 1 and merged.max_col == 1
    }
    ranges = []
    for index, start in enumerate(starts):
        next_start = starts[index + 1] if index + 1 < len(starts) else sheet.max_row + 1
        end = min(merged_by_start.get(start, next_start - 1), next_start - 1)
        ranges.append((start, end))
    return ranges


def extract_workbook_from_text(
    workbook_path,
    requirement_path,
    selected_sheets=None,
    max_sheets=None,
    model=None,
    base_url=None,
    api_key=None,
    timeout=90,
    top_k=20,
):
    catalog = load_requirement_catalog(requirement_path)
    if len(catalog) < 50:
        raise ValueError(f"Only loaded {len(catalog)} signals from requirement file: {requirement_path}")
    workbook = load_workbook(workbook_path)
    selected = set(selected_sheets or workbook.sheetnames)
    results = []
    cache = {}
    sheets = workbook.worksheets[:max_sheets] if max_sheets else workbook.worksheets
    for sheet in sheets:
        if sheet.title not in selected:
            continue
        hil_columns = find_hil_columns(sheet)
        unmerge_hil_output_cells(sheet, hil_columns)
        for start_row, end_row in case_ranges(sheet):
            case_rows = []
            case_context = "\n".join(
                part
                for part in [
                    normalize_text(sheet.cell(start_row, 2).value),
                    normalize_text(sheet.cell(start_row, 4).value),
                ]
                if part
            )
            initial_commands = fixed_commands(sheet.cell(start_row, hil_columns["initial"] - 4).value)
            set_cell_value(sheet, start_row, hil_columns["initial"], "\n".join(initial_commands))
            for row in range(start_row, end_row + 1):
                action_text = sheet.cell(row, hil_columns["action"] - 4).value
                expected_text = sheet.cell(row, hil_columns["expected"] - 4).value
                row_context = "\n".join(
                    part
                    for part in [
                        case_context,
                        normalize_text(sheet.cell(row, 4).value),
                    ]
                    if part
                )
                action_mapped = map_text_cell(
                    action_text,
                    "write",
                    catalog,
                    model,
                    base_url,
                    api_key,
                    timeout,
                    top_k=top_k,
                    cache=cache,
                    context=row_context,
                )
                expected_mapped = map_text_cell(
                    expected_text,
                    "read",
                    catalog,
                    model,
                    base_url,
                    api_key,
                    timeout,
                    top_k=top_k,
                    cache=cache,
                    context=row_context,
                )
                action_commands = render_commands(action_mapped, "write")
                expected_commands = render_commands(expected_mapped, "read")
                step = normalize_text(sheet.cell(row, hil_columns["step_id"] - 4).value)
                if step:
                    set_cell_value(sheet, row, hil_columns["step_id"], step)
                set_cell_value(sheet, row, hil_columns["action"], "\n".join(action_commands))
                set_cell_value(sheet, row, hil_columns["expected"], "\n".join(expected_commands))
                case_rows.append({
                    "row": row,
                    "step": step,
                    "initialCommands": initial_commands if row == start_row else [],
                    "action": action_mapped,
                    "expected": expected_mapped,
                })
            results.append({
                "sheet": sheet.title,
                "range": f"{start_row}-{end_row}",
                "caseName": normalize_text(sheet.cell(start_row, 1).value),
                "rows": case_rows,
            })
    return {"catalogSize": len(catalog), "cases": results}, workbook


def main():
    parser = argparse.ArgumentParser(description="用大模型把文本用例里的中文短语映射成需求表 SignalName")
    parser.add_argument("input", nargs="?", default=str(PROJECT_ROOT / "用例1-1.xlsx"))
    parser.add_argument("--requirement", default=str(default_requirement_file()))
    parser.add_argument("--sheet", action="append", help="只处理指定工作表，可重复")
    parser.add_argument("--max-sheets", type=int, default=None, help="只处理前 N 个工作表")
    parser.add_argument("--output", default=str(PROJECT_ROOT / "demo" / "用例1-1_HIL_simple.xlsx"))
    parser.add_argument("--json-output", default=None, help="另存匹配明细 JSON；默认与 output 同名")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER, choices=sorted(PROVIDER_DEFAULTS.keys()))
    parser.add_argument("--model", default=DEFAULTS["model"])
    parser.add_argument("--base-url", default=DEFAULTS["base_url"])
    parser.add_argument("--api-key", default=DEFAULTS["api_key"])
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument(
        "--top-k",
        type=int,
        default=0,
        help="每次给模型的候选数；默认 0 表示完整需求表，数值大于 0 时启用候选召回以加快运行",
    )
    args = parser.parse_args()

    if args.provider == "transformers":
        args.base_url = "transformers"
        args.api_key = args.api_key or "local"

    if not args.api_key:
        key_names = {
            "qwen": "QWEN_API_KEY or DASHSCOPE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "transformers": "LOCAL_MODEL",
        }.get(args.provider, "the provider API key")
        raise SystemExit(
            f"Please set {key_names}, or pass --api-key. "
            f"Current provider: {args.provider}, base-url: {args.base_url}"
        )

    result, workbook = extract_workbook_from_text(
        args.input,
        args.requirement,
        args.sheet,
        args.max_sheets,
        args.model,
        args.base_url,
        args.api_key,
        args.timeout,
        args.top_k,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    json_output = Path(args.json_output) if args.json_output else output_path.with_suffix(".json")
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"requirement={Path(args.requirement).resolve()}")
    print(f"catalogSize={result['catalogSize']}")
    print(f"output={output_path.resolve()}")
    print(f"json={json_output.resolve()}")


if __name__ == "__main__":
    main()
