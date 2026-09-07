"""Definition of meta model 'generator'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from testcase import Activity, DirectActivity


name = 'generator'
nsURI = 'com.hirain.tae.generator'
nsPrefix = 'generator'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class DynamicGuiActivity(EObject, metaclass=MetaEClass):

    className = EAttribute(eType=EString, derived=False, changeable=True)
    attributeGuis = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, className=None, attributeGuis=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if className is not None:
            self.className = className

        if attributeGuis:
            self.attributeGuis.extend(attributeGuis)


class AttributeGuiProperties(EObject, metaclass=MetaEClass):

    attrName = EAttribute(eType=EString, derived=False, changeable=True)
    attrView = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, attrName=None, attrView=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if attrName is not None:
            self.attrName = attrName

        if attrView is not None:
            self.attrView = attrView


class GuiControl(EObject, metaclass=MetaEClass):

    viewType = EAttribute(eType=EString, derived=False, changeable=True)
    viewExtend = EAttribute(eType=EString, derived=False, changeable=True)
    attrDefaultValue = EAttribute(eType=EString, derived=False, changeable=True)
    attrDescription = EAttribute(eType=EString, derived=False, changeable=True)
    attrLabel = EAttribute(eType=EString, derived=False, changeable=True)
    parameterType = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    icon = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    scriptName = EAttribute(eType=EString, derived=False, changeable=True)
    validationrule = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, viewType=None, viewExtend=None, attrDefaultValue=None, attrDescription=None, attrLabel=None, parameterType=None, icon=None, scriptName=None, validationrule=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if viewType is not None:
            self.viewType = viewType

        if viewExtend is not None:
            self.viewExtend = viewExtend

        if attrDefaultValue is not None:
            self.attrDefaultValue = attrDefaultValue

        if attrDescription is not None:
            self.attrDescription = attrDescription

        if attrLabel is not None:
            self.attrLabel = attrLabel

        if parameterType is not None:
            self.parameterType = parameterType

        if icon is not None:
            self.icon = icon

        if scriptName is not None:
            self.scriptName = scriptName

        if validationrule is not None:
            self.validationrule = validationrule


class AttributeDynamicValue(EObject, metaclass=MetaEClass):

    attrName = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    attrValue = EAttribute(eType=EString, derived=False, changeable=True)
    validationrule = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, attrName=None, attrValue=None, validationrule=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if attrName is not None:
            self.attrName = attrName

        if attrValue is not None:
            self.attrValue = attrValue

        if validationrule is not None:
            self.validationrule = validationrule


class FieldModel(AttributeDynamicValue):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class DynamicValueActivity(DirectActivity):

    toolType = EAttribute(eType=EString, derived=False, changeable=True, default_value='default')
    deviceInterfaceType = EAttribute(eType=EString, derived=False, changeable=True)
    toolName = EAttribute(eType=EString, derived=False, changeable=True, default_value='default')
    deviceInterfaceName = EAttribute(eType=EString, derived=False,
                                     changeable=True, default_value='default')
    functionName = EAttribute(eType=EString, derived=False,
                              changeable=True, default_value='default')
    inputField = EReference(ordered=True, unique=True, containment=True, upper=-1)
    outputField = EReference(ordered=True, unique=True, containment=True, upper=-1)
    timeoption = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, toolType=None, deviceInterfaceType=None, toolName=None, deviceInterfaceName=None, functionName=None, inputField=None, outputField=None, timeoption=None, **kwargs):

        super().__init__(**kwargs)

        if toolType is not None:
            self.toolType = toolType

        if deviceInterfaceType is not None:
            self.deviceInterfaceType = deviceInterfaceType

        if toolName is not None:
            self.toolName = toolName

        if deviceInterfaceName is not None:
            self.deviceInterfaceName = deviceInterfaceName

        if functionName is not None:
            self.functionName = functionName

        if inputField:
            self.inputField.extend(inputField)

        if outputField:
            self.outputField.extend(outputField)

        if timeoption is not None:
            self.timeoption = timeoption


class SaveAndAssertFieldModel(FieldModel):

    save = EReference(ordered=True, unique=True, containment=True)
    taeAssert = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, save=None, taeAssert=None, **kwargs):

        super().__init__(**kwargs)

        if save is not None:
            self.save = save

        if taeAssert is not None:
            self.taeAssert = taeAssert
