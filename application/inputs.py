import cv2

class Input:
    def start(self):pass
    def get_inputs(self):pass
    def destroy(self):pass

class WebcamInput(Input):
    def __init__(self, cam_id, resolution):
        self.cam_id = cam_id
        self.resolution = resolution

    def start(self):
        self.cam = cv2.VideoCapture(self.cam_id, cv2.CAP_DSHOW)

    def get_inputs(self):
        s, img = self.cam.read()
        if not s:
            raise IOError('Could not read an image from the webcam')
        
        # opencv uses BGR color order; `cv2.cvtColor` does the necessary transformation
        resized = cv2.cvtColor(cv2.resize(img, self.resolution), cv2.COLOR_BGR2RGB)
        return {'image': resized, 'original': resized}

    def destroy(self):
        self.cam.release()

class VideoFileInput(Input):
    def __init__(self, path, resolution):
        self.path = path
        self.resolution = resolution
    def start(self):
        self.cap = cv2.VideoCapture(self.path)

    def get_inputs(self):
        s, img = self.cap.read()
        if not s:
            # Video file end
            raise IOError('Could not read a frame from the video')
        
        # opencv uses BGR color order; `cv2.cvtColor` does the necessary transformation
        resized = cv2.cvtColor(cv2.resize(img, self.resolution), cv2.COLOR_BGR2RGB)
        return {'image': resized, 'original': resized}
    def destroy(self):
        self.cap.release()