import json

from .style_models import parse_torch_model_group   

parsers = {
    'torch_group': parse_torch_model_group
}


def parse_model_def(file):
    with open(file) as f:
        cfg = json.load(f)
    def_type = cfg['type']
    if def_type in parsers:
        return parsers[def_type](cfg)
    else:
        raise ValueError('Unknown model type')
