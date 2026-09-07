import sys
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generator import DynamicValueActivity, FieldModel, SaveAndAssertFieldModel
from mapping import *
from testcase import *
from utils import save_model, load_model_root

# 修改为自己使用的工作空间路径
workspace_path = r"E:\\TAE\\Test"

def generate_mapping(mapping_info):
    # 只实现Model类Mapping的示例，其他类型参考此实现方式
    mapping_obj = None
    mapping_type = mapping_info.get("type")
    if  mapping_type== "ModelMapping":
        mapping_obj = ModelMapping()
    elif mapping_type == "MeasurementMapping":
        pass
    else:
        pass
    mapping_obj.name = mapping_info.get("name")
    mapping_obj.deviceName = mapping_info.get("deviceName")
    mapping_obj.path = mapping_info.get("path")
    mapping_obj.dataType = mapping_info.get("dataType")
    return mapping_obj

def generate_variable(variable_info):
    # 只实现Number类Variable的示例，其他类型参考此实现方式
    variable_obj = Variable()
    variable_type = variable_info.get("type")
    if  variable_type== "NumberVariableValue":
        variable_obj.initialValue = NumberVariableValue()
        variable_obj.initialValue.value = variable_info.get("value")
    elif variable_type == "StringVariableValue":
        pass
    else:
        pass
    variable_obj.name = variable_info.get("name")
    variable_obj.describle = variable_info.get("desc")
    return variable_obj

# scriptblock的代码示例，作用是借助api读写全局变量
API_OPTION_STR = """
import api
print(api.getVariable("aaa"))
print(api.getVariable(["aaa","bbb"]))

api.setVariable("aaa", 1)
print(api.getVariable("aaa"))

api.setVariable({"aaa": 2, "bbb":22})
print(api.getVariable(["aaa","bbb"]))
"""

if __name__ == '__main__':

    # 创建一个序列文件的框架， Process为根节点
    process = Process()
    process.startNode = StartNode()
    process.endNode = EndNode()
    process.activitySequence = ActivitySequence()
    initialization_group = Initialization()
    initialization_group.name = "Initialization"
    cleanup_group  = Cleanup()
    cleanup_group.name  = "Clean Up"
    test_step_group = Group()
    test_step_group.name = "Test Step & Expected Result"
    # 按顺序添加，保证第一个为初始化框，中间是测试步骤框，最后一个为复位框
    process.activitySequence.children.append(initialization_group)
    process.activitySequence.children.append(test_step_group)
    process.activitySequence.children.append(cleanup_group)
    # 序列本地mapping的信息
    mapping_list = [
        {
            "type": "ModelMapping",
            "name": "a",
            "deviceName": "HIL",
            "path": "param/a",
            "dataType": "VALUE"
        },
        {
            "type": "ModelMapping",
            "name": "b",
            "deviceName": "HIL",
            "path": "param/b",
            "dataType": "VALUE"
        }
    ]
    for info in mapping_list:
        # 遍历mapping信息，添加到序列外层的本地mapping容器中
        process.activitySequence.mappingItems.append(generate_mapping(info))

    # 本地定义的variable信息
    variable_list = [
        {
            "name": "variable",
            "desc": "变量的描述信息",
            "type": "NumberVariableValue",
            "value": "0",
        }
    ]
    for info in variable_list:
        # 遍历variable信息，添加到序列外层的本地variable容器中
        process.activitySequence.variables.append(generate_variable(info))

    # Write a=2
    write_a_2 = Write(sourceMapping="a",value="2")
    # AccessMode代表操作模式，可选PhysicalValue，TextValue，RawValue
    access_mode = AccessMode()
    access_mode.mode = TYPEACCESSMODE.PhysicalValue
    write_a_2.accessMode = access_mode
    initialization_group.children.append(write_a_2)

    # Write a=0
    write_a_0 = Write(sourceMapping="a", value="0")
    access_mode = AccessMode()
    access_mode.mode = TYPEACCESSMODE.PhysicalValue
    write_a_0.accessMode = access_mode
    cleanup_group.children.append(write_a_0)

    # Wait 3 s
    wait_3 = Wait(time="3", unit="s")

    # Compute variable<=1
    compute_variable = Compute()
    compute_variable.expression = "variable"
    compute_variable.taeAssert = IsAssert()
    compute_variable.taeAssert.expectation = Expectation()
    # 此处断言类型有多种，参照 ExpectationInterface 的子类
    compute_variable.taeAssert.expectation.expectationInterface = ExpectationModeNumeric()
    compute_variable.taeAssert.expectation.expectationInterface.operator = TYPENUMBEROPERATOR.LessThanOrEqual
    compute_variable.taeAssert.expectation.expectationInterface.value = "1"
    compute_variable.taeAssert.timeoption = ExpectationTimeOption()

    # ScriptBlock 脚本调用
    scriptBlock = ScriptBlock()
    scriptBlock.name = "API Read Write"
    scriptBlock.script = API_OPTION_STR

    # Read a 并判断在5s内，等于2
    read_a_with_time_option = Read()
    access_mode = AccessMode()
    access_mode.mode = TYPEACCESSMODE.PhysicalValue
    read_a_with_time_option.accessMode = access_mode
    temp_SignalItem = SignalItem()
    temp_SignalItem.signal = "a"
    read_a_with_time_option.sourceSignalItem = temp_SignalItem
    temp = Expectation()
    temp.expectationType = TYPEEXPECTATIONINTERFACE.Number
    temp_expectation = ExpectationModeNumeric()
    temp_expectation.operator = TYPENUMBEROPERATOR.Equal
    temp_expectation.value = "2"
    temp.expectationInterface = temp_expectation
    temp_time_option = ExpectationTimeOption()
    temp_time_option.mode = TYPETIMEOPTIONMODE.WaitUntilTrue
    temp_time_option.timeout = "5"
    temp_time_option.timeoutUnit = TYPETIMEUNIT.s
    temp_time_option.timeout = "5"
    temp_time_option.timeout = "5"
    temp_taeAssert = IsAssert()
    temp_taeAssert.expectation = temp
    temp_taeAssert.timeoption = temp_time_option
    read_a_with_time_option.taeAssert = temp_taeAssert

    # IF 类型，判断variable != 0 时， wait 100ms， 否则wait 200ms
    if_obj = If()
    if_obj.name = "If-Else判断"
    if_obj.condition = "variable != 0"
    then_obj = Then()
    then_obj.directactivity.append(Wait(time="100", unit="ms"))
    else_obj = Else()
    else_obj.directactivity.append(Wait(time="200", unit="ms"))
    if_obj.then = then_obj
    if_obj.taeElse = else_obj

    # # 调用Clib，此clib涉及参数传入
    # clib_path = r"\library\1231321.clib"
    # clib_obj = CallSequence()
    # clib_obj.name = "调clib带入参"
    # clib_obj.seqPath = clib_path
    # # load_model_root 是已封装好的函数，将xml文件反序列为python对象
    # clib_temp = load_model_root(fr"{workspace_path}{clib_path}")
    # clib_obj.variables.extend([i for i in clib_temp.activitySequence.variables if i.input is True])
    # clib_obj.mappingItems.extend(clib_temp.activitySequence.mappingItems)
    # # set clib的变量初始值为11，reference为variable
    # set_variable = {"lib_variable": "11"}
    # for i in clib_obj.variables:
    #     if i.name == "lib_variable":
    #         i.initialReference = "variable"
    #         i.initialValue.value = "11"
    #         break

    # 调用工具的JOB控件,
    job_demo = DynamicValueActivity()
    job_demo.name = "调用工具的JOB"
    job_demo.toolType = "VBASoft"
    job_demo.toolName = "default"
    job_demo.deviceInterfaceName = "default"
    job_demo.functionName = "readMessage"
    job_demo.inputField.append(FieldModel(attrName="networkName",attrValue="'CAN1'"))
    job_demo.inputField.append(FieldModel(attrName="MsgId",attrValue="0x4C1"))
    job_demo.inputField.append(FieldModel(attrName="msgType",attrValue="1"))
    job_demo.outputField.append(SaveAndAssertFieldModel(attrName="value", save=IsSave(), taeAssert=IsAssert()))
    # 设置控件效果为跳过
    job_demo.skip = True

    # Capture a,b 两个信号
    captureGroup = CaptureGroup()
    capture_name = "CaptureDemo"
    baseCapture = BaseCapture()
    baseCapture.captureName = capture_name
    baseCapture.captureId = str(uuid4())

    for info in mapping_list:
        signal = SignalItem()
        signal.signal = info.get("name")
        signal.signalType = info.get("type")
        baseCapture.signals.append(signal)

    captureGroup.captures.append(baseCapture)
    chartGroup = ChartGroup()
    chartGroup.refId = baseCapture.captureId
    captureGroup.chartGroup.append(chartGroup)
    process.activitySequence.captureGroup = captureGroup

    startCapture = StartCapture()
    startCapture.name = 'Start Capture'
    startCapture.captureName = capture_name

    stopCapture = StopCapture()
    stopCapture.name = 'Stop Capture'
    stopCapture.captureName = capture_name

    addCaptureToReport = AddCaptureToReport()
    addCaptureToReport.name = 'Add Capture To Report'
    addCaptureToReport.captureName = capture_name
    addCaptureToReport.title = 'demo title'
    plots = Chart()
    plots.xLabel = "time(s)"
    for info in mapping_list:
        plots.items.append(f'{info.get("name")}')
    addCaptureToReport.plots.append(plots)

    # 按照逻辑将每个控件进行添加
    test_step_group.children.append(startCapture)
    test_step_group.children.append(wait_3)
    test_step_group.children.append(compute_variable)
    test_step_group.children.append(scriptBlock)
    test_step_group.children.append(read_a_with_time_option)
    test_step_group.children.append(if_obj)
    test_step_group.children.append(stopCapture)
    test_step_group.children.append(addCaptureToReport)
    # 不使用 clib，因此不向测试步骤中添加 CallSequence。
    # test_step_group.children.append(clib_obj)
    test_step_group.children.append(job_demo)

    seq_path = "generate_demo.seq"
    # 已封装好的函数，将python对象序列化为xml文件
    save_model(process, seq_path)



