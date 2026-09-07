"""将单个或批量标准JSON转换为TAE .seq测试序列。"""

import argparse
import copy
import json
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generator import DynamicValueActivity  # noqa: E402
from testcase import *  # noqa: E402,F403
from utils import save_model  # noqa: E402


NUMBER_OPERATOR_MAP = {
    "GreaterThan": TYPENUMBEROPERATOR.GreaterThan,
    "GreaterThanOrEqual": TYPENUMBEROPERATOR.GreaterThanOrEqual,
    "Equal": TYPENUMBEROPERATOR.Equal,
    "NotEqual": TYPENUMBEROPERATOR.NotEqual,
    "LessThan": TYPENUMBEROPERATOR.LessThan,
    "LessThanOrEqual": TYPENUMBEROPERATOR.LessThanOrEqual,
}

STRING_OPERATOR_MAP = {
    "Equal": TYPESTRINGOPERATOR.Equal,
    "NotEqual": TYPESTRINGOPERATOR.NotEqual,
}

TIME_UNIT_MAP = {
    "ms": TYPETIMEUNIT.ms,
    "s": TYPETIMEUNIT.s,
    "min": TYPETIMEUNIT.min,
    "h": TYPETIMEUNIT.h,
}

ACCESS_MODE_MAP = {
    "PhysicalValue": TYPEACCESSMODE.PhysicalValue,
    "TextValue": TYPEACCESSMODE.TextValue,
    "RawValue": TYPEACCESSMODE.RawValue,
}


def sanitize_filename(value, limit=90):
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(value)).strip(" .")
    value = re.sub(r"\s+", "_", value)
    return (value or "unnamed")[:limit]


def expression_value(value, value_type):
    return repr(str(value)) if value_type == "String" else str(value)


def generate_write(step):
    value_type = step.get("valueType") or (
        "String" if step.get("accessMode") == "TextValue" else "Number"
    )
    write_obj = Write(
        sourceMapping=step["signal"],
        value=expression_value(step["value"], value_type),
    )
    write_obj.name = step.get("name", f"Write {step['signal']}")
    write_obj.describle = step.get("description", "")
    write_obj.accessMode = AccessMode(
        mode=ACCESS_MODE_MAP[step.get("accessMode", "PhysicalValue")]
    )
    return write_obj


def generate_wait(step):
    wait_obj = Wait(time=str(step["time"]), unit=step.get("unit", "ms"))
    wait_obj.name = step.get("name", "Wait")
    wait_obj.describle = step.get("description", "")
    return wait_obj


def offline_literal(step):
    value = step.get("offlineValue", 0)
    if step.get("expectType") == "String":
        return repr(str(value))
    return str(value)


def generate_read(step):
    read_obj = Read()
    read_obj.name = step.get("name", f"Read {step['signal']}")
    description = step.get("description", "")
    if "offlineValue" in step:
        description = f"@OFFLINE={offline_literal(step)}@ {description}".strip()
    read_obj.describle = description
    read_obj.sourceSignalItem = SignalItem(signal=step["signal"])
    read_obj.accessMode = AccessMode(
        mode=ACCESS_MODE_MAP[step.get("accessMode", "PhysicalValue")]
    )

    if not step.get("expectType") or "operator" not in step:
        return read_obj

    expectation = Expectation()
    if step["expectType"] == "String":
        if step["operator"] not in STRING_OPERATOR_MAP:
            raise ValueError(f"字符串断言不支持：{step['operator']}")
        expectation_mode = ExpectationModeString()
        expectation_mode.operator = STRING_OPERATOR_MAP[step["operator"]]
        expectation_mode.value = repr(str(step["expectValue"]))
        expectation.expectationType = TYPEEXPECTATIONINTERFACE.String
    else:
        expectation_mode = ExpectationModeNumeric()
        expectation_mode.operator = NUMBER_OPERATOR_MAP[step["operator"]]
        expectation_mode.value = str(step["expectValue"])
        expectation.expectationType = TYPEEXPECTATIONINTERFACE.Number
    expectation.expectationInterface = expectation_mode

    time_option = ExpectationTimeOption()
    time_option.mode = TYPETIMEOPTIONMODE.WaitUntilTrue
    time_option.timeout = str(step.get("timeout", "0"))
    time_option.timeoutUnit = TIME_UNIT_MAP[step.get("timeoutUnit", "ms")]
    read_obj.taeAssert = IsAssert(expectation=expectation, timeoption=time_option)
    return read_obj


def generate_power_action(step):
    function_name = {"POWERUP": "powerOn", "POWERDOWN": "powerOff"}[step["action"]]
    power_obj = DynamicValueActivity()
    power_obj.name = function_name
    power_obj.describle = "上下电框图占位，真实HiL平台接入后再启用"
    power_obj.toolType = "powerControl_EA"
    power_obj.toolName = "default"
    power_obj.deviceInterfaceName = "default"
    power_obj.functionName = function_name
    power_obj.skip = False
    return power_obj


def generate_placeholder(step):
    placeholder = ScriptBlock()
    placeholder.name = step.get("name", "Unsupported Action")
    placeholder.describle = step.get("description", "尚未映射到确定的TAE组件")
    placeholder.script = ""
    placeholder.skip = True
    return placeholder


ACTION_GENERATORS = {
    "Write": generate_write,
    "Wait": generate_wait,
    "Read": generate_read,
    "POWERUP": generate_power_action,
    "POWERDOWN": generate_power_action,
    "Placeholder": generate_placeholder,
}


def generate_action(step):
    action = step.get("action")
    if action not in ACTION_GENERATORS:
        return generate_placeholder({
            "name": str(action),
            "description": "JSON动作类型未被生成器支持",
        })
    return ACTION_GENERATORS[action](step)


def append_actions(group, steps):
    for step in steps:
        group.children.append(generate_action(step))


def generate_variable(variable_info):
    variable_type = variable_info.get("type", "NumberVariableValue")
    if variable_type == "NumberVariableValue":
        initial_value = NumberVariableValue(value=str(variable_info.get("value", 0)))
    elif variable_type == "StringVariableValue":
        initial_value = StringVariableValue(value=str(variable_info.get("value", "")))
    else:
        raise ValueError(f"暂不支持的变量类型：{variable_type}")
    return Variable(
        name=variable_info["name"],
        describle=variable_info.get("description", ""),
        initialValue=initial_value,
    )


def apply_offline_values(test_case):
    if not test_case.get("offlineMode", False):
        return
    variables = {item["name"]: item.get("value", 0) for item in test_case.get("variables", [])}
    for step in test_case.get("steps", []):
        if step.get("action") != "Read" or "offlineValue" in step:
            continue
        expected = step.get("expectValue", 0)
        step["offlineValue"] = variables.get(str(expected), expected)


def build_sequence(source_case):
    test_case = copy.deepcopy(source_case)
    apply_offline_values(test_case)

    process = Process()
    process.name = test_case["caseName"]
    process.describle = (
        f"来源：{test_case.get('source', {}).get('sheet', '')} "
        f"{test_case.get('source', {}).get('range', '')}"
    ).strip()
    process.startNode = StartNode()
    process.endNode = EndNode()
    process.activitySequence = ActivitySequence(name=test_case["caseName"])

    for variable_info in test_case.get("variables", []):
        process.activitySequence.variables.append(generate_variable(variable_info))

    initialization_group = Initialization(name="Initialization")
    test_step_group = Group(name="Test Step & Expected Result")
    cleanup_group = Cleanup(name="Clean Up", executeAfterAbortingTheTest=True)

    append_actions(initialization_group, test_case.get("initialization", []))
    append_actions(test_step_group, test_case.get("steps", []))
    append_actions(cleanup_group, test_case.get("cleanup", []))
    process.activitySequence.children.extend(
        [initialization_group, test_step_group, cleanup_group]
    )
    return process


def generate_sequence_file(test_case, output_path):
    save_model(build_sequence(test_case), str(output_path))


def load_cases(input_path):
    if input_path.is_file():
        return [(input_path, json.loads(input_path.read_text(encoding="utf-8")))]
    if not input_path.is_dir():
        raise FileNotFoundError(f"输入不存在：{input_path}")
    cases = []
    for path in sorted(input_path.glob("*.json")):
        if path.name == "manifest.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if "caseName" in data:
            cases.append((path, data))
    return cases


def batch_generate(input_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for source_path, case in load_cases(input_path):
        case_id = case.get("caseId", source_path.stem)
        filename = f"{sanitize_filename(case_id, 40)}_{sanitize_filename(case['caseName'])}.seq"
        output_path = output_dir / filename
        try:
            generate_sequence_file(case, output_path)
            results.append({
                "caseId": case_id,
                "caseName": case["caseName"],
                "status": "success",
                "sourceJson": str(source_path.resolve()),
                "sequence": str(output_path.resolve()),
                "warnings": case.get("warnings", []),
            })
        except Exception as exc:
            results.append({
                "caseId": case_id,
                "caseName": case.get("caseName", source_path.stem),
                "status": "failed",
                "sourceJson": str(source_path.resolve()),
                "error": str(exc),
            })

    manifest = {
        "total": len(results),
        "success": sum(item["status"] == "success" for item in results),
        "failed": sum(item["status"] == "failed" for item in results),
        "results": results,
    }
    (output_dir / "generation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description="单个或批量生成TAE测试序列")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(Path(__file__).with_name("generated_cases") / "json"),
        help="单个用例JSON或JSON目录",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).with_name("generated_cases") / "seq"),
    )
    args = parser.parse_args()

    manifest = batch_generate(Path(args.input), Path(args.output_dir))
    print(
        f"生成完成：总计{manifest['total']}，成功{manifest['success']}，"
        f"失败{manifest['failed']}"
    )
    print(f"输出目录：{Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
