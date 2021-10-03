import cv2
import numpy as np
import pyvirtualcam
import time

from .config import FPS


def generate_final_image(inputs, outputs):
    if 'segmentation' in outputs:
        out_seg = outputs['segmentation']
        result = np.where(out_seg[..., np.newaxis],
                          outputs['output'], inputs['original'])
    else:
        result = outputs['output']
    return result


class Output:
    def start(self):
        pass

    def output(self, inputs, outputs):
        pass

    def destroy(self):
        pass


class WindowOutput(Output):
    """Class for handling output to a - possible fullscreen - window"""

    def __init__(self, winname, fullscreen):
        self.winname = winname
        self.fullscreen = fullscreen

    # TODO: I/O could be async to run the models all the time.
    def output(self, *args):
        result = generate_final_image(*args)

        # opencv uses BGR color order; `cv2.cvtColor` does the necessary transformation
        cv2.imshow(self.winname, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        return cv2.waitKey(1)

    def start(self):
        if self.fullscreen:
            cv2.namedWindow(self.winname, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(
                self.winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.namedWindow(self.winname)

    def destroy(self):
        cv2.destroyWindow(self.winname)


class VirtualWebcamOutput(Output):
    """Class for handling output to an OBS virtual camera device.
    Can be used for recording or video conferences

    resolution is inferred from the given outputs"""

    def __init__(self):
        self.shape = None
        self.cam = None

    def output(self, *args):
        result = generate_final_image(*args)

        # Create a new virtual camera if there is no old one or the resolution has changed
        if self.cam is None or result.shape != self.shape:
            self.destroy()
            height, width, _ = self.shape = result.shape
            self.cam = pyvirtualcam.Camera(width=width, height=height, fps=FPS)

        self.cam.send(result)

    def destroy(self):
        if self.cam is not None:
            self.cam.close()
            time.sleep(1)


class VideoFileOutput(Output):
    def __init__(self, path):
        self.path = path
        self.out = None

    def output(self, *args):
        result = generate_final_image(*args)
        if self.out is None:
            height, width, _ = result.shape
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.out = cv2.VideoWriter(self.path, fourcc, FPS, (width, height))
        self.out.write(cv2.cvtColor(result, cv2.COLOR_RGB2BGR))

    def destroy(self):
        self.out.release()
