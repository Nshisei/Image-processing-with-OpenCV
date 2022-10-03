# サブプロセスから音声ファイルを再生するファイル
import sys
from playsound import playsound
file = sys.argv[1]
playsound(f"./sound/{file}.mp3")