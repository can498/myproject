import traceback
from pyecore.resources import *
from pyecore.resources.xmi import XMIOptions, XMIResource
from pyecore.resources.json import JsonResource, JsonOptions


def save_model(model_obj, save_path):
    try:
        resource = XMIResource(URI(save_path), use_uuid=True)
        resource.append(model_obj)
        resource.save(options={XMIOptions.OPTION_USE_XMI_TYPE: True})
    except:
        traceback.print_exc()
        raise Exception(f"Model saved failed, path:{save_path}")

