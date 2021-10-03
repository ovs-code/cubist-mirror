import time
import typing

import numpy as np

from .config import DEFAULT_MODEL, FPS_LOG_INTERVAL, SEGMENTATION_FG_CHANNEL
from .inputs import Input
from .models.model import Model
from .outputs import VideoFileOutput, VirtualWebcamOutput, WindowOutput
from .utils import Background, Update, OutputMode, random_image


class Controller:
    def __init__(self, style_models, segmentation_model: Model, input_controller: Input, output_path = None):
        self.model: typing.Optional[Model] = None
        self.bg_model: typing.Optional[Model] = None
        
        self.style_models: typing.List[Model] = style_models
        self.segmentation_model: Model = segmentation_model

        self.input_controller: Input = input_controller

        self.background = Background.SAME_STYLE
        self.running = False

        self.output_path = output_path

    def start(self, mode: OutputMode):
        if mode == OutputMode.VIRTUAL_WEBCAM:
            self.output_controller = VirtualWebcamOutput()
        elif mode == OutputMode.WINDOW:
            self.output_controller = WindowOutput('main', fullscreen=False)
        elif mode == OutputMode.FULLSCREEEN:
            self.output_controller = WindowOutput('main', fullscreen=True)
        elif mode == OutputMode.VIDEO:
            self.output_controller = VideoFileOutput(self.output_path)
        else:
            raise ValueError(f'Invalid operation mode {mode!r}')
        self.running = True
        self.input_controller.start()
        self.output_controller.start()
        self.segmentation_model.load()

    def destroy(self):
        self.input_controller.destroy()
        self.output_controller.destroy()
        self.segmentation_model.destroy()
        if self.model is not None:
            self.model.destroy()
        if self.bg_model is not None:
            self.bg_model.destroy()

    def _change_model(self, model_name: str):
        if self.model is not None:
            self.model.destroy()
        self.model = [m for m in self.style_models if m.name == model_name][0]
        self.model.load()

    def _change_bg_model(self, model_name: str):
        if self.bg_model is not None:
            self.bg_model.destroy()
        self.bg_model = [m for m in self.style_models if m.name == model_name][0]
        self.bg_model.load()

    def process_update(self, update_type, value):
        if update_type == Update.FG_STYLE:
            self._change_model(value)
        elif update_type == Update.BG_STYLE:
            self._change_bg_model(value)
        elif update_type == Update.BG_TYPE:
            self.background = int(value)
        elif update_type == Update.BACKGROUND:
            self.background = value
        elif update_type == Update.EXIT:
            return False
        elif update_type == Update.RESOLUTION:
            height = int(value)
            width = height // 9 * 16
            self.input_controller.resolution = (width, height)
        elif update_type == Update.START:
            self.start(mode = value)
        return True

    def step(self):
        while self.updates:
            t, value = self.updates.pop(0)
            if not self.process_update(t, value):
                return False
            if self.background != Background.NO_SEGMENTATION:
                self.noise = random_image((*self.input_controller.resolution[::-1], 3))
                if self.background == Background.DIFFERENT_STYLE:
                    self.styled_noise = self.bg_model.infer(dict(image = self.noise))['output']
        if not self.running:
            time.sleep(.1)
            return True
        try:
            inputs = self.input_controller.get_inputs()
        except IOError:
            print('Failed to read input. Shutting down ...')
            return False
        outputs = {}
        if self.background == Background.SAME_STYLE:
            seg =  self.segmentation_model.infer(inputs)['segmentation'].argmax(axis=0) == SEGMENTATION_FG_CHANNEL
            inputs['image'] = np.where(seg[..., np.newaxis], inputs['original'], self.noise)
        elif self.background == Background.DIFFERENT_STYLE:
            outputs['segmentation'] = self.segmentation_model.infer(inputs)['segmentation'].argmax(axis=0) == SEGMENTATION_FG_CHANNEL
            inputs['image'] = inputs['original']
            inputs['original'] = self.styled_noise
        else:
            inputs['image'] = inputs['original']
        outputs.update(self.model.infer(inputs))
        self.output_controller.output(inputs, outputs)
        return True

    def run(self, update_queue):
        self.updates = update_queue
        self._change_model(DEFAULT_MODEL)
        self._change_bg_model(DEFAULT_MODEL)

        if FPS_LOG_INTERVAL > 0:

            frame_times = []
            last_time = time.monotonic()
            while self.step():
                new_time = time.monotonic()
                frame_times.append(new_time-last_time)
                if len(frame_times) == FPS_LOG_INTERVAL:
                    print(FPS_LOG_INTERVAL / sum(frame_times), 'FPS')
                    frame_times = []
                last_time = new_time
        else:
            while self.step():
                pass

        self.destroy()
