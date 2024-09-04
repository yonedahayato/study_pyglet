import sys
from pathlib import Path

GAME_DIR = str(Path(__file__).resolve().parents[1])
sys.path.append(GAME_DIR)

from game import (
    image,
    run,
    add,
)

chicken_image_file = "chicken.png"
image_player = image(chicken_image_file)

def player(p: any) -> None:
    """
    自機の処理
    """

    p.x += p.vx

def start():
    """
    ゲームの開始処理
    """
    add(player, image_player, size=0.1, 
        x=-1.1, y=0, vx=0.01, vy=0)

if __name__ == "__main__":
    run(start, 1280, 720)