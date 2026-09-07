"""Fill blank SignalName cells in requirement workbook using an LLM only.

Input:
  - requirement workbook (需求1-1.xlsx)
  - case workbook (用例1-1.xlsx), used only as style/context reference
  - seed workbook (需求1-1_AI填充.xlsx), used as the primary SignalName seed

Output:
  - copied workbook with AI-filled SignalName cells
  - audit sheet describing each filled row

This script does not use the case workbook to derive signal names directly.
It only uses the case workbook as a style/context reference for Description.
"""

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import PatternFill


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "qwen-turbo")
DEFAULT_BASE_URL = os.environ.get(
    "OPENAI_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

SYSTEM_PROMPT = """You are filling a vehicle signal matrix.
Your job is to infer the SignalName and a useful Description draft for a requirement row.

Rules:
1. Return JSON only.
2. Use the workbook row context, especially Chinese name, sender, description, nearby rows, and case-design style references.
5. Do not output Chinese words as SignalName.
6. Do not output verbose descriptions, spaces, punctuation, or explanations inside SignalName.
7. Prefer common automotive abbreviations:
   - request: Req
   - feedback: FB
   - valid: Vld
   - status: Sts
   - front left/right/rear left/rear right: FL/FR/RL/RR
8. Follow these naming patterns when possible:
   - request signals: <System><Thing>Req
   - feedback signals: <System><Thing>FB
   - status signals: <System><Thing>Sts
   - valid flags: <Thing>Vld
   - wheel-specific signals: use FL/FR/RL/RR suffixes
   - mode or level signals: use Mode, Lvl, Posn, or similar short engineering terms
9. If you are not confident about SignalName, return an empty signalName.
10. Description can be Chinese. It should briefly explain the signal meaning or enum mapping when obvious from context.
11. Do not fabricate exact bit/DBC data in Description.
12. When Description is an enum or fault map, use multiline `0x... = ...` style similar to the provided examples.

Return schema:
{
  "signalName": "ExactSignalNameOrEmpty",
  "description": "DescriptionDraftOrEmpty",
  "reason": "short reason in Chinese or English"
}
"""


def normalize(value):
    return "" if value is None else str(value).replace("\u3000", " ").strip()


def default_requirement():
    candidates = [p for p in PROJECT_ROOT.glob("*.xlsx") if p.name == "需求1-1.xlsx"]
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError("Cannot find 需求1-1.xlsx in project root.")


def default_case():
    candidates = [p for p in PROJECT_ROOT.glob("*.xlsx") if p.name == "用例1-1.xlsx"]
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError("Cannot find 用例1-1.xlsx in project root.")


def default_seed():
    candidates = [p for p in (PROJECT_ROOT / "demo").glob("*.xlsx") if p.name == "需求1-1_AI填充.xlsx"]
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError("Cannot find 需求1-1_AI填充.xlsx in demo directory.")


def find_col(headers, *names):
    for index, header in enumerate(headers):
        header = normalize(header)
        if any(name.lower() in header.lower() for name in names):
            return index
    return None


def chat_completion(messages, model, base_url, api_key, timeout):
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def extract_json(text):
    return json.loads(text)


def build_row_context(sheet, row, window=2):
    start = max(1, row - window)
    end = min(sheet.max_row, row + window)
    rows = []
    for r in range(start, end + 1):
        rows.append({
            "row": r,
            "subnet": normalize(sheet.cell(r, 1).value),
            "sender": normalize(sheet.cell(r, 2).value),
            "signalName": normalize(sheet.cell(r, 3).value),
            "chineseName": normalize(sheet.cell(r, 4).value),
            "description": normalize(sheet.cell(r, 16).value),
            "note": normalize(sheet.cell(r, 20).value),
        })
    return rows


def load_case_style_context(case_path, limit_per_sheet=8):
    workbook = load_workbook(case_path, data_only=True, read_only=True)
    samples = []
    for sheet in workbook.worksheets:
        count = 0
        for r in range(4, sheet.max_row + 1):
            case_name = normalize(sheet.cell(r, 1).value)
            settings = normalize(sheet.cell(r, 2).value)
            cs_id = normalize(sheet.cell(r, 3).value)
            cs_details = normalize(sheet.cell(r, 4).value)
            if not (case_name or settings or cs_id or cs_details):
                continue
            samples.append({
                "sheet": sheet.title,
                "row": r,
                "caseName": case_name,
                "settings": settings,
                "csId": cs_id,
                "csDetails": cs_details,
            })
            count += 1
            if count >= limit_per_sheet:
                break
    return samples


def load_seed_signal_map(seed_path):
    workbook = load_workbook(seed_path, data_only=True, read_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    signal_map = {}
    for row in range(2, sheet.max_row + 1):
        chinese_name = normalize(sheet.cell(row, 4).value)
        signal_name = normalize(sheet.cell(row, 3).value)
        if chinese_name and signal_name and chinese_name not in signal_map:
            signal_map[chinese_name] = signal_name
    return signal_map


def infer_signal_name(sheet, row, case_style_context, model, base_url, api_key, timeout):
    context = build_row_context(sheet, row)
    payload = {
        "targetRow": row,
        "rowContext": context,
        "caseStyleContext": case_style_context,
    }
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
    content = chat_completion(messages, model, base_url, api_key, timeout)
    result = extract_json(content)
    return (
        normalize(result.get("signalName")),
        normalize(result.get("description")),
        normalize(result.get("reason")),
    )


def fill_requirement(requirement_path, case_path, seed_path, output_path, model, base_url, api_key, timeout, max_rows=None):
    workbook = load_workbook(requirement_path)
    sheet = workbook[workbook.sheetnames[0]]
    changed_fill = PatternFill("solid", fgColor="FFF2CC")
    case_style_context = load_case_style_context(case_path)
    seed_signal_map = load_seed_signal_map(seed_path)

    audit_rows = []
    row_limit = sheet.max_row if max_rows is None else min(sheet.max_row, max_rows + 1)

    for row in range(2, row_limit + 1):
        current = normalize(sheet.cell(row, 3).value)
        chinese_name = normalize(sheet.cell(row, 4).value)
        current_description = normalize(sheet.cell(row, 16).value)
        if not chinese_name:
            continue
        if current and current_description:
            continue
        seed_signal = seed_signal_map.get(chinese_name, "")
        if seed_signal and not current:
            sheet.cell(row, 3).value = seed_signal
            sheet.cell(row, 3).fill = changed_fill
            current = seed_signal
            wrote_seed = True
        else:
            wrote_seed = False
        if current and current_description:
            if wrote_seed:
                audit_rows.append((row, chinese_name, current, current_description, "seed", "seed workbook"))
            continue
        try:
            signal_name, description, reason = infer_signal_name(
                sheet, row, case_style_context, model, base_url, api_key, timeout
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            audit_rows.append((row, chinese_name, "", "", f"LLM error: {exc}", ""))
            continue
        wrote = False
        if not current and signal_name:
            sheet.cell(row, 3).value = signal_name
            sheet.cell(row, 3).fill = changed_fill
            wrote = True
        if not current_description and description:
            sheet.cell(row, 16).value = description
            sheet.cell(row, 16).fill = changed_fill
            wrote = True
        if wrote:
            audit_rows.append((row, chinese_name, signal_name or current, description, reason, "AI"))
        else:
            audit_rows.append((row, chinese_name, "", "", reason or "empty", ""))
        time.sleep(0.15)

    if "AI填充记录" in workbook.sheetnames:
        del workbook["AI填充记录"]
    audit = workbook.create_sheet("AI填充记录")
    audit.append(["需求行号", "Name In Chinese", "填入SignalName", "填入Description", "Reason", "Mode"])
    for item in audit_rows:
        audit.append(item)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    return audit_rows


def main():
    parser = argparse.ArgumentParser(description="Fill requirement workbook blanks with LLM only.")
    parser.add_argument("--requirement", default=default_requirement())
    parser.add_argument("--case", default=default_case())
    parser.add_argument("--seed", default=default_seed())
    parser.add_argument("--output", default=str(PROJECT_ROOT / "demo" / "需求1-1_AI填充.xlsx"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Please set OPENAI_API_KEY or pass --api-key.")

    audit_rows = fill_requirement(
        Path(args.requirement),
        Path(args.case),
        Path(args.seed),
        Path(args.output),
        args.model,
        args.base_url,
        args.api_key,
        args.timeout,
        args.max_rows,
    )

    filled = sum(1 for row in audit_rows if row[2] or row[3])
    print(f"Filled rows: {filled}")
    print(f"Output: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
