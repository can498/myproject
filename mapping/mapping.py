"""Definition of meta model 'mapping'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'mapping'
nsURI = 'com.hirain.tae.model.mapping'
nsPrefix = 'mapping'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
VarType = EEnum('VarType', literals=['Scalar', 'Vector',
                                     'Matrix', 'Curve', 'Map', 'VectorItem', 'MatrixItem'])

DataType = EEnum('DataType', literals=['Int', 'float', 'array',
                                       'char', 'enum', 'structure', 'point', 'cfile', 'bool', 'union'])


class Enumeration(EObject, metaclass=MetaEClass):

    keyValue = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, keyValue=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if keyValue:
            self.keyValue.extend(keyValue)


class EnumerationEntity(EObject, metaclass=MetaEClass):

    key = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


class MappingFolder(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    folder = EReference(ordered=True, unique=True, containment=True, upper=-1)
    mapping = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, folder=None, mapping=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if folder:
            self.folder.extend(folder)

        if mapping:
            self.mapping.extend(mapping)


class Mapping(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    deviceName = EAttribute(eType=EString, derived=False, changeable=True)
    path = EAttribute(eType=EString, derived=False, changeable=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    reference = EAttribute(eType=EString, derived=False, changeable=True, default_value=' ')
    enumeration = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, name=None, deviceName=None, path=None, description=None, reference=None, enumeration=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if deviceName is not None:
            self.deviceName = deviceName

        if path is not None:
            self.path = path

        if description is not None:
            self.description = description

        if reference is not None:
            self.reference = reference

        if enumeration is not None:
            self.enumeration = enumeration


class ModelMapping(Mapping):

    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    dimension = EAttribute(eType=EString, derived=False, changeable=True)
    raster = EAttribute(eType=EString, derived=False, changeable=True)
    unit = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, dataType=None, dimension=None, raster=None, unit=None, **kwargs):

        super().__init__(**kwargs)

        if dataType is not None:
            self.dataType = dataType

        if dimension is not None:
            self.dimension = dimension

        if raster is not None:
            self.raster = raster

        if unit is not None:
            self.unit = unit


class MeasurementMapping(Mapping):

    varType = EAttribute(eType=VarType, derived=False, changeable=True)
    raster = EAttribute(eType=EString, derived=False, changeable=True)
    dimension = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, varType=None, raster=None, dimension=None, **kwargs):

        super().__init__(**kwargs)

        if varType is not None:
            self.varType = varType

        if raster is not None:
            self.raster = raster

        if dimension is not None:
            self.dimension = dimension


class CalibrationMapping(Mapping):

    varType = EAttribute(eType=VarType, derived=False, changeable=True)
    dimension = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, varType=None, dimension=None, **kwargs):

        super().__init__(**kwargs)

        if varType is not None:
            self.varType = varType

        if dimension is not None:
            self.dimension = dimension


class EesMapping(Mapping):

    potential = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)

    def __init__(self, *, potential=None, **kwargs):

        super().__init__(**kwargs)

        if potential:
            self.potential.extend(potential)


class MessageMapping(Mapping):

    shouldsignals = EAttribute(eType=EString, derived=False, changeable=True)
    signal = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, signal=None, shouldsignals=None, **kwargs):

        super().__init__(**kwargs)

        if shouldsignals is not None:
            self.shouldsignals = shouldsignals

        if signal:
            self.signal.extend(signal)


class SignalMapping(Mapping):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class DebugMapping(Mapping):

    datatype = EAttribute(eType=DataType, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)
    scope = EAttribute(eType=EString, derived=False, changeable=True)
    otherInfo = EAttribute(eType=EString, derived=False, changeable=True)
    children = EReference(ordered=True, unique=True, containment=True, upper=-1)
    parent = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, datatype=None, children=None, value=None, parent=None, scope=None, otherInfo=None, **kwargs):

        super().__init__(**kwargs)

        if datatype is not None:
            self.datatype = datatype

        if value is not None:
            self.value = value

        if scope is not None:
            self.scope = scope

        if otherInfo is not None:
            self.otherInfo = otherInfo

        if children:
            self.children.extend(children)

        if parent is not None:
            self.parent = parent


class AudioMapping(Mapping):

    dataType = EAttribute(eType=EString, derived=False, changeable=True)
    dimension = EAttribute(eType=EString, derived=False, changeable=True)
    raster = EAttribute(eType=EString, derived=False, changeable=True)
    unit = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, dataType=None, dimension=None, raster=None, unit=None, **kwargs):

        super().__init__(**kwargs)

        if dataType is not None:
            self.dataType = dataType

        if dimension is not None:
            self.dimension = dimension

        if raster is not None:
            self.raster = raster

        if unit is not None:
            self.unit = unit


class EthMapping(Mapping):

    ethDataType = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, ethDataType=None, **kwargs):

        super().__init__(**kwargs)

        if ethDataType is not None:
            self.ethDataType = ethDataType
