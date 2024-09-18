import sys
from pathlib import Path
import math
import random

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
    group,
)

from crash import (
    new_crash,
)

SW, SH = 1, 9/16

chicken_image_file = "chicken.png"
image_player = image(chicken_image_file)
image_enemy = image("car.png")

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

    # 時期との衝突反転
    # すべての敵に対して順番に行う
    for e in group(enemy):
        dist: float = math.dist((p.x, p.y), (e.x, e.y))
        min_dist: float = (p.sx + e.sx) * 0.5
        if dist < min_dist:
            new_crash(p.x, p.y, 0.01, 20, 0.98)

            p.life = 0

def enemy(e):
    """
    敵の動き
    """
    e.x += e.vx

    e.time += 1

    # 的が画面の外に出たら消去する
    if abs(e.x) > (SW + e.sx):
        e.life = 0

def stage(s):
    """
    敵の作成などのステージを作成する
    """

    if random.random() < 0.05:
        size = 0.1
        side = random.choice([-1, 1])

        y = random.uniform(-SH + size, SH - size)
        add(enemy, image_enemy, size, (SW + size) * side, y, -0.01 * side)


def start():
    """
    ゲームの開始処理
    """
    add(stage)
    add(player, image_player, size=0.09, 
        x=0, y=0, vx=0, vy=0)

if __name__ == "__main__":
    print("player1.py")
    run(start, 1280, 720)