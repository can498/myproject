"""Definition of meta model 'testcase'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from mapping import DataType


name = 'testcase'
nsURI = 'com.hirain.tae.model.testcase'
nsPrefix = 'tae'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
CAPTURETYPE = EEnum('CAPTURETYPE', literals=['Model', 'ECU', 'Audio', 'Base', 'Auto'])

TESTON = EEnum('TESTON', literals=['error', 'errorOrFailed', 'Inconclusive'])

CAPTURETRIGGER = EEnum('CAPTURETRIGGER', literals=['AutoStartAndEnd', 'AutoStep', 'Manually'])

ERRORTYPE = EEnum('ERRORTYPE', literals=['Null', 'Resistor'])

TIMEOPTION = EEnum('TIMEOPTION', literals=['Static', 'Duration', 'LooseContact'])

POTENTIAL = EEnum('POTENTIAL', literals=['Normal', 'OC', 'ToVBAT', 'ToGND', 'ToCOM', 'Other'])

TYPEACCESSMODE = EEnum('TYPEACCESSMODE', literals=['PhysicalValue', 'TextValue', 'RawValue'])

TYPEEXPECTATIONINTERFACE = EEnum('TYPEEXPECTATIONINTERFACE', literals=[
                                 'Number', 'String', 'PythonExpression', 'Null', 'Array', 'Boolean', 'Enum', 'McArray'])

TYPENUMBEROPERATOR = EEnum('TYPENUMBEROPERATOR', literals=[
                           'LessThan', 'LessThanOrEqual', 'GreaterThan', 'GreaterThanOrEqual', 'Equal', 'NotEqual'])

TYPENUMBERTOLERANCE = EEnum('TYPENUMBERTOLERANCE', literals=[
                            'Null', 'Absolute', 'Percentage', 'Fractional'])

TYPESTRINGOPERATOR = EEnum('TYPESTRINGOPERATOR', literals=[
                           'Equal', 'NotEqual', 'StartWith', 'EndWith', 'Contain', 'NotContain', 'ContainedIn'])

TYPETIMEOPTIONMODE = EEnum('TYPETIMEOPTIONMODE', literals=[
                           'Null', 'WaitUntilTrue', 'TrueInDuration', 'WaitUntilTrueNotAssert'])

TYPETIMEUNIT = EEnum('TYPETIMEUNIT', literals=['ms', 's', 'min', 'h'])

CONFIRMTYPE = EEnum('CONFIRMTYPE', literals=['Information', 'Waring', 'Question'])

CONFIRMDEFAULTVALUE = EEnum('CONFIRMDEFAULTVALUE', literals=[
                            'Success', 'Failed', 'Undefined', 'Error'])

TYPEPASSWHENMODE = EEnum('TYPEPASSWHENMODE', literals=['AllStep', 'OneOf'])


@abstract
class Activity(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    describle = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    skip = EAttribute(eType=EBoolean, derived=False, changeable=True)
    genReport = EAttribute(eType=EBoolean, derived=False, changeable=True)
    debug = EAttribute(eType=EBoolean, derived=False, changeable=True)
    mask = EAttribute(eType=EBoolean, derived=False, changeable=True)
    collapsed = EAttribute(eType=EBoolean, derived=False, changeable=True)
    tagList = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, describle=None, skip=None, genReport=None, tagList=None, debug=None, mask=None, collapsed=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if describle is not None:
            self.describle = describle

        if skip is not None:
            self.skip = skip

        if genReport is not None:
            self.genReport = genReport

        if debug is not None:
            self.debug = debug

        if mask is not None:
            self.mask = mask

        if collapsed is not None:
            self.collapsed = collapsed

        if tagList:
            self.tagList.extend(tagList)


class TestCase(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class PythonSequence(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class BreakCondition(EObject, metaclass=MetaEClass):

    taeBreak = EAttribute(eType=EBoolean, derived=False, changeable=True)
    breakContent = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, taeBreak=None, breakContent=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if taeBreak is not None:
            self.taeBreak = taeBreak

        if breakContent is not None:
            self.breakContent = breakContent


class Chart(EObject, metaclass=MetaEClass):

    xLabel = EAttribute(eType=EString, derived=False, changeable=True, default_value='time(ms)')
    yLabel = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='plot')
    items = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)

    def __init__(self, *, xLabel=None, yLabel=None, name=None, items=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if xLabel is not None:
            self.xLabel = xLabel

        if yLabel is not None:
            self.yLabel = yLabel

        if name is not None:
            self.name = name

        if items:
            self.items.extend(items)


class Variable(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    input = EAttribute(eType=EBoolean, derived=False, changeable=True)
    output = EAttribute(eType=EBoolean, derived=False, changeable=True)
    initialReference = EAttribute(eType=EString, derived=False, changeable=True)
    describle = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    initialValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, name=None, initialValue=None, input=None, output=None, initialReference=None, describle=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if input is not None:
            self.input = input

        if output is not None:
            self.output = output

        if initialReference is not None:
            self.initialReference = initialReference

        if describle is not None:
            self.describle = describle

        if initialValue is not None:
            self.initialValue = initialValue


@abstract
class VariableValue(EObject, metaclass=MetaEClass):

    value = EAttribute(eType=EString, derived=False, changeable=True, default_value='0')

    def __init__(self, *, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if value is not None:
            self.value = value


class EnumEntity(EObject, metaclass=MetaEClass):

    key = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    value = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


class IsSave(EObject, metaclass=MetaEClass):

    save = EAttribute(eType=EBoolean, derived=False, changeable=True)
    savedvar = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, save=None, savedvar=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if save is not None:
            self.save = save

        if savedvar is not None:
            self.savedvar = savedvar

    def saveValidate(self, chain=None, context=None):

        raise NotImplementedError('operation saveValidate(...) not yet implemented')


class VariableContiner(EObject, metaclass=MetaEClass):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    mappingItems = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, variables=None, mappingItems=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if variables:
            self.variables.extend(variables)

        if mappingItems:
            self.mappingItems.extend(mappingItems)


class DataStructure(EObject, metaclass=MetaEClass):

    xAxis = EAttribute(eType=EInt, derived=False, changeable=True)
    yAxis = EAttribute(eType=EInt, derived=False, changeable=True)
    json = EAttribute(eType=EString, derived=False, changeable=True)
    attribute = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, xAxis=None, yAxis=None, attribute=None, json=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if xAxis is not None:
            self.xAxis = xAxis

        if yAxis is not None:
            self.yAxis = yAxis

        if json is not None:
            self.json = json

        if attribute:
            self.attribute.extend(attribute)


class Element(EObject, metaclass=MetaEClass):

    x = EAttribute(eType=EInt, derived=False, changeable=True)
    y = EAttribute(eType=EInt, derived=False, changeable=True)
    type = EAttribute(eType=EString, derived=False, changeable=True)
    relattion = EAttribute(eType=EString, derived=False, changeable=True)
    content = EAttribute(eType=EString, derived=False, changeable=True)
    tolerange = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, x=None, y=None, type=None, relattion=None, content=None, tolerange=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if type is not None:
            self.type = type

        if relattion is not None:
            self.relattion = relattion

        if content is not None:
            self.content = content

        if tolerange is not None:
            self.tolerange = tolerange


class CaptureGroup(EObject, metaclass=MetaEClass):

    captures = EReference(ordered=True, unique=True, containment=True, upper=-1)
    chartGroup = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, captures=None, chartGroup=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if captures:
            self.captures.extend(captures)

        if chartGroup:
            self.chartGroup.extend(chartGroup)


class SignalItem(EObject, metaclass=MetaEClass):

    signal = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    raster = EAttribute(eType=EString, derived=False, changeable=True)
    signalType = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, signal=None, raster=None, signalType=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if signal is not None:
            self.signal = signal

        if raster is not None:
            self.raster = raster

        if signalType is not None:
            self.signalType = signalType


class ChartGroup(EObject, metaclass=MetaEClass):

    refId = EAttribute(eType=EString, derived=False, changeable=True)
    chart = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, refId=None, chart=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if refId is not None:
            self.refId = refId

        if chart:
            self.chart.extend(chart)


class Capture(EObject, metaclass=MetaEClass):

    captureName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    describle = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    captureId = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    trigger = EAttribute(eType=CAPTURETRIGGER, derived=False, changeable=True)
    signals = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, captureName=None, signals=None, describle=None, captureId=None, trigger=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if captureName is not None:
            self.captureName = captureName

        if describle is not None:
            self.describle = describle

        if captureId is not None:
            self.captureId = captureId

        if trigger is not None:
            self.trigger = trigger

        if signals:
            self.signals.extend(signals)


class EESMappingChannel(EObject, metaclass=MetaEClass):

    withload = EAttribute(eType=EBoolean, derived=False, changeable=True)
    items = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, withload=None, items=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if withload is not None:
            self.withload = withload

        if items is not None:
            self.items = items


class CtcGeneratorScript(EObject, metaclass=MetaEClass):

    script = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, script=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if script is not None:
            self.script = script


class StartNode(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class EndNode(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class AccessMode(EObject, metaclass=MetaEClass):

    mode = EAttribute(eType=TYPEACCESSMODE, derived=False, changeable=True)

    def __init__(self, *, mode=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if mode is not None:
            self.mode = mode


class IsAssert(EObject, metaclass=MetaEClass):

    taeAssert = EAttribute(eType=EBoolean, derived=False, changeable=True)
    expectation = EReference(ordered=True, unique=True, containment=True)
    timeoption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, taeAssert=None, expectation=None, timeoption=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if taeAssert is not None:
            self.taeAssert = taeAssert

        if expectation is not None:
            self.expectation = expectation

        if timeoption is not None:
            self.timeoption = timeoption

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class Expectation(EObject, metaclass=MetaEClass):

    expectationType = EAttribute(eType=TYPEEXPECTATIONINTERFACE, derived=False, changeable=True)
    expectationInterface = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, expectationType=None, expectationInterface=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if expectationType is not None:
            self.expectationType = expectationType

        if expectationInterface is not None:
            self.expectationInterface = expectationInterface


@abstract
class ExpectationInterface(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class NegativeResponse(EObject, metaclass=MetaEClass):

    isNegative = EAttribute(eType=EBoolean, derived=False, changeable=True)
    negativeCode = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, isNegative=None, negativeCode=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if isNegative is not None:
            self.isNegative = isNegative

        if negativeCode is not None:
            self.negativeCode = negativeCode


class OptionRecord(EObject, metaclass=MetaEClass):

    optionName = EAttribute(eType=EString, derived=False, changeable=True)
    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)
    effectiveRange = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, optionName=None, dataType=None, value=None, effectiveRange=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if optionName is not None:
            self.optionName = optionName

        if dataType is not None:
            self.dataType = dataType

        if value is not None:
            self.value = value

        if effectiveRange is not None:
            self.effectiveRange = effectiveRange


class SeqTag(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Signal(EObject, metaclass=MetaEClass):

    input = EAttribute(eType=EBoolean, derived=False, changeable=True)
    output = EAttribute(eType=EBoolean, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    targetSignal = EAttribute(eType=EString, derived=False, changeable=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, input=None, output=None, name=None, targetSignal=None, description=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if input is not None:
            self.input = input

        if output is not None:
            self.output = output

        if name is not None:
            self.name = name

        if targetSignal is not None:
            self.targetSignal = targetSignal

        if description is not None:
            self.description = description


class SignalVariableContainer(EObject, metaclass=MetaEClass):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    signalItems = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, variables=None, signalItems=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if variables:
            self.variables.extend(variables)

        if signalItems:
            self.signalItems.extend(signalItems)


class SubData(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    physicalvalue = EAttribute(eType=EString, derived=False, changeable=True)
    unit = EAttribute(eType=EString, derived=False, changeable=True)
    options = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, physicalvalue=None, unit=None, options=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if physicalvalue is not None:
            self.physicalvalue = physicalvalue

        if unit is not None:
            self.unit = unit

        if options is not None:
            self.options = options


class StimulusBinding(EObject, metaclass=MetaEClass):

    stimulusSource = EAttribute(eType=EString, derived=False, changeable=True)
    targetSignal = EAttribute(eType=EString, derived=False, changeable=True)
    stimulusId = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, stimulusSource=None, targetSignal=None, stimulusId=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if stimulusSource is not None:
            self.stimulusSource = stimulusSource

        if targetSignal is not None:
            self.targetSignal = targetSignal

        if stimulusId is not None:
            self.stimulusId = stimulusId


class StimulusParameter(EObject, metaclass=MetaEClass):

    parameterName = EAttribute(eType=EString, derived=False, changeable=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, parameterName=None, description=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if parameterName is not None:
            self.parameterName = parameterName

        if description is not None:
            self.description = description

        if value is not None:
            self.value = value


class ArrayMember(EObject, metaclass=MetaEClass):

    index = EAttribute(eType=EInt, derived=False, changeable=True, upper=-1)
    attribute = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    dataType = EAttribute(eType=DataType, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, index=None, attribute=None, name=None, taeAssert=None, dataType=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if index:
            self.index.extend(index)

        if attribute:
            self.attribute.extend(attribute)

        if name is not None:
            self.name = name

        if dataType is not None:
            self.dataType = dataType

        if taeAssert is not None:
            self.taeAssert = taeAssert


class EthInputVariable(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)
    unit = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, dataType=None, value=None, unit=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if dataType is not None:
            self.dataType = dataType

        if value is not None:
            self.value = value

        if unit is not None:
            self.unit = unit


class Process(Activity):

    tpaId = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    startNode = EReference(ordered=True, unique=True, containment=True)
    endNode = EReference(ordered=True, unique=True, containment=True)
    activitySequence = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, startNode=None, endNode=None, activitySequence=None, tpaId=None, **kwargs):

        super().__init__(**kwargs)

        if tpaId is not None:
            self.tpaId = tpaId

        if startNode is not None:
            self.startNode = startNode

        if endNode is not None:
            self.endNode = endNode

        if activitySequence is not None:
            self.activitySequence = activitySequence


@abstract
class IndirectActivity(Activity):

    directactivity = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, directactivity=None, **kwargs):

        super().__init__(**kwargs)

        if directactivity:
            self.directactivity.extend(directactivity)


@abstract
class DirectActivity(Activity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class NumberVariableValue(VariableValue):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class StringVariableValue(VariableValue):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class PythonObjectVariableValue(VariableValue):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class EnumVariableValue(VariableValue):

    entity = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, entity=None, **kwargs):

        super().__init__(**kwargs)

        if entity:
            self.entity.extend(entity)


class FunctionVariableValue(VariableValue):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class ModelCapture(Capture):

    downsampling = EAttribute(eType=EString, derived=False, changeable=True, default_value='100')

    def __init__(self, *, downsampling=None, **kwargs):

        super().__init__(**kwargs)

        if downsampling is not None:
            self.downsampling = downsampling


class McCapture(Capture):

    raster = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, raster=None, **kwargs):

        super().__init__(**kwargs)

        if raster is not None:
            self.raster = raster


class ExpectationModeNumeric(ExpectationInterface):

    operator = EAttribute(eType=TYPENUMBEROPERATOR, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True, default_value='0')
    typeOfTolerance = EAttribute(eType=TYPENUMBERTOLERANCE, derived=False, changeable=True)
    valueOfTolerance = EAttribute(eType=EString, derived=False, changeable=True, default_value='0')

    def __init__(self, *, operator=None, value=None, typeOfTolerance=None, valueOfTolerance=None, **kwargs):

        super().__init__(**kwargs)

        if operator is not None:
            self.operator = operator

        if value is not None:
            self.value = value

        if typeOfTolerance is not None:
            self.typeOfTolerance = typeOfTolerance

        if valueOfTolerance is not None:
            self.valueOfTolerance = valueOfTolerance


class ExpectationModeString(ExpectationInterface):

    operator = EAttribute(eType=TYPESTRINGOPERATOR, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True, default_value="''")
    caseSensitivity = EAttribute(eType=EBoolean, derived=False, changeable=True)
    containedInValues = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)

    def __init__(self, *, operator=None, value=None, caseSensitivity=None, containedInValues=None, **kwargs):

        super().__init__(**kwargs)

        if operator is not None:
            self.operator = operator

        if value is not None:
            self.value = value

        if caseSensitivity is not None:
            self.caseSensitivity = caseSensitivity

        if containedInValues:
            self.containedInValues.extend(containedInValues)


class ExpectationModePythonExpression(ExpectationInterface):

    value = EAttribute(eType=EString, derived=False, changeable=True, default_value='_value_==0')

    def __init__(self, *, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value


class ExpectationTimeOption(IsSave):

    mode = EAttribute(eType=TYPETIMEOPTIONMODE, derived=False, changeable=True)
    timeout = EAttribute(eType=EString, derived=False, changeable=True, default_value='100')
    timeoutUnit = EAttribute(eType=TYPETIMEUNIT, derived=False, changeable=True)
    minimumDuration = EAttribute(eType=EString, derived=False, changeable=True, default_value='100')
    minimumDurationUnit = EAttribute(eType=TYPETIMEUNIT, derived=False, changeable=True)
    samplingPeriod = EAttribute(eType=EString, derived=False, changeable=True, default_value='100')
    samplingPeriodUnit = EAttribute(eType=TYPETIMEUNIT, derived=False,
                                    changeable=True, default_value=TYPETIMEUNIT.ms)
    sampling = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, mode=None, timeout=None, timeoutUnit=None, minimumDuration=None, minimumDurationUnit=None, samplingPeriod=None, samplingPeriodUnit=None, sampling=None, **kwargs):

        super().__init__(**kwargs)

        if mode is not None:
            self.mode = mode

        if timeout is not None:
            self.timeout = timeout

        if timeoutUnit is not None:
            self.timeoutUnit = timeoutUnit

        if minimumDuration is not None:
            self.minimumDuration = minimumDuration

        if minimumDurationUnit is not None:
            self.minimumDurationUnit = minimumDurationUnit

        if samplingPeriod is not None:
            self.samplingPeriod = samplingPeriod

        if samplingPeriodUnit is not None:
            self.samplingPeriodUnit = samplingPeriodUnit

        if sampling is not None:
            self.sampling = sampling


class DidSaveAndAssert(IsSave):

    mode = EAttribute(eType=EString, derived=False, changeable=True, default_value='Physical')
    name = EAttribute(eType=EString, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, taeAssert=None, mode=None, name=None, **kwargs):

        super().__init__(**kwargs)

        if mode is not None:
            self.mode = mode

        if name is not None:
            self.name = name

        if taeAssert is not None:
            self.taeAssert = taeAssert


class DTCObject(IsSave):

    value = EAttribute(eType=EString, derived=False, changeable=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    statusCode = EAttribute(eType=EString, derived=False, changeable=True)
    numberIdentifier = EAttribute(eType=EString, derived=False, changeable=True)
    statusCodeSaveAndAssert = EReference(ordered=True, unique=True, containment=True)
    numberOfIdentifierSaveAndAssert = EReference(ordered=True, unique=True, containment=True)
    snapshotRecord = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, value=None, description=None, statusCode=None, statusCodeSaveAndAssert=None, numberOfIdentifierSaveAndAssert=None, numberIdentifier=None, snapshotRecord=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value

        if description is not None:
            self.description = description

        if statusCode is not None:
            self.statusCode = statusCode

        if numberIdentifier is not None:
            self.numberIdentifier = numberIdentifier

        if statusCodeSaveAndAssert is not None:
            self.statusCodeSaveAndAssert = statusCodeSaveAndAssert

        if numberOfIdentifierSaveAndAssert is not None:
            self.numberOfIdentifierSaveAndAssert = numberOfIdentifierSaveAndAssert

        if snapshotRecord:
            self.snapshotRecord.extend(snapshotRecord)


class StatusRecord(IsSave):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, name=None, dataType=None, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if dataType is not None:
            self.dataType = dataType

        if taeAssert is not None:
            self.taeAssert = taeAssert


class ExpectationModeArray(ExpectationInterface):

    member = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, member=None, **kwargs):

        super().__init__(**kwargs)

        if member:
            self.member.extend(member)


class DTCStatusCodeSaveAndAssert(IsSave):

    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if taeAssert is not None:
            self.taeAssert = taeAssert


class NumberOfIdentifierSaveAndAssert(IsSave):

    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if taeAssert is not None:
            self.taeAssert = taeAssert


class DID(IsSave):

    byte = EAttribute(eType=EString, derived=False, changeable=True)
    bit = EAttribute(eType=EString, derived=False, changeable=True)
    subDataNameC = EAttribute(eType=EString, derived=False, changeable=True)
    subDataNameE = EAttribute(eType=EString, derived=False, changeable=True)
    datatype = EAttribute(eType=EString, derived=False, changeable=True)
    number = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)
    didSaveAndAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, byte=None, bit=None, subDataNameC=None, subDataNameE=None, datatype=None, didSaveAndAssert=None, number=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if byte is not None:
            self.byte = byte

        if bit is not None:
            self.bit = bit

        if subDataNameC is not None:
            self.subDataNameC = subDataNameC

        if subDataNameE is not None:
            self.subDataNameE = subDataNameE

        if datatype is not None:
            self.datatype = datatype

        if number is not None:
            self.number = number

        if value is not None:
            self.value = value

        if didSaveAndAssert is not None:
            self.didSaveAndAssert = didSaveAndAssert


class AudioCapture(Capture):

    downsampling = EAttribute(eType=EString, derived=False, changeable=True, default_value='16000')

    def __init__(self, *, downsampling=None, **kwargs):

        super().__init__(**kwargs)

        if downsampling is not None:
            self.downsampling = downsampling


class ExpectationMcArray(ExpectationInterface):

    member = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, member=None, **kwargs):

        super().__init__(**kwargs)

        if member:
            self.member.extend(member)


class BaseCapture(Capture):

    raster = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, raster=None, **kwargs):

        super().__init__(**kwargs)

        if raster is not None:
            self.raster = raster


class EthReadVariable(IsSave):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    expect = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, name=None, dataType=None, expect=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if dataType is not None:
            self.dataType = dataType

        if expect is not None:
            self.expect = expect


@abstract
class ActivityList(DirectActivity):

    children = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, children=None, **kwargs):

        super().__init__(**kwargs)

        if children:
            self.children.extend(children)


class Wait(DirectActivity):

    time = EAttribute(eType=EString, derived=False, changeable=True, default_value='100')
    unit = EAttribute(eType=TYPETIMEUNIT, derived=False,
                      changeable=True, default_value=TYPETIMEUNIT.ms)

    def __init__(self, *, time=None, unit=None, **kwargs):

        super().__init__(**kwargs)

        if time is not None:
            self.time = time

        if unit is not None:
            self.unit = unit

    def waitValidate(self, chain=None, context=None):

        raise NotImplementedError('operation waitValidate(...) not yet implemented')


class If(DirectActivity):

    condition = EAttribute(eType=EString, derived=False, changeable=True)
    then = EReference(ordered=True, unique=True, containment=True)
    elseif = EReference(ordered=True, unique=True, containment=True, upper=-1)
    taeElse = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, then=None, elseif=None, taeElse=None, condition=None, **kwargs):

        super().__init__(**kwargs)

        if condition is not None:
            self.condition = condition

        if then is not None:
            self.then = then

        if elseif:
            self.elseif.extend(elseif)

        if taeElse is not None:
            self.taeElse = taeElse

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class ElseIf(IndirectActivity):

    condition = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, condition=None, **kwargs):

        super().__init__(**kwargs)

        if condition is not None:
            self.condition = condition

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class Then(IndirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Else(IndirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Case(IndirectActivity):

    condition = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, condition=None, **kwargs):

        super().__init__(**kwargs)

        if condition is not None:
            self.condition = condition

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class Switch(DirectActivity):

    expression = EAttribute(eType=EString, derived=False, changeable=True)
    taeCase = EReference(ordered=True, unique=True, containment=True, upper=-1)
    taeDefault = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, taeCase=None, taeDefault=None, expression=None, **kwargs):

        super().__init__(**kwargs)

        if expression is not None:
            self.expression = expression

        if taeCase:
            self.taeCase.extend(taeCase)

        if taeDefault is not None:
            self.taeDefault = taeDefault

    def expressValidate(self, chain=None, context=None):

        raise NotImplementedError('operation expressValidate(...) not yet implemented')


class Default(IndirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Break(DirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Return(DirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Exit(DirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Continue(DirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Try(DirectActivity):

    taeExcept = EReference(ordered=True, unique=True, containment=False)
    taeFinally = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, taeExcept=None, taeFinally=None, **kwargs):

        super().__init__(**kwargs)

        if taeExcept is not None:
            self.taeExcept = taeExcept

        if taeFinally is not None:
            self.taeFinally = taeFinally


class Except(IndirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Finally(IndirectActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Condition(DirectActivity):

    source = EAttribute(eType=EString, derived=False, changeable=True)
    condtionType = EAttribute(eType=EString, derived=False, changeable=True)
    condtionValue = EAttribute(eType=EString, derived=False, changeable=True)
    strMeasurment = EAttribute(eType=EString, derived=False,
                               changeable=True, default_value='end with')
    strMeasurmentContent = EAttribute(eType=EString, derived=False,
                                      changeable=True, default_value=' ')
    measurment = EAttribute(eType=EString, derived=False, changeable=True)
    measurmentContent = EAttribute(eType=EString, derived=False, changeable=True)
    time = EAttribute(eType=EBoolean, derived=False, changeable=True)
    timeOut = EAttribute(eType=EString, derived=False, changeable=True)
    timeUnit = EAttribute(eType=EString, derived=False, changeable=True, default_value='ms')
    success = EAttribute(eType=EBoolean, derived=False, changeable=True)
    failed = EAttribute(eType=EBoolean, derived=False, changeable=True)
    successContent = EAttribute(eType=EString, derived=False, changeable=True)
    failedContent = EAttribute(eType=EString, derived=False, changeable=True)
    none = EAttribute(eType=EBoolean, derived=False, changeable=True)
    min = EAttribute(eType=EBoolean, derived=False, changeable=True)
    minText = EAttribute(eType=EString, derived=False, changeable=True)
    last = EAttribute(eType=EBoolean, derived=False, changeable=True)
    cycle = EAttribute(eType=EBoolean, derived=False, changeable=True)
    cycleText = EAttribute(eType=EString, derived=False, changeable=True)
    sys = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, source=None, condtionType=None, condtionValue=None, strMeasurment=None, strMeasurmentContent=None, measurment=None, measurmentContent=None, time=None, timeOut=None, timeUnit=None, success=None, failed=None, successContent=None, failedContent=None, none=None, min=None, minText=None, last=None, cycle=None, cycleText=None, sys=None, **kwargs):

        super().__init__(**kwargs)

        if source is not None:
            self.source = source

        if condtionType is not None:
            self.condtionType = condtionType

        if condtionValue is not None:
            self.condtionValue = condtionValue

        if strMeasurment is not None:
            self.strMeasurment = strMeasurment

        if strMeasurmentContent is not None:
            self.strMeasurmentContent = strMeasurmentContent

        if measurment is not None:
            self.measurment = measurment

        if measurmentContent is not None:
            self.measurmentContent = measurmentContent

        if time is not None:
            self.time = time

        if timeOut is not None:
            self.timeOut = timeOut

        if timeUnit is not None:
            self.timeUnit = timeUnit

        if success is not None:
            self.success = success

        if failed is not None:
            self.failed = failed

        if successContent is not None:
            self.successContent = successContent

        if failedContent is not None:
            self.failedContent = failedContent

        if none is not None:
            self.none = none

        if min is not None:
            self.min = min

        if minText is not None:
            self.minText = minText

        if last is not None:
            self.last = last

        if cycle is not None:
            self.cycle = cycle

        if cycleText is not None:
            self.cycleText = cycleText

        if sys is not None:
            self.sys = sys


class Write(DirectActivity):

    sourceMapping = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)
    accessMode = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, sourceMapping=None, accessMode=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if sourceMapping is not None:
            self.sourceMapping = sourceMapping

        if value is not None:
            self.value = value

        if accessMode is not None:
            self.accessMode = accessMode


class StartCapture(DirectActivity):

    captureName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, captureName=None, **kwargs):

        super().__init__(**kwargs)

        if captureName is not None:
            self.captureName = captureName


class StopCapture(DirectActivity):

    captureName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, captureName=None, **kwargs):

        super().__init__(**kwargs)

        if captureName is not None:
            self.captureName = captureName


class AddCaptureToReport(DirectActivity):

    captureName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    title = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    plots = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, captureName=None, title=None, plots=None, **kwargs):

        super().__init__(**kwargs)

        if captureName is not None:
            self.captureName = captureName

        if title is not None:
            self.title = title

        if plots:
            self.plots.extend(plots)


class Exec(DirectActivity):

    code = EAttribute(eType=EString, derived=False, changeable=True)
    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    mapping = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, variables=None, mapping=None, code=None, **kwargs):

        super().__init__(**kwargs)

        if code is not None:
            self.code = code

        if variables:
            self.variables.extend(variables)

        if mapping:
            self.mapping.extend(mapping)


class EESConnect(DirectActivity):

    deviceName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, deviceName=None, **kwargs):

        super().__init__(**kwargs)

        if deviceName is not None:
            self.deviceName = deviceName


class EESDeConnect(DirectActivity):

    deviceName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, deviceName=None, **kwargs):

        super().__init__(**kwargs)

        if deviceName is not None:
            self.deviceName = deviceName


class EESConfig(DirectActivity):

    resistor = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    duration = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    dutyCycle = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    frequency = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    potential = EAttribute(eType=POTENTIAL, derived=False, changeable=True)
    userDefined = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    errorType = EAttribute(eType=ERRORTYPE, derived=False, changeable=True)
    timeOption = EAttribute(eType=TIMEOPTION, derived=False, changeable=True)
    channel = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, channel=None, resistor=None, duration=None, dutyCycle=None, frequency=None, potential=None, userDefined=None, errorType=None, timeOption=None, **kwargs):

        super().__init__(**kwargs)

        if resistor is not None:
            self.resistor = resistor

        if duration is not None:
            self.duration = duration

        if dutyCycle is not None:
            self.dutyCycle = dutyCycle

        if frequency is not None:
            self.frequency = frequency

        if potential is not None:
            self.potential = potential

        if userDefined is not None:
            self.userDefined = userDefined

        if errorType is not None:
            self.errorType = errorType

        if timeOption is not None:
            self.timeOption = timeOption

        if channel:
            self.channel.extend(channel)


class EESActivateAll(DirectActivity):

    deviceName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, deviceName=None, **kwargs):

        super().__init__(**kwargs)

        if deviceName is not None:
            self.deviceName = deviceName


class EESDeActivateAll(DirectActivity):

    deviceName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, deviceName=None, **kwargs):

        super().__init__(**kwargs)

        if deviceName is not None:
            self.deviceName = deviceName


@abstract
class Dialog(DirectActivity):

    titile = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    description = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, titile=None, description=None, **kwargs):

        super().__init__(**kwargs)

        if titile is not None:
            self.titile = titile

        if description is not None:
            self.description = description


class WriteSignalGroup(DirectActivity):

    sourceMapping = EAttribute(eType=EString, derived=False, changeable=True)
    shouldWrite = EAttribute(eType=EString, derived=False, changeable=True)
    cycleTime = EAttribute(eType=EInt, derived=False, changeable=True)
    intervalTime = EAttribute(eType=EInt, derived=False, changeable=True)
    existWrite = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, existWrite=None, sourceMapping=None, shouldWrite=None, cycleTime=None, intervalTime=None, **kwargs):

        super().__init__(**kwargs)

        if sourceMapping is not None:
            self.sourceMapping = sourceMapping

        if shouldWrite is not None:
            self.shouldWrite = shouldWrite

        if cycleTime is not None:
            self.cycleTime = cycleTime

        if intervalTime is not None:
            self.intervalTime = intervalTime

        if existWrite:
            self.existWrite.extend(existWrite)


class ReadSignalGroup(DirectActivity):

    sourceMapping = EAttribute(eType=EString, derived=False, changeable=True)
    shouldRead = EAttribute(eType=EString, derived=False, changeable=True)
    existRead = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, existRead=None, sourceMapping=None, shouldRead=None, **kwargs):

        super().__init__(**kwargs)

        if sourceMapping is not None:
            self.sourceMapping = sourceMapping

        if shouldRead is not None:
            self.shouldRead = shouldRead

        if existRead:
            self.existRead.extend(existRead)


class MultiRead(DirectActivity):

    passWhen = EAttribute(eType=TYPEPASSWHENMODE, derived=False, changeable=True)
    passAtSameTime = EAttribute(eType=EBoolean, derived=False, changeable=True)
    signalList = EReference(ordered=True, unique=True, containment=True, upper=-1)
    timeOption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, signalList=None, passWhen=None, passAtSameTime=None, timeOption=None, **kwargs):

        super().__init__(**kwargs)

        if passWhen is not None:
            self.passWhen = passWhen

        if passAtSameTime is not None:
            self.passAtSameTime = passAtSameTime

        if signalList:
            self.signalList.extend(signalList)

        if timeOption is not None:
            self.timeOption = timeOption


class StartStimulus(DirectActivity):

    stimulusFile = EAttribute(eType=EString, derived=False, changeable=True)
    executeMode = EAttribute(eType=EString, derived=False, changeable=True)
    stimulusationName = EAttribute(eType=EString, derived=False, changeable=True)
    targetSignal = EReference(ordered=True, unique=True, containment=True, upper=-1)
    parameter = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, stimulusFile=None, executeMode=None, targetSignal=None, parameter=None, stimulusationName=None, **kwargs):

        super().__init__(**kwargs)

        if stimulusFile is not None:
            self.stimulusFile = stimulusFile

        if executeMode is not None:
            self.executeMode = executeMode

        if stimulusationName is not None:
            self.stimulusationName = stimulusationName

        if targetSignal:
            self.targetSignal.extend(targetSignal)

        if parameter:
            self.parameter.extend(parameter)


class SignalStimulus(DirectActivity):

    signalName = EAttribute(eType=EString, derived=False, changeable=True)
    executeMode = EAttribute(eType=EString, derived=False, changeable=True)
    stimulusationDescription = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, signalName=None, executeMode=None, stimulusationDescription=None, **kwargs):

        super().__init__(**kwargs)

        if signalName is not None:
            self.signalName = signalName

        if executeMode is not None:
            self.executeMode = executeMode

        if stimulusationDescription:
            self.stimulusationDescription.extend(stimulusationDescription)


class StopStimulus(DirectActivity):

    stimulusationName = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, stimulusationName=None, **kwargs):

        super().__init__(**kwargs)

        if stimulusationName is not None:
            self.stimulusationName = stimulusationName


class Evaluate(DirectActivity):

    evaluateDescription = EAttribute(eType=EString, derived=False, changeable=True)
    setResult = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, evaluateDescription=None, setResult=None, **kwargs):

        super().__init__(**kwargs)

        if evaluateDescription is not None:
            self.evaluateDescription = evaluateDescription

        if setResult is not None:
            self.setResult = setResult


class BaseSegmentType(DirectActivity):

    comment = EAttribute(eType=EString, derived=False, changeable=True)
    duration = EAttribute(eType=EString, derived=False, changeable=True)
    stopTrigger = EAttribute(eType=EString, derived=False, changeable=True)
    options = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, comment=None, duration=None, stopTrigger=None, options=None, **kwargs):

        super().__init__(**kwargs)

        if comment is not None:
            self.comment = comment

        if duration is not None:
            self.duration = duration

        if stopTrigger is not None:
            self.stopTrigger = stopTrigger

        if options is not None:
            self.options = options


class EthReadInput(DirectActivity):

    methodName = EAttribute(eType=EString, derived=False, changeable=True)
    methodPath = EAttribute(eType=EString, derived=False, changeable=True)
    resultValue = EReference(ordered=True, unique=True, containment=True, upper=-1)
    timeOption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, methodName=None, methodPath=None, resultValue=None, timeOption=None, **kwargs):

        super().__init__(**kwargs)

        if methodName is not None:
            self.methodName = methodName

        if methodPath is not None:
            self.methodPath = methodPath

        if resultValue:
            self.resultValue.extend(resultValue)

        if timeOption is not None:
            self.timeOption = timeOption


class EthReadOutput(DirectActivity):

    methodName = EAttribute(eType=EString, derived=False, changeable=True)
    methodPath = EAttribute(eType=EString, derived=False, changeable=True)
    resultValue = EReference(ordered=True, unique=True, containment=True, upper=-1)
    timeOption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, methodName=None, methodPath=None, resultValue=None, timeOption=None, **kwargs):

        super().__init__(**kwargs)

        if methodName is not None:
            self.methodName = methodName

        if methodPath is not None:
            self.methodPath = methodPath

        if resultValue:
            self.resultValue.extend(resultValue)

        if timeOption is not None:
            self.timeOption = timeOption


class EthCallMethod(DirectActivity):

    methodName = EAttribute(eType=EString, derived=False, changeable=True)
    methodPath = EAttribute(eType=EString, derived=False, changeable=True)
    inputValue = EReference(ordered=True, unique=True, containment=True, upper=-1)
    returnValue = EReference(ordered=True, unique=True, containment=True, upper=-1)
    timeOption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, methodName=None, methodPath=None, inputValue=None, returnValue=None, timeOption=None, **kwargs):

        super().__init__(**kwargs)

        if methodName is not None:
            self.methodName = methodName

        if methodPath is not None:
            self.methodPath = methodPath

        if inputValue:
            self.inputValue.extend(inputValue)

        if returnValue:
            self.returnValue.extend(returnValue)

        if timeOption is not None:
            self.timeOption = timeOption


class While(ActivityList):

    condition = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, condition=None, **kwargs):

        super().__init__(**kwargs)

        if condition is not None:
            self.condition = condition

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class DoWhile(ActivityList):

    condition = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, condition=None, **kwargs):

        super().__init__(**kwargs)

        if condition is not None:
            self.condition = condition

    def conditionValidate(self, chain=None, context=None):

        raise NotImplementedError('operation conditionValidate(...) not yet implemented')


class CallSequence(DirectActivity, VariableContiner):

    seqPath = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, seqPath=None, **kwargs):

        super().__init__(**kwargs)

        if seqPath is not None:
            self.seqPath = seqPath


class Compute(DirectActivity, IsSave):

    expression = EAttribute(eType=EString, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, expression=None, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if expression is not None:
            self.expression = expression

        if taeAssert is not None:
            self.taeAssert = taeAssert

    def expressValidate(self, chain=None, context=None):

        raise NotImplementedError('operation expressValidate(...) not yet implemented')


class ScriptBlock(DirectActivity, VariableContiner):

    script = EAttribute(eType=EString, derived=False, changeable=True)
    runInAnotherThread = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, script=None, runInAnotherThread=None, **kwargs):

        super().__init__(**kwargs)

        if script is not None:
            self.script = script

        if runInAnotherThread is not None:
            self.runInAnotherThread = runInAnotherThread


class Read(DirectActivity, IsSave):

    offlineValue = EAttribute(eType=EString, derived=False, changeable=True)
    sourceSignalItem = EReference(ordered=True, unique=True, containment=True)
    accessMode = EReference(ordered=True, unique=True, containment=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, sourceSignalItem=None, accessMode=None, taeAssert=None, offlineValue=None, **kwargs):

        super().__init__(**kwargs)

        if offlineValue is not None:
            self.offlineValue = offlineValue

        if sourceSignalItem is not None:
            self.sourceSignalItem = sourceSignalItem

        if accessMode is not None:
            self.accessMode = accessMode

        if taeAssert is not None:
            self.taeAssert = taeAssert


class ConfirmDialog(Dialog):

    confirmType = EAttribute(eType=CONFIRMTYPE, derived=False, changeable=True)
    time = EAttribute(eType=EBoolean, derived=False, changeable=True)
    timeOut = EAttribute(eType=EString, derived=False, changeable=True)
    timeUnit = EAttribute(eType=TYPETIMEUNIT, derived=False, changeable=True)
    defaultValue = EAttribute(eType=CONFIRMDEFAULTVALUE, derived=False, changeable=True)

    def __init__(self, *, confirmType=None, time=None, timeOut=None, timeUnit=None, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if confirmType is not None:
            self.confirmType = confirmType

        if time is not None:
            self.time = time

        if timeOut is not None:
            self.timeOut = timeOut

        if timeUnit is not None:
            self.timeUnit = timeUnit

        if defaultValue is not None:
            self.defaultValue = defaultValue


class DataAnalysesRef(DirectActivity, SignalVariableContainer):

    daFilePath = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, daFilePath=None, **kwargs):

        super().__init__(**kwargs)

        if daFilePath is not None:
            self.daFilePath = daFilePath


class ExpSegmentType(BaseSegmentType):

    start = EAttribute(eType=EString, derived=False, changeable=True)
    stop = EAttribute(eType=EString, derived=False, changeable=True)
    tau = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, start=None, stop=None, tau=None, **kwargs):

        super().__init__(**kwargs)

        if start is not None:
            self.start = start

        if stop is not None:
            self.stop = stop

        if tau is not None:
            self.tau = tau


class ConstSegmentType(BaseSegmentType):

    value = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value


class IdleSegmentType(BaseSegmentType):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class NoiseSegmentType(BaseSegmentType):

    mean = EAttribute(eType=EString, derived=False, changeable=True)
    sigma = EAttribute(eType=EString, derived=False, changeable=True)
    seed = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, mean=None, sigma=None, seed=None, **kwargs):

        super().__init__(**kwargs)

        if mean is not None:
            self.mean = mean

        if sigma is not None:
            self.sigma = sigma

        if seed is not None:
            self.seed = seed


class PulseSegmentType(BaseSegmentType):

    dutyCycle = EAttribute(eType=EString, derived=False, changeable=True)
    amplitude = EAttribute(eType=EString, derived=False, changeable=True)
    period = EAttribute(eType=EString, derived=False, changeable=True)
    offset = EAttribute(eType=EString, derived=False, changeable=True)
    phase = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, dutyCycle=None, amplitude=None, period=None, offset=None, phase=None, **kwargs):

        super().__init__(**kwargs)

        if dutyCycle is not None:
            self.dutyCycle = dutyCycle

        if amplitude is not None:
            self.amplitude = amplitude

        if period is not None:
            self.period = period

        if offset is not None:
            self.offset = offset

        if phase is not None:
            self.phase = phase


class RampSegmentType(BaseSegmentType):

    start = EAttribute(eType=EString, derived=False, changeable=True)
    stop = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, start=None, stop=None, **kwargs):

        super().__init__(**kwargs)

        if start is not None:
            self.start = start

        if stop is not None:
            self.stop = stop


class RampSlopeSegmentType(BaseSegmentType):

    offset = EAttribute(eType=EString, derived=False, changeable=True)
    slope = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, offset=None, slope=None, **kwargs):

        super().__init__(**kwargs)

        if offset is not None:
            self.offset = offset

        if slope is not None:
            self.slope = slope


class SawSegmentType(BaseSegmentType):

    dutyCycle = EAttribute(eType=EString, derived=False, changeable=True)
    amplitude = EAttribute(eType=EString, derived=False, changeable=True)
    period = EAttribute(eType=EString, derived=False, changeable=True)
    offset = EAttribute(eType=EString, derived=False, changeable=True)
    phase = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, dutyCycle=None, amplitude=None, period=None, offset=None, phase=None, **kwargs):

        super().__init__(**kwargs)

        if dutyCycle is not None:
            self.dutyCycle = dutyCycle

        if amplitude is not None:
            self.amplitude = amplitude

        if period is not None:
            self.period = period

        if offset is not None:
            self.offset = offset

        if phase is not None:
            self.phase = phase


class SineSegmentType(BaseSegmentType):

    phase = EAttribute(eType=EString, derived=False, changeable=True)
    amplitude = EAttribute(eType=EString, derived=False, changeable=True)
    period = EAttribute(eType=EString, derived=False, changeable=True)
    offset = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, phase=None, amplitude=None, period=None, offset=None, **kwargs):

        super().__init__(**kwargs)

        if phase is not None:
            self.phase = phase

        if amplitude is not None:
            self.amplitude = amplitude

        if period is not None:
            self.period = period

        if offset is not None:
            self.offset = offset


class Group(ActivityList, VariableContiner):

    on = EAttribute(eType=EBoolean, derived=False, changeable=True)
    abortTestOn = EAttribute(eType=TESTON, derived=False, changeable=True)

    def __init__(self, *, on=None, abortTestOn=None, **kwargs):

        super().__init__(**kwargs)

        if on is not None:
            self.on = on

        if abortTestOn is not None:
            self.abortTestOn = abortTestOn


class ChoiceDialog(Dialog, IsSave):

    items = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)
    enum = EAttribute(eType=EBoolean, derived=False, changeable=True)
    enumVariable = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')

    def __init__(self, *, items=None, enum=None, enumVariable=None, **kwargs):

        super().__init__(**kwargs)

        if items:
            self.items.extend(items)

        if enum is not None:
            self.enum = enum

        if enumVariable is not None:
            self.enumVariable = enumVariable


class InputDialog(Dialog, IsSave):

    identifier = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    defaultValue = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    res = EAttribute(eType=EBoolean, derived=False, changeable=True)
    restirction = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, identifier=None, defaultValue=None, res=None, restirction=None, **kwargs):

        super().__init__(**kwargs)

        if identifier is not None:
            self.identifier = identifier

        if defaultValue is not None:
            self.defaultValue = defaultValue

        if res is not None:
            self.res = res

        if restirction is not None:
            self.restirction = restirction


class Initialization(ActivityList, VariableContiner):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Cleanup(ActivityList, VariableContiner):

    executeAfterAbortingTheTest = EAttribute(
        eType=EBoolean, derived=False, changeable=True, default_value=True)

    def __init__(self, *, executeAfterAbortingTheTest=None, **kwargs):

        super().__init__(**kwargs)

        if executeAfterAbortingTheTest is not None:
            self.executeAfterAbortingTheTest = executeAfterAbortingTheTest


class ReadDataByIdentifier(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    did = EAttribute(eType=EString, derived=False, changeable=True)
    subData = EAttribute(eType=EString, derived=False, changeable=True)
    didSaveAndAssertList = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, ecu=None, didSaveAndAssertList=None, did=None, subData=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if did is not None:
            self.did = did

        if subData is not None:
            self.subData = subData

        if didSaveAndAssertList:
            self.didSaveAndAssertList.extend(didSaveAndAssertList)


class WriteDataByIdentifier(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    didName = EAttribute(eType=EString, derived=False, changeable=True)
    mode = EAttribute(eType=EString, derived=False, changeable=True, default_value='RAW')
    value = EAttribute(eType=EString, derived=False, changeable=True)
    did = EAttribute(eType=EString, derived=False, changeable=True)
    subDataList = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, ecu=None, didName=None, mode=None, value=None, did=None, subDataList=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if didName is not None:
            self.didName = didName

        if mode is not None:
            self.mode = mode

        if value is not None:
            self.value = value

        if did is not None:
            self.did = did

        if subDataList:
            self.subDataList.extend(subDataList)


class ClearDTC(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    groupOfDTC = EAttribute(eType=EString, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, ecu=None, groupOfDTC=None, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if groupOfDTC is not None:
            self.groupOfDTC = groupOfDTC

        if taeAssert is not None:
            self.taeAssert = taeAssert


class CallService(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    request = EAttribute(eType=EString, derived=False, changeable=True)
    serviceName = EAttribute(eType=EString, derived=False, changeable=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, ecu=None, taeAssert=None, request=None, serviceName=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if request is not None:
            self.request = request

        if serviceName is not None:
            self.serviceName = serviceName

        if taeAssert is not None:
            self.taeAssert = taeAssert


class ReadDTCInformation(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    subFunction = EAttribute(eType=EString, derived=False, changeable=True)
    statusMask = EAttribute(eType=EString, derived=False, changeable=True)
    subFunctionId = EAttribute(eType=EString, derived=False, changeable=True)
    snapshotRecordNumber = EAttribute(eType=EString, derived=False, changeable=True)
    expectList = EReference(ordered=True, unique=True, containment=True, upper=-1)
    notExpectList = EReference(ordered=True, unique=True, containment=True, upper=-1)
    dtc = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, ecu=None, subFunction=None, statusMask=None, expectList=None, notExpectList=None, subFunctionId=None, snapshotRecordNumber=None, dtc=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if subFunction is not None:
            self.subFunction = subFunction

        if statusMask is not None:
            self.statusMask = statusMask

        if subFunctionId is not None:
            self.subFunctionId = subFunctionId

        if snapshotRecordNumber is not None:
            self.snapshotRecordNumber = snapshotRecordNumber

        if expectList:
            self.expectList.extend(expectList)

        if notExpectList:
            self.notExpectList.extend(notExpectList)

        if dtc is not None:
            self.dtc = dtc


class RoutineControl(DirectActivity, IsSave, NegativeResponse):

    ecu = EAttribute(eType=EString, derived=False, changeable=True)
    subFunction = EAttribute(eType=EString, derived=False, changeable=True)
    routineIdentifier = EAttribute(eType=EString, derived=False, changeable=True)
    statusOptions = EAttribute(eType=EString, derived=False, changeable=True)
    optionRecordList = EReference(ordered=True, unique=True, containment=True, upper=-1)
    statusRecordList = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, ecu=None, subFunction=None, routineIdentifier=None, optionRecordList=None, statusRecordList=None, statusOptions=None, **kwargs):

        super().__init__(**kwargs)

        if ecu is not None:
            self.ecu = ecu

        if subFunction is not None:
            self.subFunction = subFunction

        if routineIdentifier is not None:
            self.routineIdentifier = routineIdentifier

        if statusOptions is not None:
            self.statusOptions = statusOptions

        if optionRecordList:
            self.optionRecordList.extend(optionRecordList)

        if statusRecordList:
            self.statusRecordList.extend(statusRecordList)


class ActivitySequence(Group):

    postProcessingScript = EAttribute(eType=EString, derived=False,
                                      changeable=True, default_value=' ')
    captureGroup = EReference(ordered=True, unique=True, containment=True)
    ctcGeneratorScript = EReference(ordered=True, unique=True, containment=True)
    ctc = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, captureGroup=None, postProcessingScript=None, ctcGeneratorScript=None, ctc=None, **kwargs):

        super().__init__(**kwargs)

        if postProcessingScript is not None:
            self.postProcessingScript = postProcessingScript

        if captureGroup is not None:
            self.captureGroup = captureGroup

        if ctcGeneratorScript is not None:
            self.ctcGeneratorScript = ctcGeneratorScript

        if ctc:
            self.ctc.extend(ctc)


class For(ActivityList, BreakCondition, IsSave):

    start = EAttribute(eType=EString, derived=False, changeable=True, default_value='0')
    stop = EAttribute(eType=EString, derived=False, changeable=True, default_value='10')
    step = EAttribute(eType=EString, derived=False, changeable=True, default_value='1')

    def __init__(self, *, start=None, stop=None, step=None, **kwargs):

        super().__init__(**kwargs)

        if start is not None:
            self.start = start

        if stop is not None:
            self.stop = stop

        if step is not None:
            self.step = step

    def currentValidate(self, chain=None, context=None):

        raise NotImplementedError('operation currentValidate(...) not yet implemented')

    def startValidate(self, chain=None, context=None):

        raise NotImplementedError('operation startValidate(...) not yet implemented')

    def stopValidate(self, chain=None, context=None):

        raise NotImplementedError('operation stopValidate(...) not yet implemented')

    def stepValidate(self, chain=None, context=None):

        raise NotImplementedError('operation stepValidate(...) not yet implemented')


class Loop(ActivityList, BreakCondition, IsSave):

    loopNumber = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, loopNumber=None, **kwargs):

        super().__init__(**kwargs)

        if loopNumber is not None:
            self.loopNumber = loopNumber

    def currentValidate(self, chain=None, context=None):

        raise NotImplementedError('operation currentValidate(...) not yet implemented')

    def loopValidate(self, chain=None, context=None):

        raise NotImplementedError('operation loopValidate(...) not yet implemented')
