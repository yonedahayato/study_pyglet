import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, 
    ReferenceListProperty, 
    ObjectProperty
)
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.clock import Clock

from pathlib import Path
from random import randint

# from kivy.lang import Builder
# Builder.load_file('./pyglet_to_kivy/player.kv')

# == ウィンドウに関する設定 ==

Window.size = (1280, 720)

# == FPSに関する設定 ==

FPS: float = 60.0

# == 画像に関する設定 ==

# RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resource" / "download_pipoya"
RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resource"

class PongBall(Widget):
    """
    ボールの物体
    """
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    v_operation = 20

    def move(self, operation: str = ""):
        """
        等速直線運動の場合の動く処理
        """
        if operation == "up":
            self.pos = [self.pos[0], self.pos[1] + self.v_operation]
        elif operation == "down":
            self.pos = [self.pos[0], self.pos[1] - self.v_operation]
        elif operation == "left":
            self.pos = [self.pos[0] - self.v_operation, self.pos[1]]
        elif operation == "right":
            self.pos = [self.pos[0] + self.v_operation, self.pos[1]]
        else:
            self.pos: kivy.properties.ObservableReferenceList = Vector(*self.velocity) + self.pos

class CharacterBall(Image):
    """
    キャラクターのオブジェクト

    Attributes:
        velocity_x (NumericProperty): X軸方向の速度
        velocity_y (NumericProperty): Y軸方向の速度
        velocity (ReferenceListProperty): 速度ベクトル
        angle (NumericProperty): 回転角度
        shrinking_speed (float): オブジェクトの縮小速度
        life (int): キャラクターのライフ
            0 になると削除される
    """
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    angle = NumericProperty(0)
    shrinking_speed: float = 0.001
    life: int = 1
    min_size: int = 150

    def move(self):
        """
        1 step における動作処理

        Note:
            1. pos の更新
            2. angle の更新
            3. size の更新
            4. life の更新
        """
        self.pos: kivy.properties.ObservableReferenceList = Vector(*self.velocity) + self.pos
        self.angle += 1

        shrinking_rate = 1 - self.shrinking_speed
        size_x = self.size[0] * shrinking_rate
        size_y = self.size[1] * shrinking_rate
        self.size = [size_x, size_y]

        if size_x < self.min_size or size_y < self.min_size:
            self.life = 0

    def delete(self):
        self.size = [0, 0]

class PlayerGame(Widget):
    """
    ゲームの実行を管理
    """
    ball = ObjectProperty(None)
    character_ball = ObjectProperty(None)
    cho_cho = ObjectProperty(None)

    keys = []
    movers = []

    def __init__(self, **kwargs):
        super(PlayerGame, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')

        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass

        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        if keycode[1] in ["up", "down", "left", "right"]:
            self.keys.append(keycode[1])

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def set_image_path(self,
                       object: ObjectProperty,
                       image_name: str = "chicken.png"):
        """
        画像のパスを設定する
        """
        image_path = RESOURCE_DIR / image_name
        object.source = str(image_path)
        return object

    def set_images_path(self):
        """
        画像の設定
        """
        self.character_ball = self.set_image_path(self.character_ball, "by_max.png")
        self.cho_cho = self.set_image_path(self.cho_cho, "chocho.webp")

    def serve_ball(self, ball):
        ball.center = self.center
        ball.velocity = Vector(4, 0).rotate(randint(0, 360))

        return ball

    def serve_balls(self):
        self.ball.center = self.center
        # self.ball.center = [0, Window.size[1] / 2]

        # self.ball.velocity = Vector(4, 0).rotate(0)
        # self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
        self.ball.velocity = (0, 0)

        self.character_ball = self.serve_ball(self.character_ball)
        self.cho_cho = self.serve_ball(self.cho_cho)

    def updata_each_ball(self, ball):
        """
        ボールを動かす
        """
        ball.move()

        # bounce off top and bottom
        if (ball.y < 0) or (ball.top > self.height):
            ball.velocity_y *= -1

        # bounce off left and right
        if (ball.x < 0) or (ball.right > self.width):
            ball.velocity_x *= -1

        return ball

    def update(self, dt) -> None:
        """
        状態を更新する
        """
        if len(self.keys) != 0:
            key = self.keys.pop()
            print(f"update key: {key}")

            if key in ["up", "down", "left", "right"]:
                self.ball.move(operation=key)

        self.ball = self.updata_each_ball(self.ball)

        if self.character_ball.life == 0:
            self.character_ball.delete()
        else:
            self.character_ball = self.updata_each_ball(self.character_ball)
        self.cho_cho = self.updata_each_ball(self.cho_cho)

class PlayerApp(App):
    def build(self):
        game = PlayerGame()
        game.set_images_path()
        game.serve_balls()
        Clock.schedule_interval(game.update, 1.0/FPS)
        return game

if __name__ == '__main__':
    PlayerApp().run()