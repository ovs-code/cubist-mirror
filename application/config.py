from .utils import OutputMode

# File which stores a list of all styles
MODEL_CONFIG_FILE = 'assets/models/defs/style_models.json'

# the port to launch the web server for the UI
DEFAULT_PORT = 8123

# which channel is the foreground (person) channel in the segmentation model
SEGMENTATION_FG_CHANNEL = 15

# the model to select at start
DEFAULT_MODEL = 'EMPTY'

# log every n frames. Set to 0 to disable this output
FPS_LOG_INTERVAL = 0

# the id of the camera device to use.
# TODO: A device selector on the launch screen would be nicer
CAM_ID = 0

# the mode to launch the application in if the launch page is skipped
DEFAULT_MODE = OutputMode.WINDOW

# directory for the html templates
TEMPLATE_DIR = 'client/templates'

# the maximum fps to run on. This is probably limited by the webcam.
FPS = 30