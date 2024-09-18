import sys
from pathlib import Path
from pyglet.window.key import (
    LEFT,
    RIGHT,
    UP,
    DOWN,
)


GAME_DIR = str(Path(__file__).resolve().parents[1])
sys.path.append(GAME_DIR)

from game import (
    add, 
    image, 
    run,
    Mover,
    key,
)

SW, SH = 1, 9/16

chicken_image_file = "chicken.png"
image_player = image(chicken_image_file)

def player(p: Mover) -> None:
    """
    自機の処理
    """

    v: float = 0.01

    if key(LEFT):
        p.x -= v

    if key(RIGHT):
        p.x += v

    if key(UP):
        p.y += v

    if key(DOWN):
        p.y -= v

    p.x = max(-SW + p.sx, min(SW - p.sx, p.x))
    p.y = max(-SH + p.sy, min(SH - p.sy, p.y))

def start():
    """
    ゲームの開始処理
    """
    print("start func")
    add(player, image_player, size=0.09, 
        x=0, y=0, vx=0, vy=0)

if __name__ == "__main__":
    print("player1.py")
    run(start, 1280, 720)