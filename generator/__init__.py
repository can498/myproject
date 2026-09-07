
from .generator import getEClassifier, eClassifiers
from .generator import name, nsURI, nsPrefix, eClass
from .generator import DynamicGuiActivity, AttributeGuiProperties, GuiControl, DynamicValueActivity, AttributeDynamicValue, FieldModel, SaveAndAssertFieldModel

from testcase import SeqTag, IsAssert, IsSave, ExpectationTimeOption

from . import generator

__all__ = ['DynamicGuiActivity', 'AttributeGuiProperties', 'GuiControl',
           'DynamicValueActivity', 'AttributeDynamicValue', 'FieldModel', 'SaveAndAssertFieldModel']

eSubpackages = []
eSuperPackage = None
generator.eSubpackages = eSubpackages
generator.eSuperPackage = eSuperPackage

DynamicGuiActivity.attributeGuis.eType = AttributeGuiProperties
AttributeGuiProperties.attrView.eType = GuiControl
DynamicValueActivity.inputField.eType = FieldModel
DynamicValueActivity.outputField.eType = SaveAndAssertFieldModel
DynamicValueActivity.timeoption.eType = ExpectationTimeOption
SaveAndAssertFieldModel.save.eType = IsSave
SaveAndAssertFieldModel.taeAssert.eType = IsAssert

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
