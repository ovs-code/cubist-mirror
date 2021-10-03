# models adapted from https://github.com/pytorch/examples/tree/master/fast_neural_style,
# based on "Perceptual Losses for Real-Time Style Transfer and Super-Resolution" by Johnson et. al

import re
from os import path

import numpy as np
from torchvision import transforms, models
import torch

from .transformer_net import TransformerNet
from .model import Model

class StyleTransferModel(Model):
    def __init__(self, path, name, image):
        self.path = path
        self.name = name
        self.image = image

    def load(self):
        content_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.mul(255))
        ])
        style_model = TransformerNet()
        state_dict = torch.load(self.path)
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.cuda()
        style_model.eval()
        self.model = style_model
        self.transform = content_transform
    def destroy(self, *args):
        pass

    def infer(self, data) -> np.ndarray:
        with torch.no_grad():
            input_batch = self.transform(data['image']).unsqueeze(0).cuda()
            output = self.model(input_batch)[0].cpu().numpy()
            processed = np.clip(output, 0, 255).transpose(1, 2, 0).astype(np.uint8)
        return dict(output = processed)

class SegmentationModel(Model):
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def load(self):
        self.model = models.segmentation.deeplabv3_mobilenet_v3_large(pretrained=True)
        self.model.cuda()
        self.model.eval()
    def destroy(self, *args):
        pass
    def infer(self, data):
        input_batch = self.transform(data['image']).cuda().unsqueeze(0)
        with torch.no_grad():
            seg = self.model(input_batch)['out'][0].cpu().numpy()
        return dict(segmentation = seg)

def parse_torch_model_group(cfg):
    models = []
    for v in cfg['variants']:
        model = StyleTransferModel(path.join('assets/models/pretrained',
                          cfg['name'], v['file']), name=v['name'], image=v['image'])
        models.append(model)
    return models