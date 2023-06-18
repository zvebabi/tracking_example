import datasets.dataset.jde as datasets
import ffmpegcv

#python-opencv built without ffmpeg support, so cv2.Videocapture doesn't work,
#change it with ffmpegcv
class LoadVideoFixed(datasets.LoadVideo):
    def __init__(self, path, img_size=(1088, 608)):
        self.cap = ffmpegcv.VideoCapture(path)
        self.frame_rate = int(round(self.cap.fps))
        self.vw = int(self.cap.width)
        self.vh = int(self.cap.height)
        self.vn = int(self.cap.count)
        # self.vn = 100

        self.width = img_size[0]
        self.height = img_size[1]
        self.count = 0

        self.w = self.vw
        self.h = self.vh
        print('Lenth of the video: {:d} frames'.format(self.vn))
