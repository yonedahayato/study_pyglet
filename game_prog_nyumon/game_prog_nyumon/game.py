import math
import random
from pathlib import Path

import pyglet
from pyglet.window.key import ESCAPE

RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resource" / "download_pipoya"
pyglet.resource.path = [RESOURCE_DIR]

# == ウィンドウに関する機能 ==

# ウィンドウの作成
window = pyglet.window.Window()

# 画像をまとめて描画するためのバッチを作成
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    """
    ウィンドウの描画
    """
    # print("on_draw func")

    # 背景色の設定
    pyglet.gl.glClearColor(*background, 1)

    # ウィンドウのクリア
    window.clear()

    # バッチを描画
    batch.draw()

    if score_draw:
        raise Exception("on_draw func")

# == スコアに関する機能 ==

# スコアを描画するかどうか
score_draw = False

# 現在のスコアとベストスコア
score_now = score_best = 0

# スコアのラベル
score_now_label = pyglet.text.Label()
score_best_label = pyglet.text.Label(anchor_x="right")

def score(s: int = 0):
    """
    スコアの加算と取得

    Args:
        s (int, optional): 加算するスコア. デフォルトは0.

    Returns:
        int: 現在のスコア
    """

    global score_draw, score_now, score_best
    score_draw = True

    score_now = max(score_now + s, 0)

    score_best = max(score_best, score_now)

    return score_now

# == fpsに関する機能 ==

# fpsを描画するかどうか
fps_draw = False

# fpsのラベル
fps_label = pyglet.text.Label(anchor_x="center")

# == キーボードに関する機能 ==

# 現在押されているキーの一覧と、1フレーム前に押されていたキーの一覧を管理するために、空の集合を作成する
key_state = key_state_old = set()

@window.event
def on_key_press(symbol, modifiers) -> None:
    """
    キーが押されたら、現在押されているキーの一覧に追加する
    """
    key_state.add(symbol)

@window.event
def on_key_release(symbol, modifiers) -> None:
    """
    キーが離されたら、現在押されているキーの一覧から削除する
    """
    key_state.discard(symbol)

def key(k: str) -> bool:
    """
    指定したキーが現在押されていたら、True を返す
    """

    return k in key_state

def key_old(k: str) -> bool:
    """
    指定したキーが1フレーム前に押されていたら、Trueを返す
    """

    return k in key_state_old

# == 画像に関する機能 ==

def image(file: str) -> pyglet.image.AbstractImage:
    """
    画像の読み込み

    Args:
        file (str): 読み込む画像ファイルのパス

    Returns:
        pyglet.image.AbstractImage: 読み込んだ画像オブジェクト
    """
    pyglet.resource.path = [str(RESOURCE_DIR)]
    img = pyglet.resource.image(file)

    img.anchor_x = img.width//2
    img.anchor_y = img.height//2

    return img

# == カメラに関する機能 ==

# カメラの座標を (0, 0) で初期化する
camera_x = camera_y = 0

# == キャラクター実行に関する機能 ==

mover = []

# 合計の経過時間
time_sum = 0

# 最短の経過時間
time_min = 1/60 * 0.9

# 一時停止しているかどうか
pause = False

# キャラクターのクラス
class Mover:
    pass

def add(move_fun: callable,
        image: pyglet.image.TextureRegion = None,
        size: float = 0.1,
        x: int = 0,
        y: int = 0,
        vx: int = 0,
        vy: int = 0,
        **kwargs
        ) -> None:
    """
    キャラクターの追加

    Args:
        move_fun (callable): キャラクターの移動関数
        image (pyglet.image.AbstractImage, optional): キャラクターの画像. デフォルトはNone.
        size (float, optional): キャラクターの大きさ. デフォルトは0.1.
        x (int, optional): キャラクターのx座標. デフォルトは0.
        y (int, optional): キャラクターのy座標. デフォルトは0.
        vx (int, optional): キャラクターのx方向の速度. デフォルトは0.
        vy (int, optional): キャラクターのy方向の速度. デフォルトは0.
        **kwargs: キャラクターの追加に関する引数

    Returns:
        Mover: 作成したキャラクター
    """
    print("add func")
    print(f"image: {type(image)}")

    m = Mover()
    m.move = move_fun
    m.image = image

    if image:
        m.sprite = pyglet.sprite.Sprite(image, batch=batch)
        m.sprite.scale_x = m.sprite.scale_y = 0
    else:
        m.sprite = None

    m.sx = m.sy = size

    m.x, m.y = x, y
    m.vx, m.vy = vx, vy

    m.r = m.state = m.time = 0

    m.life = 1

    for k, v in kwargs.items():
        setattr(m, k, v)

    mover.append(m)

    return m

def move(dt: float) -> None:
    """
    キャラクターの移動

    Args:
        dt (float): 前回キャラクターを動かした後の経過時間

    Returns:
        None
    """
    # print("move func")
    global time_sum, time_min, pause, mover

    # 合計の経過時間に、前回からの経過時間を加算する

    time_sum += dt

    # 一時停止していなくて、かつ経過時間が最短の経過時間より大きければ,
    # キャラクターを動かす
    if (not pause) and time_sum >= time_min:
        time_sum = 0
        for m in mover:
            m.move(m)

        w, w2, h2 = window.width, window.width//2, window.height//2

        for m in mover:

            if m.sprite:
                m.sprite.image = m.image

                # スプライトのサイズを設定する
                m.sprite.scale_x = m.sx * w / m.image.width
                m.sprite.scale_y = m.sy * w / m.image.height

                # スプライトの座標を設定する
                m.sprite.x = (m.x - camera_x) * w2 + w2
                m.sprite.y = (m.y - camera_y) * w2 + h2

                # スプライトの角度を設定する
                m.sprite.rotation = -m.r * 360

        old_mover = mover

        # ライフが0より大きなキャラクターだけを取得して、新しいリストを作成する
        mover = [m for m in old_mover if m.life > 0]

        old_mover.clear()

    global score_now, fps_draw

    # エスケープキーを押したら、プログラムを終了する
    if key(ESCAPE):
        pyglet.app.exit()

def group(*move):
    """
    キャラクターの取得
    """
    for m in mover:
        if m.move in move:
            yield m

# == ゲームの実行に関する機能 ==

def run(start_fun: callable,
        w: int = window.width,
        h: int = window.height,
        bg: tuple[int] = (1, 1, 1),
        fs: bool = False,
        tc: tuple[float] = (0.5, 0.5, 0.5),
        tfn: str = "Arial") -> None:
    """
    ゲームの実行

    Args:
        start_fun (function): ゲームの開始時に呼び出される関数
        w (int, optional): ウィンドウの幅. デフォルトはwindow.width.
        h (int, optional): ウィンドウの高さ. デフォルトはwindow.height.
        bg (tuple[int], optional): 背景色 (R, G, B). デフォルトは (1, 1, 1).
        fs (bool, optional): フルスクリーンモードにするかどうか. デフォルトはFalse.
        tc (tuple[float], optional): テキストの色 (R, G, B). デフォルトは (0.5, 0.5, 0.5).
        tfn (str, optional): テキストフォントの名前. デフォルトは "Arial".

    Returns:
        None
    """
    print("run func")
    global start, background, text_color, text_font_name

    start = start_fun
    background = bg

    snl, sbl, fl = score_now_label, score_best_label, fps_label

    # 現在のスコア、ベストスコア、FPSの色を設定
    snl.color = sbl.color = fl.color = int(tc[0]*255), int(tc[1]*255), int(tc[2]*255), 255

    # 現在のスコア、ベストスコア、FPSのフォント名を設定
    snl.font_name = sbl.font_name = fl.font_name = tfn

    # ウィンドウのサイズを設定
    window.set_size(w, h)

    # フルスクリーンモードにするかどうか
    window.set_fullscreen(fs)

    start()

    pyglet.clock.schedule(move)
    pyglet.app.run()