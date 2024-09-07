import sys
from pathlib import Path

GAME_DIR = str(Path(__file__).resolve().parents[1])
sys.path.append(GAME_DIR)

from game import PlayerApp

if __name__ == '__main__':
    PlayerApp().run()