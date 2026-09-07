"""仿照 generator_mapping.py，根据测试用例和信号目录生成TAE mapping文件。"""

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mapping import (  # noqa: E402
    Enumeration,
    EnumerationEntity,
    MappingFolder,
    ModelMapping,
)
from utils import save_model  # noqa: E402


def generate_mapping(mapping_info):
    mapping_type = mapping_info.get("type", "ModelMapping")
    if mapping_type != "ModelMapping":
        raise ValueError(f"暂不支持的 mapping 类型：{mapping_type}")

    mapping_obj = ModelMapping()
    mapping_obj.name = mapping_info["name"]
    mapping_obj.deviceName = mapping_info["deviceName"]
    mapping_obj.path = mapping_info["path"]
    mapping_obj.description = mapping_info.get("description", "")
    mapping_obj.reference = mapping_info.get("reference", "")
    mapping_obj.dataType = mapping_info.get("dataType", "VALUE")
    mapping_obj.enumeration = Enumeration()
    for key, value in mapping_info.get("enumerations", {}).items():
        mapping_obj.enumeration.keyValue.append(
            EnumerationEntity(key=str(key), value=str(value))
        )
    return mapping_obj


def resolve_mappings(test_case, mapping_catalog=None):
    if test_case.get("mappings"):
        return test_case["mappings"]

    if mapping_catalog is None:
        required = ", ".join(test_case.get("requiredMappings", []))
        raise ValueError(
            "测试用例没有真实Mapping信息。请通过--catalog提供真实信号目录。"
            f" 当前需要：{required}"
        )

    catalog_by_name = {
        item["name"]: item for item in mapping_catalog.get("mappings", [])
    }
    missing = [
        name
        for name in test_case.get("requiredMappings", [])
        if name not in catalog_by_name
    ]
    if missing:
        raise ValueError(f"信号目录缺少Mapping：{', '.join(missing)}")
    return [catalog_by_name[name] for name in test_case.get("requiredMappings", [])]


def build_mapping(test_case, mapping_catalog):
    root_obj = MappingFolder(name="")
    model_folder = MappingFolder(name="Model")
    root_obj.folder.append(model_folder)

    for mapping_info in resolve_mappings(test_case, mapping_catalog):
        model_folder.mapping.append(generate_mapping(mapping_info))

    return root_obj


def generate_mapping_file(test_case, mapping_catalog, output_path):
    save_model(build_mapping(test_case, mapping_catalog), str(output_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据测试用例生成TAE Mapping")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(Path(__file__).with_name("test_case_from_excel.json")),
    )
    parser.add_argument(
        "--catalog",
        help="真实信号Mapping目录JSON；测试用例已内含mappings时可省略",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open(encoding="utf-8") as file:
        case = json.load(file)

    catalog = None
    if args.catalog:
        with Path(args.catalog).open(encoding="utf-8") as file:
            catalog = json.load(file)

    output_path = (
        Path(args.output)
        if args.output
        else Path(__file__).with_name(f"{case['caseName']}.mapping")
    )
    generate_mapping_file(case, catalog, output_path)
    print(f"映射生成成功：{output_path.resolve()}")
