
from .testcase import getEClassifier, eClassifiers
from .testcase import name, nsURI, nsPrefix, eClass
from .testcase import Process, Activity, ActivitySequence, IndirectActivity, DirectActivity, ActivityList, Group, TestCase, PythonSequence, Wait, For, Loop, BreakCondition, While, DoWhile, If, ElseIf, Then, Else, Case, Switch, Default, Break, Return, Exit, Continue, Try, Except, Finally, Condition, Write, CallSequence, StartCapture, StopCapture, AddCaptureToReport, Chart, CAPTURETYPE, Variable, VariableValue, NumberVariableValue, StringVariableValue, PythonObjectVariableValue, EnumVariableValue, EnumEntity, FunctionVariableValue, Exec, Compute, IsSave, TESTON, ScriptBlock, VariableContiner, DataStructure, Element, CaptureGroup, SignalItem, ChartGroup, Capture, CAPTURETRIGGER, ModelCapture, McCapture, EESConnect, EESDeConnect, EESConfig, EESActivateAll, EESDeActivateAll, EESMappingChannel, ERRORTYPE, TIMEOPTION, POTENTIAL, CtcGeneratorScript, StartNode, EndNode, AccessMode, Read, IsAssert, Expectation, ExpectationInterface, ExpectationModeNumeric, ExpectationModeString, ExpectationModePythonExpression, ExpectationTimeOption, TYPEACCESSMODE, TYPEEXPECTATIONINTERFACE, TYPENUMBEROPERATOR, TYPENUMBERTOLERANCE, TYPESTRINGOPERATOR, TYPETIMEOPTIONMODE, TYPETIMEUNIT, Dialog, ChoiceDialog, InputDialog, ConfirmDialog, CONFIRMTYPE, CONFIRMDEFAULTVALUE, Initialization, Cleanup, WriteSignalGroup, ReadSignalGroup, ReadDataByIdentifier, DidSaveAndAssert, WriteDataByIdentifier, ClearDTC, CallService, ReadDTCInformation, DTCObject, NegativeResponse, OptionRecord, StatusRecord, RoutineControl, MultiRead, TYPEPASSWHENMODE, SeqTag, Signal, DataAnalysesRef, SignalVariableContainer, SubData, StartStimulus, SignalStimulus, StopStimulus, StimulusBinding, StimulusParameter, Evaluate, BaseSegmentType, ExpSegmentType, ConstSegmentType, IdleSegmentType, NoiseSegmentType, PulseSegmentType, RampSegmentType, RampSlopeSegmentType, SawSegmentType, SineSegmentType, ExpectationModeArray, ArrayMember, DTCStatusCodeSaveAndAssert, NumberOfIdentifierSaveAndAssert, DID, AudioCapture, ExpectationMcArray, BaseCapture, EthReadInput, EthReadOutput, EthCallMethod, EthReadVariable, EthInputVariable

from ctc import Ctc
from mapping import Mapping

from . import testcase

__all__ = ['Process', 'Activity', 'ActivitySequence', 'IndirectActivity', 'DirectActivity', 'ActivityList', 'Group', 'TestCase', 'PythonSequence', 'Wait', 'For', 'Loop', 'BreakCondition', 'While', 'DoWhile', 'If', 'ElseIf', 'Then', 'Else', 'Case', 'Switch', 'Default', 'Break', 'Return', 'Exit', 'Continue', 'Try', 'Except', 'Finally', 'Condition', 'Write', 'CallSequence', 'StartCapture', 'StopCapture', 'AddCaptureToReport', 'Chart', 'CAPTURETYPE', 'Variable', 'VariableValue', 'NumberVariableValue', 'StringVariableValue', 'PythonObjectVariableValue', 'EnumVariableValue', 'EnumEntity', 'FunctionVariableValue', 'Exec', 'Compute', 'IsSave', 'TESTON', 'ScriptBlock', 'VariableContiner', 'DataStructure', 'Element', 'CaptureGroup', 'SignalItem', 'ChartGroup', 'Capture', 'CAPTURETRIGGER', 'ModelCapture', 'McCapture', 'EESConnect', 'EESDeConnect', 'EESConfig', 'EESActivateAll', 'EESDeActivateAll', 'EESMappingChannel', 'ERRORTYPE', 'TIMEOPTION', 'POTENTIAL', 'CtcGeneratorScript', 'StartNode', 'EndNode', 'AccessMode', 'Read', 'IsAssert', 'Expectation', 'ExpectationInterface', 'ExpectationModeNumeric', 'ExpectationModeString', 'ExpectationModePythonExpression', 'ExpectationTimeOption',
           'TYPEACCESSMODE', 'TYPEEXPECTATIONINTERFACE', 'TYPENUMBEROPERATOR', 'TYPENUMBERTOLERANCE', 'TYPESTRINGOPERATOR', 'TYPETIMEOPTIONMODE', 'TYPETIMEUNIT', 'Dialog', 'ChoiceDialog', 'InputDialog', 'ConfirmDialog', 'CONFIRMTYPE', 'CONFIRMDEFAULTVALUE', 'Initialization', 'Cleanup', 'WriteSignalGroup', 'ReadSignalGroup', 'ReadDataByIdentifier', 'DidSaveAndAssert', 'WriteDataByIdentifier', 'ClearDTC', 'CallService', 'ReadDTCInformation', 'DTCObject', 'NegativeResponse', 'OptionRecord', 'StatusRecord', 'RoutineControl', 'MultiRead', 'TYPEPASSWHENMODE', 'SeqTag', 'Signal', 'DataAnalysesRef', 'SignalVariableContainer', 'SubData', 'StartStimulus', 'SignalStimulus', 'StopStimulus', 'StimulusBinding', 'StimulusParameter', 'Evaluate', 'BaseSegmentType', 'ExpSegmentType', 'ConstSegmentType', 'IdleSegmentType', 'NoiseSegmentType', 'PulseSegmentType', 'RampSegmentType', 'RampSlopeSegmentType', 'SawSegmentType', 'SineSegmentType', 'ExpectationModeArray', 'ArrayMember', 'DTCStatusCodeSaveAndAssert', 'NumberOfIdentifierSaveAndAssert', 'DID', 'AudioCapture', 'ExpectationMcArray', 'BaseCapture', 'EthReadInput', 'EthReadOutput', 'EthCallMethod', 'EthReadVariable', 'EthInputVariable']

eSubpackages = []
eSuperPackage = None
testcase.eSubpackages = eSubpackages
testcase.eSuperPackage = eSuperPackage

Process.startNode.eType = StartNode
Process.endNode.eType = EndNode
Process.activitySequence.eType = ActivitySequence
Activity.tagList.eType = SeqTag
ActivitySequence.captureGroup.eType = CaptureGroup
ActivitySequence.ctcGeneratorScript.eType = CtcGeneratorScript
ActivitySequence.ctc.eType = Ctc
IndirectActivity.directactivity.eType = DirectActivity
ActivityList.children.eType = DirectActivity
If.then.eType = Then
If.elseif.eType = ElseIf
If.taeElse.eType = Else
Switch.taeCase.eType = Case
Switch.taeDefault.eType = Default
Try.taeExcept.eType = Except
Try.taeFinally.eType = Finally
Write.accessMode.eType = AccessMode
AddCaptureToReport.plots.eType = Chart
Variable.initialValue.eType = VariableValue
EnumVariableValue.entity.eType = EnumEntity
Exec.variables.eType = Variable
Exec.mapping.eType = Mapping
Compute.taeAssert.eType = IsAssert
VariableContiner.variables.eType = Variable
VariableContiner.mappingItems.eType = Mapping
DataStructure.attribute.eType = Element
CaptureGroup.captures.eType = Capture
CaptureGroup.chartGroup.eType = ChartGroup
ChartGroup.chart.eType = Chart
Capture.signals.eType = SignalItem
EESConfig.channel.eType = EESMappingChannel
Read.sourceSignalItem.eType = SignalItem
Read.accessMode.eType = AccessMode
Read.taeAssert.eType = IsAssert
IsAssert.expectation.eType = Expectation
IsAssert.timeoption.eType = ExpectationTimeOption
Expectation.expectationInterface.eType = ExpectationInterface
WriteSignalGroup.existWrite.eType = Write
ReadSignalGroup.existRead.eType = Read
ReadDataByIdentifier.didSaveAndAssertList.eType = DidSaveAndAssert
DidSaveAndAssert.taeAssert.eType = IsAssert
WriteDataByIdentifier.subDataList.eType = SubData
ClearDTC.taeAssert.eType = IsAssert
CallService.taeAssert.eType = IsAssert
ReadDTCInformation.expectList.eType = DTCObject
ReadDTCInformation.notExpectList.eType = DTCObject
ReadDTCInformation.dtc.eType = DTCObject
DTCObject.statusCodeSaveAndAssert.eType = DTCStatusCodeSaveAndAssert
DTCObject.numberOfIdentifierSaveAndAssert.eType = NumberOfIdentifierSaveAndAssert
DTCObject.snapshotRecord.eType = DID
StatusRecord.taeAssert.eType = IsAssert
RoutineControl.optionRecordList.eType = OptionRecord
RoutineControl.statusRecordList.eType = StatusRecord
MultiRead.signalList.eType = DirectActivity
MultiRead.timeOption.eType = ExpectationTimeOption
SignalVariableContainer.variables.eType = Variable
SignalVariableContainer.signalItems.eType = Signal
StartStimulus.targetSignal.eType = StimulusBinding
StartStimulus.parameter.eType = StimulusParameter
SignalStimulus.stimulusationDescription.eType = BaseSegmentType
ExpectationModeArray.member.eType = ArrayMember
ArrayMember.taeAssert.eType = IsAssert
DTCStatusCodeSaveAndAssert.taeAssert.eType = IsAssert
NumberOfIdentifierSaveAndAssert.taeAssert.eType = IsAssert
DID.didSaveAndAssert.eType = DidSaveAndAssert
ExpectationMcArray.member.eType = ArrayMember
EthReadInput.resultValue.eType = EthReadVariable
EthReadInput.timeOption.eType = ExpectationTimeOption
EthReadOutput.resultValue.eType = EthReadVariable
EthReadOutput.timeOption.eType = ExpectationTimeOption
EthCallMethod.inputValue.eType = EthInputVariable
EthCallMethod.returnValue.eType = EthReadVariable
EthCallMethod.timeOption.eType = ExpectationTimeOption
EthReadVariable.expect.eType = Expectation

otherClassifiers = [CAPTURETYPE, TESTON, CAPTURETRIGGER, ERRORTYPE, TIMEOPTION, POTENTIAL, TYPEACCESSMODE, TYPEEXPECTATIONINTERFACE,
                    TYPENUMBEROPERATOR, TYPENUMBERTOLERANCE, TYPESTRINGOPERATOR, TYPETIMEOPTIONMODE, TYPETIMEUNIT, CONFIRMTYPE, CONFIRMDEFAULTVALUE, TYPEPASSWHENMODE]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
