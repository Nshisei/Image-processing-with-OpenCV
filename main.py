import cv2
import mediapipe as mp
import numpy as np
import pyaudio
from utils import *
from handsign import goukakyu, show_sign
# from FaceMeshModule import FaceMeshDetector
from FaceMeshModule import FaceDetector
from cvzone.HandTrackingModule import HandDetector
import subprocess
from time import sleep

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input = True,
    frames_per_buffer = 1024
)

cap = cv2.VideoCapture(0) # カメラ
cap.set(3, 640) # 画面サイズ 幅640
cap.set(4, 360) # 画面サイズ 高さ360
# detector_f = FaceMeshDetector(maxFaces=1) # 顔検出インスタンス
detector_f = FaceDetector() # 顔検出インスタンス
detector_h = HandDetector(detectionCon=0.8, maxHands=2) # 手検出インスタンス
page = 1    # 表示する火の画像番号
pos = [0,0] # 火の画像を表示する位置

fire_direction = None   # 火を吹く方向{front, left, right, None}
next_sign = 'hebi'      # 次に検出するべき印{hebi, hituji, saru, inoshishi, uma, tora, fire}
show_time = 0           # 印を検出したとき、検出した印の漢字を表記する時間

while cap.isOpened():
    success, image = cap.read()
    image, faces = detector_f.findFaceMesh(image,draw=False)
    hands = detector_h.findHands(image,draw=False)
    if faces: # 顔検出出来た時
        face = faces[0]
        angles = detector_f.faceDirection(image, draw=False) # 顔の方向検出
        x,y,z = angles

        if next_sign == 'fire' and fire_direction == None: # 印を組み終えてかつ、火を噴く前
            data = stream.read(1024)
            volume = np.frombuffer(data, dtype="int16") / 32768.0
            # print(volume.max())
            if volume.max() > 0.1: # 一定音量を超えた時のみ表示 
                subprocess.Popen(['python', 'sound.py', 'fire']) # 火を吹く音
                sleep(0.15)
                if y < -10:
                    fire_direction = 'left' # 方向
                    pos = [face[13][0], int(face[13][1]-(4*x))] # 口元の座標±上下方向の顔の向き
                    rotate = x
                elif y > 10:
                    fire_direction = 'right'
                    pos = [face[13][0], int(face[13][1]-(4*x))]
                    rotate = x
                else:
                    fire_direction = 'front'
                    pos = [0,0]
                    rotate = 0

    if fire_direction != None: # 火を吹く方向が決まったとき、火を表示する
        image, page = fire(image, page, pos, fire_direction, rotate) # 火を表示する関数
        if page == 1: # 火の画像を一通り表示し終わったら、リセット
            fire_direction = None
            next_sign = 'hebi'

    if len(hands) >= 1: # 手が一つでも検出できた時
        pre = next_sign
        next_sign = goukakyu(hands, next_sign) 
        if pre != next_sign: # 印を検出できた時、印を表示する時間をセット
            show_time = 20
    
    if show_time != 0: # 印の表示時間が0出ないとき印を表示
        show_time -= 1
        if next_sign == 'fire' and show_time < 11: # 寅の印を検出した時は、「寅」の次に「火遁・豪火球の術」を表示する
            if show_time == 10: # 「火遁・豪火球の術」を表示するタイミングで効果音を出す
                subprocess.Popen(['python', 'sound.py', 'zyutu'])
                sleep(0.15)
            sign = cv2.imread(f'./image/zyutu.png',cv2.IMREAD_UNCHANGED) #「火遁・豪火球の術」
            image = cvzone.overlayPNG(image, sign, [0,0])
        else:
            image = show_sign(image,next_sign)

    cv2.imshow('Image', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()