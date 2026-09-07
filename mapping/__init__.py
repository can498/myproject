
from .mapping import getEClassifier, eClassifiers
from .mapping import name, nsURI, nsPrefix, eClass
from .mapping import VarType, Enumeration, EnumerationEntity, MappingFolder, Mapping, ModelMapping, MeasurementMapping, CalibrationMapping, EesMapping, MessageMapping, SignalMapping, DebugMapping, DataType, AudioMapping, EthMapping


from . import mapping

__all__ = ['VarType', 'Enumeration', 'EnumerationEntity', 'MappingFolder', 'Mapping', 'ModelMapping', 'MeasurementMapping',
           'CalibrationMapping', 'EesMapping', 'MessageMapping', 'SignalMapping', 'DebugMapping', 'DataType', 'AudioMapping', 'EthMapping']

eSubpackages = []
eSuperPackage = None
mapping.eSubpackages = eSubpackages
mapping.eSuperPackage = eSuperPackage

Enumeration.keyValue.eType = EnumerationEntity
MappingFolder.folder.eType = MappingFolder
MappingFolder.mapping.eType = Mapping
Mapping.enumeration.eType = Enumeration
MessageMapping.signal.eType = SignalMapping
DebugMapping.children.eType = DebugMapping
DebugMapping.parent.eType = DebugMapping

otherClassifiers = [VarType, DataType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
