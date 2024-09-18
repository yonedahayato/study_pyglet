from game import (
    image,
    add,
)
import math

image_crash = image("crash.png")

def crash(c):
    
    # 座標に速度を加算して移動する
    c.x += c.vx
    c.y += c.vy

    # 動いている感じを出すために回転させる
    c.r += 0.2

    # サイズに縮小率を乗算して、次第にサイズを小さくする
    c.sx *= c.vs
    c.sy *= c.vs

    # サイズが一定より小さくなったら削除する
    if c.sx < 0.01:
        c.life = 0

def new_crash(x, y, v, n, vs):
    """
    爆発の生成
    """

    for i in range(n):

        # 破片を発射する角度を決定する
        rad = i / n * math.pi * 2

        # 破片の速度を決定する
        # v ベクトルを x 方向と y 方向に分離する
        vx = math.cos(rad) * v
        vy = math.sin(rad) * v

        add(crash, image_crash, 0.04, x, y, vx, vy, vs=vs)