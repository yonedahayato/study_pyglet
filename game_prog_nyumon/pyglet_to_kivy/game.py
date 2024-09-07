from kivy.app import App
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

# from kivy.lang import Builder
# Builder.load_file('./pyglet_to_kivy/player.kv')

# == ウィンドウに関する設定 ==

Window.size = (1280, 720)

# == FPSにかんする設定 ==

FPS: float = 60.0

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PlayerGame(Widget):
    pass


class PlayerApp(App):
    def build(self):
        game = PlayerGame()
        Clock.schedule_interval(game.update, 1.0/FPS)
        return game


if __name__ == '__main__':
    PlayerApp().run()