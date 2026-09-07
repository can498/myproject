import traceback
from pyecore.resources import ResourceSet, URI

import generator
import testcase
import mapping
import ctc
# import testplan
# import dataAnalysis
# import globalvariable
# import taeconfig



def load_model_root(model_file_path):
    try:
        rset = ResourceSet()
        rset.metamodel_registry[testcase.nsURI] = testcase
        rset.metamodel_registry[generator.nsURI] = generator
        rset.metamodel_registry[mapping.nsURI] = mapping
        rset.metamodel_registry[ctc.nsURI] = ctc
        # rset.metamodel_registry[testplan.nsURI] = testplan
        # rset.metamodel_registry[dataAnalysis.nsURI] = dataAnalysis
        # rset.metamodel_registry[globalvariable.nsURI] = globalvariable
        # rset.metamodel_registry[taeconfig.nsURI] = taeconfig
        resource = rset.get_resource(URI(model_file_path))
        model_root = resource.contents[0]
        return model_root
    except:
        traceback.print_exc()
        raise Exception(f"Model file loading failed ! path: {model_file_path}")


