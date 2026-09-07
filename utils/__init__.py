from .save_model import save_model


def load_model_root(model_file_path):
    """按需加载反序列化功能，保存模型时不要求加载全部外部元模型。"""
    from .load_model import load_model_root as _load_model_root

    return _load_model_root(model_file_path)
