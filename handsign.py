import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import cvzone
import subprocess
from time import sleep
cam_w, cam_h = 640, 480

# 巳の印を検出
# 検出できていれば、True。そうでなければFalse
# 条件：
# ・手が上向き（親指の付け根が手首の座標より上）
# ・各指の先端がその指の第二関節の座標より下
def hebi(hands):
    hand = hands[0]
    lmList = hand["lmList"]
    bbox = hand["bbox"]
    if lmList[0][1] > lmList[1][1]: # 手が上向き
        if not (lmList[8][1] < lmList[8-2][1]): # 人差し指の先端が第二関節より下にある
            if not (lmList[12][1] < lmList[12-2][1]): # 中指の先端が第二関節より下にある
                if not (lmList[16][1] < lmList[16-2][1]): # 薬指の先端が第二関節より下にある
                    if not (lmList[20][1] < lmList[20-2][1]): # 小指の先端が第二関節より下にある
                        # print('hebi')
                        return True
    return False                        

# 未or寅の印を検出
# 検出できていれば、True。そうでなければFalse
# 条件：
# ・手が上向き（親指の付け根が手首の座標より上）
# ・人差し指と中指の先端がその指の第二関節の座標より上
# ・薬指と小指の先端がその指の第二関節の座標より下
def hituji(hands):
    hand = hands[0]
    lmList = hand["lmList"]
    bbox = hand["bbox"]
    if lmList[0][1] > lmList[1][1]: # 手が上向き
        if lmList[8][1] < lmList[8-2][1]: # 人差し指が立っている
            if lmList[12][1] < lmList[12-2][1]: # 人差し指が立っている
                if not lmList[16][1] < lmList[16-2][1]:
                    if not lmList[20][1] < lmList[20-2][1]:
                        # print('hituji')
                        return True
    return False                        

# 申の印を検出
# 検出できていれば、True。そうでなければFalse
# 条件：
# ・手が横向き (手も高さより幅の方が大きい)
# ・手首の座標が親指付け根より上
def saru(hands):
    hand = hands[0]
    lmList = hand["lmList"]
    xmin, ymin, boxW, boxH = hand["bbox"]
    if boxW > boxH: # 手が横向き
        if lmList[0][1] < lmList[1][1]: # 手首の座標が親指付け根より上
            # print('saru')
            return True
    return False            

# 亥の印を検出
# 検出できていれば、True。そうでなければFalse
# 条件：
# ・手が上向き（親指の付け根が手首の座標より上）
# ・各指の先端がその指の第二関節の座標より上
def inoshishi(hands):
    hand = hands[0]
    lmList = hand["lmList"]
    xmin, ymin, boxW, boxH = hand["bbox"]
    if lmList[0][1] < lmList[1][1]: # 手が上向き
        if lmList[8][1] < lmList[8-2][1]: # 人差し指の先端が第二関節より上にある
            if lmList[12][1] < lmList[12-2][1]: # 中指の先端が第二関節より上にある
                if lmList[16][1] < lmList[16-2][1]: # 薬指の先端が第二関節より上にある
                    if lmList[20][1] < lmList[20-2][1]: # 小指指の先端が第二関節より上にある
                        # print('inoshishi')
                        return True
    return False                        

# 午の印を検出
# 検出できていれば、True。そうでなければFalse
# 条件：
# ・両手が検出できている
# ・手が横向き(どちらの手も高さより幅の方が大きい)
# ・人差し指どうしの距離が一定以下（カメラからの距離によらないように両手を合わせた幅に対する割合になっている）
def uma(hands):
    # 右手と左手を格納
    if hands[0]["type"] == "right":
        righthand = hands[0]
        lefthand = hands[1]
    else:
        righthand = hands[1]
        lefthand = hands[0]
    leftlmList = lefthand["lmList"]
    rightlmList = righthand["lmList"]
    finger_length = math.hypot(leftlmList[8][0] - rightlmList[8][0] , leftlmList[8][1]  - rightlmList[8][1]) # 右手首の座標と左手首の座標間の距離
    hand_length = math.hypot(leftlmList[0][0] - rightlmList[0][0] , leftlmList[0][1]  - rightlmList[0][1]) # 右手人差し指と左人差し指の距離
    if lefthand["bbox"][2] > lefthand["bbox"][3]: # 左手が横向き（幅>高さ）
        if righthand["bbox"][2] > righthand["bbox"][3]: # 右手が横向き（幅>高さ）
            if (finger_length/hand_length) < 0.04: # 人差し指間の距離/手首間距離の値が一定以下
                # print('uma')
                return True
    return False                

# 手の形から次認識するべき印を検出できているかを判定
# 検出できているときは、next_signを更新。効果音を出力する
def goukakyu(hands, next_sign):
    if next_sign == 'hebi':
        if hebi(hands):
            subprocess.Popen(['python', 'sound.py', 'handsign'])
            sleep(0.15)
            return 'hituji'
    elif next_sign == 'hituji':
        if hituji(hands):
            subprocess.Popen(['python', 'sound.py', 'handsign'])
            sleep(0.15)
            return 'saru'
    elif next_sign == 'saru':
        if saru(hands):
            subprocess.Popen(['python', 'sound.py', 'handsign'])
            sleep(0.15)
            return 'inoshishi'
    elif next_sign == 'inoshishi':
        if inoshishi(hands):
            subprocess.Popen(['python', 'sound.py', 'handsign'])
            sleep(0.15)
            return 'uma'
    elif next_sign == 'uma':
        if len(hands) == 2:
            if uma(hands):
                subprocess.Popen(['python', 'sound.py', 'handsign'])
                sleep(0.15)
                return 'tora'
    elif next_sign == 'tora':
        if hituji(hands):
            subprocess.Popen(['python', 'sound.py', 'handsign'])
            sleep(0.15)
            return 'fire'
    return next_sign

# 検出した印の漢字を表示する関数。next_signの一つ前
def show_sign(img,next_sign):
    if next_sign == 'hituji':
        sign = cv2.imread(f'./image/handsign/hebi.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    elif next_sign == 'saru':
        sign = cv2.imread(f'./image/handsign/hituji.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    elif next_sign == 'inoshishi':
        sign = cv2.imread(f'./image/handsign/saru.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    elif next_sign == 'uma':
        sign = cv2.imread(f'./image/handsign/inoshishi.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    elif next_sign == 'tora':
        sign = cv2.imread(f'./image/handsign/uma.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    elif next_sign == 'fire':
        sign = cv2.imread(f'./image/handsign/tora.png',cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, sign, [160,30])
        return img
    else:
        return img

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 360)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if len(hands) > 1:
            uma(hands)
        cv2.imshow("Image", img)
        pressed_key = cv2.waitKey(1)
        if pressed_key == 27:
            break

if __name__ == '__main__':
    main()