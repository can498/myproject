import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mapping import *
from utils import save_model, load_model_root

# 修改为自己使用的工作空间路径
workspace_path = r"E:\\TAE\\map"
workspace_path
if __name__ == '__main__':

    # 创建一个mapping文件的框架， MappingFolder为根节点
    root_obj = MappingFolder()

    # 创建一个来自 HIL 设备的 Model类型mapping变量
    demo_model_mapping = ModelMapping()
    demo_model_mapping.name = "command_RPM"
    demo_model_mapping.deviceName = "HIL"
    demo_model_mapping.path = "Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM"
    demo_model_mapping.reference = ""
    demo_model_mapping.dataType = "VALUE"
    demo_model_mapping.enumeration = Enumeration()
    # 如果需要定义枚举值，在此属性下增加
    demo_model_mapping.enumeration.keyValue.append(EnumerationEntity(key="on", value="1"))
    demo_model_mapping.enumeration.keyValue.append(EnumerationEntity(key="off", value="0"))
    root_obj.mapping.append(demo_model_mapping)

    # 其他类型信号参考Model类型实现

    # 若需要增加文件夹以便分类
    folder1 = MappingFolder()
    folder1.name = "Engine"
    # folder1.mapping.append()
    root_obj.folder.append(folder1)

    map_path = "generate_demo.mapping"
    # 已封装好的函数，将python对象序列化为xml文件
    save_model(root_obj, map_path)



