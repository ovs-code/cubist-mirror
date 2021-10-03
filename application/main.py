import multiprocessing
import webbrowser
from typing import Optional

from application.utils import Update

from .config import CAM_ID, DEFAULT_PORT, MODEL_CONFIG_FILE
from .controller import Controller
from .inputs import VideoFileInput, WebcamInput
from .models.config import parse_model_def
from .models.model import EmptyModel
from .models.style_models import SegmentationModel
from .server import WebServer
from .utils import OutputMode, Update, get_video_resolution


def run(port: Optional[int] = None):
    if port is None:
        port = DEFAULT_PORT

    # The main application and the web server for control run in a different process.
    # This is necessary for the web server to be responsive because of GIL.
    # Communication happens through a single list, called `update_queue`
    with multiprocessing.Manager() as manager:
        update_queue = manager.list()

        style_models = parse_model_def(MODEL_CONFIG_FILE)
        style_models.append(EmptyModel())
        data = [(model.name, model.image)for model in style_models]

        segmentation_model = SegmentationModel()

        input_controller = WebcamInput(CAM_ID, (1920//2, 1080//2))
        controller = Controller(
            style_models, segmentation_model, input_controller)

        server = WebServer(data, port)

        server_process = multiprocessing.Process(target=server.run, args=(update_queue, ))
        controller_process = multiprocessing.Process(target=controller.run, args=(update_queue, ))
        server_process.start()
        controller_process.start()

        # Open the start page in a new browser tab.
        # Might want to disable this if the browser is started separately (i.e. in kiosk mode)
        webbrowser.open(f'http://localhost:{DEFAULT_PORT}/launch')

        # wait for the processes to end
        controller_process.join()
        server_process.join()

def stylize_video(input_path, output_path, fg_style, background:int, scaling, bg_style=None):
    style_models = parse_model_def(MODEL_CONFIG_FILE)
    style_models.append(EmptyModel())

    segmentation_model = SegmentationModel()
    height, width = get_video_resolution(input_path)
    scaled_width = width // scaling
    scaled_height = height // scaling
    input_controller = VideoFileInput(input_path, (scaled_width, scaled_height))
    controller = Controller(
        style_models, segmentation_model, input_controller, output_path=output_path)
    updates = [
        (Update.FG_STYLE, fg_style),
        (Update.BG_STYLE, 'hundertwasser'),
        (Update.BACKGROUND, background),
    ]
    controller.start(OutputMode.VIDEO)
    controller.run(updates)


def list_styles():
    style_models = parse_model_def(MODEL_CONFIG_FILE)
    return [model.name for model in style_models]
