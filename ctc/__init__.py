
from .ctc import getEClassifier, eClassifiers
from .ctc import name, nsURI, nsPrefix, eClass
from .ctc import Ctc, CtcMap, CtcScript, CtcGenerater, DataStore


from . import ctc

__all__ = ['Ctc', 'CtcMap', 'CtcScript', 'CtcGenerater', 'DataStore']

eSubpackages = []
eSuperPackage = None
ctc.eSubpackages = eSubpackages
ctc.eSuperPackage = eSuperPackage

CtcGenerater.dataStore.eType = DataStore

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
