"""Definition of meta model 'ctc'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'ctc'
nsURI = 'com.hirain.tae.ctc'
nsPrefix = 'ctc'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


@abstract
class Ctc(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    description = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    modify = EAttribute(eType=EBoolean, derived=False, changeable=True, default_value=False)
    skip = EAttribute(eType=EBoolean, derived=False, changeable=True, default_value=False)
    report = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, name=None, description=None, modify=None, skip=None, report=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if modify is not None:
            self.modify = modify

        if skip is not None:
            self.skip = skip

        if report is not None:
            self.report = report


class DataStore(EObject, metaclass=MetaEClass):

    parameters = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)
    algorithmName = EAttribute(eType=EString, derived=False, changeable=True)
    options = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)

    def __init__(self, *, parameters=None, algorithmName=None, options=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if parameters:
            self.parameters.extend(parameters)

        if algorithmName is not None:
            self.algorithmName = algorithmName

        if options:
            self.options.extend(options)


class CtcMap(Ctc):

    value = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value


class CtcScript(Ctc):

    script = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, script=None, **kwargs):

        super().__init__(**kwargs)

        if script is not None:
            self.script = script


class CtcGenerater(Ctc):

    limit = EAttribute(eType=EString, derived=False, changeable=True)
    filterCondition = EAttribute(eType=EString, derived=False, changeable=True)
    dataStore = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, limit=None, dataStore=None, filterCondition=None, **kwargs):

        super().__init__(**kwargs)

        if limit is not None:
            self.limit = limit

        if filterCondition is not None:
            self.filterCondition = filterCondition

        if dataStore is not None:
            self.dataStore = dataStore
