import json
import sys
from pathlib import Path


# 允许直接执行 `python demo/generate_from_case.py`，也允许在 demo 目录中执行。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from testcase import (  # noqa: E402
    AccessMode,
    ActivitySequence,
    Cleanup,
    EndNode,
    Expectation,
    ExpectationModeNumeric,
    ExpectationTimeOption,
    Group,
    Initialization,
    IsAssert,
    Process,
    Read,
    SignalItem,
    StartNode,
    TYPEACCESSMODE,
    TYPEEXPECTATIONINTERFACE,
    TYPENUMBEROPERATOR,
    TYPETIMEOPTIONMODE,
    TYPETIMEUNIT,
    Wait,
)
from mapping import Enumeration, MappingFolder, ModelMapping  # noqa: E402
from utils.save_model import save_model  # noqa: E402


OPERATOR_MAP = {
    "GreaterThan": TYPENUMBEROPERATOR.GreaterThan,
    "GreaterThanOrEqual": TYPENUMBEROPERATOR.GreaterThanOrEqual,
    "Equal": TYPENUMBEROPERATOR.Equal,
    "LessThan": TYPENUMBEROPERATOR.LessThan,
    "LessThanOrEqual": TYPENUMBEROPERATOR.LessThanOrEqual,
}

TIME_UNIT_MAP = {
    "ms": TYPETIMEUNIT.ms,
    "s": TYPETIMEUNIT.s,
    "min": TYPETIMEUNIT.min,
    "h": TYPETIMEUNIT.h,
}


def build_wait(step):
    return Wait(time=str(step["time"]), unit=step.get("unit", "ms"))


def build_read(step):
    signal_name = step["signal"]

    read = Read()
    read.name = f"Read {signal_name}"
    read.sourceSignalItem = SignalItem(signal=signal_name)
    read.accessMode = AccessMode(mode=TYPEACCESSMODE.PhysicalValue)

    numeric = ExpectationModeNumeric()
    numeric.operator = OPERATOR_MAP[step["operator"]]
    numeric.value = str(step["expectValue"])

    expectation = Expectation()
    expectation.expectationType = TYPEEXPECTATIONINTERFACE.Number
    expectation.expectationInterface = numeric

    time_option = ExpectationTimeOption()
    time_option.mode = TYPETIMEOPTIONMODE.WaitUntilTrue
    time_option.timeout = str(step.get("timeout", "0"))
    time_option.timeoutUnit = TIME_UNIT_MAP[step.get("timeoutUnit", "ms")]

    assertion = IsAssert()
    assertion.expectation = expectation
    assertion.timeoption = time_option
    read.taeAssert = assertion
    return read


def build_action(step):
    builders = {
        "Wait": build_wait,
        "Read": build_read,
    }
    action = step.get("action")
    if action not in builders:
        raise ValueError(f"暂不支持的动作：{action}")
    return builders[action](step)


def build_process(test_case):
    process = Process()
    process.name = test_case["caseName"]
    process.startNode = StartNode()
    process.endNode = EndNode()
    process.activitySequence = ActivitySequence()

    initialization = Initialization(name="Initialization")
    test_steps = Group(name="Test Step & Expected Result")
    cleanup = Cleanup(name="Clean Up")

    for step in test_case["steps"]:
        test_steps.children.append(build_action(step))

    process.activitySequence.children.extend(
        [initialization, test_steps, cleanup]
    )
    return process


def build_mapping_file(test_case):
    """根据测试用例中的 mappings 字段创建独立的 TAE mapping 模型。"""
    root = MappingFolder(name="")
    model_folder = MappingFolder(name="Model")
    root.folder.append(model_folder)

    for item in test_case.get("mappings", []):
        mapping_type = item.get("type", "ModelMapping")
        if mapping_type != "ModelMapping":
            raise ValueError(f"暂不支持的 mapping 类型：{mapping_type}")

        model_mapping = ModelMapping()
        model_mapping.name = item["name"]
        model_mapping.deviceName = item["deviceName"]
        model_mapping.path = item["path"]
        model_mapping.description = item.get("description", "")
        model_mapping.reference = item.get("reference", "")
        model_mapping.dataType = item.get("dataType", "VALUE")
        model_mapping.enumeration = Enumeration()
        model_folder.mapping.append(model_mapping)

    return root


if __name__ == "__main__":
    input_path = Path(__file__).with_name("test_case_from_excel.json")
    with input_path.open(encoding="utf-8") as file:
        test_case = json.load(file)

    sequence_path = Path(__file__).with_name(f"{test_case['caseName']}.seq")
    mapping_path = Path(__file__).with_name(f"{test_case['caseName']}.mapping")

    process = build_process(test_case)
    mapping_root = build_mapping_file(test_case)

    save_model(process, str(sequence_path))
    save_model(mapping_root, str(mapping_path))
    print(f"序列生成成功：{sequence_path}")
    print(f"映射生成成功：{mapping_path}")
