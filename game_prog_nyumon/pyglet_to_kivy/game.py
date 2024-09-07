from kivy.app import App
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.clock import Clock

from pathlib import Path

# from kivy.lang import Builder
# Builder.load_file('./pyglet_to_kivy/player.kv')

# == ウィンドウに関する設定 ==

Window.size = (1280, 720)

# == FPSに関する設定 ==

FPS: float = 60.0

# == 画像に関する設定 ==

# RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resource" / "download_pipoya"
RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resource"

# class PongBall(Widget):
class PongBall(Image):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PlayerGame(Widget):
    """
    ゲームの実行を管理
    """
    ball = ObjectProperty(None)

    def set_image_path(self, image_name: str = "chicken.png"):
        """
        画像のパスを設定する
        """
        image_path = RESOURCE_DIR / image_name
        self.ball.source = str(image_path)

    def serve_ball(self):
        print("serve_ball func")
        print(f"center: {self.center}")

        # self.ball.center = self.center
        self.ball.center = [0, Window.size[1] / 2]
        self.ball.velocity = Vector(4, 0).rotate(0)

    def update(self, dt):
        self.ball.move()

class PlayerApp(App):
    def build(self):
        game = PlayerGame()
        game.set_image_path("by_max.png")
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/FPS)
        return game


if __name__ == '__main__':
    PlayerApp().run()