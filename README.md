# OpenCVを使った映像処理プログラムの作成

## 概要
学部3年生の情報システム工学演習 IIの課題で作成したもの
NARUTO世界の火遁 豪華球の術を再現するアプリケーション

main.pyもしくは、main.ipynbを実行すると、カメラが立ち上がる。
カメラに対してやや斜めに向かい合う。
その後、「巳」「未」「申」「午」「寅」の順で印を組む。
「火遁・豪火球の術」という文字が出たら任意の方向を向いて一気に息を吹きだす。
この時、うまく反応しなければイヤホンマイクなどをつけたり、息の代わりに「ワー」という声を出すとよい。一度術が発動したら、もう一度印をはじめから組む必要がある。終了するときは、Escキーを入力する。
（私の環境では、jupyter notebookでEscで終了すると画面が残り続けてしまうので、main.pyを実行するのがおすすめです。）

```
pip install numpy==1.21.1
pip install opencv-python==4.5.5.62
pip install mediapipe==0.8.9.1
pip install cvzone==1.5.4
pip install pyaudio==0.2.11
pip install playsound==1.2.2
```

## プログラム構成
* 手を検出（cvzone.HandTrackingModule）
* 指の位置から印を検出・表示（Handsign.py）
* 顔の検出・方向の計算（FaceMeshModule.py）
* 火・その他画像の表示（utils.py）
* 効果音 （sound.py）
* その他・全体の統合（08D19096.ipynb）


## 内部使用

![内部使用](https://user-images.githubusercontent.com/103732456/193593827-97d774bf-1445-4903-bc6f-2d67ad1685a7.png)

## 実行結果
### 術の発動前印の実行
![一連](https://user-images.githubusercontent.com/103732456/193596927-32716812-1498-49cf-a621-a4c96f032fb2.png)

### 術発動時の出力
![術一覧](https://user-images.githubusercontent.com/103732456/193596902-7cc48855-8cc0-4c1b-9a55-3020317d420f.png)

## 参考
参考文献
[1] MediaPipe Hands-Google, https://google.github.io/mediapipe/solutions/hands.

[2] CVZone-GitHub, https://github.com/cvzone.

[3] Head Pose Estimation with MediaPipe and OpenCV in Python - OVER 100 FPS!!!, https://www.youtube.com/watch?v=-toNMaS4SeQ&t=550s.

[4]【Python】OpenCV で 画 像 を 合成 す る–addWeighted,bitwise 演算,ROI, https://code-graffiti.com/blending-images-with-opencv-in-python/.

[5] 吹き出す炎-ニコニ・コモンズ, https://commons.nicovideo.jp/material/nc193929.

[6]【 素 材 】火 fire, https://www.youtube.com/watch?v=XsjppibitCo&ab_channel=mokeyta.

[7] 戦 闘 [1]-効 果 音 ラ ボ 火 炎 魔 法 2.mp3,https://soundeffect-lab.info/sound/battle/mp3/magic-flame2.mp3.

[8] ナルト 忍術 発動音, https://www.youtube.com/watch?v=UO4sZ3iYuTE&ab_channel=ふらっとサウンド channel.

[9] ナルト 忍術 中・終印音, https://www.youtube.com/watch?v=qaOTdQfht6k&ab_channel=ふらっとサウンド channel