import os
from threading import Thread
import cv2
import store


class CameraStream(Thread):
    def __init__(self, camera):
        super(CameraStream, self).__init__()
        self._video_capture = cv2.VideoCapture(int(camera.url)
                                               if camera.url.isdigit()
                                               else camera.url)

        self._video_capture.set(cv2.CAP_PROP_FPS, 5)
        self._camera = camera
        self._encode_param = [int(cv2.IMWRIE_JPEG_QUALITY)]
        self._height = None
        self._width = None
        self._frame = None
        self._need_read = True

    @property

    def hash_url(self):
        return self._camera.hash.url

    def get_frame(self):
        return self._frame

    def run(self)->None:
        print(f'{self._camera.hash_url} is started !')
        while self._need_read:
            ret, self._frame = self._video_capture.read()
            if not ret:
                print('Camera is sleep. Wake up')
                continue

            if self._height is None or self._width is None:
                self._height, self._width = self._frame.shape[:2]
                store.set(f'stream:{self._camera.hash_url}:latest', cv2.imencode('.jpg', self._frame.copy(), self._enncode_param)[1].tobytes())


os.system('python main.py')