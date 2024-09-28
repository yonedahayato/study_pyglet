import numpy as np
import cv2

from PIL import Image

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle


class MyApp(App):
    title = "opencv on kivy"

    def build(self):
        img = cv2.imread('/Users/yonedahayato/Downloads/Book.jpg',1)

        if img is None:
            print('load image')
            sys.exit(1)

        # 表示確認用
        cv2.imshow('opencv_normal', img)


        widget = Widget()

        ''' pattern1 (openCVの機能で表示)  '''
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # openCVの色の並びはBGRなのでRGBに直す
        img2 = cv2.flip(img2, 0)    # Kivyの座標の原点は左下なので上下反転する

        # OpenCVの座標shapeは「高さ」、「幅」、「チャンネル」の順番 Kivyのsizeは(幅、高さ)なので逆にする必要がある
        texture = Texture.create(size=(img2.shape[1], img2.shape[0]))
        texture.blit_buffer(img2.tostring())

        with widget.canvas: # 描画
            Rectangle(texture=texture ,pos=(0, 0), size=(img2.shape[1], img2.shape[0]))
