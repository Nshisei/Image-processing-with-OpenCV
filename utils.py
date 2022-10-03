import cv2
import mediapipe as mp
import numpy as np
import cvzone

# 画像を重複
# 
def overlayPNG(imgBack, imgFront, direction='right',pos=[0, 0]):
    imgFront = cv2.resize(imgFront, (int(imgFront.shape[1]//2)*2, int(imgFront.shape[0]//2)*2)) # 重ねる画像サイズを 偶数×偶数 に変更する。
    hf, wf, cf = imgFront.shape # 重ねる画像の高さ、幅、カラー
    hb, wb, cb = imgBack.shape # 背景画像の高さ、幅、カラー
    *_, mask = cv2.split(imgFront)
    maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
    imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

    imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
    if direction == 'right': # 右向きの時、画像の左端中央を軸にしてそこから右方向に画像を重ねる
        hf_u, hf_t, wf_l, wf_r = hf, 0, wf, 0
        # 重ねようとしている画像が背景画像からはみ出していれば、はみ出した分を取り除く
        if pos[1]+(hf//2) >= hb:
            hf_u = hf - (pos[1]+(hf//2)-hb)
        if pos[1]-(hf//2) < 0:
            hf_t = (hf//2)-pos[1]
            # hf = hb - pos[1]
        if pos[0]+wf >= wb:
            wf = wb - pos[0]
        imgMaskFull[(pos[1]-(hf//2-hf_t)):(pos[1]+(hf_u-hf//2)), pos[0]:wf + pos[0], :] = imgRGB[hf_t:hf_u,:wf,:]
        imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(maskBGR)
        imgMaskFull2[(pos[1]-(hf//2-hf_t)):(pos[1]+(hf_u-hf//2)), pos[0]:wf + pos[0], :] = maskBGRInv[hf_t:hf_u,:wf,:]
    
    if direction == 'left':# 左向きの時、画像の右端中央を軸にしてそこから左方向に画像を重ねる
        hf_u, hf_t, wf_l, wf_r = hf, 0, 0, wf
        if pos[1]+(hf//2) >= hb:
            hf_u = hf - (pos[1]+(hf//2)-hb)
        if pos[1]-(hf//2) < 0:
            hf_t = (hf//2)-pos[1]
        if pos[0]-wf < 0:
            wf_l = wf - pos[0]
        imgRGB = cv2.flip(imgRGB, 1)
        imgMaskFull[(pos[1]-(hf//2-hf_t)):(pos[1]+(hf_u-hf//2)), pos[0]-(wf-wf_l):pos[0], :] = imgRGB[hf_t:hf_u,wf_l:wf_r,:]
        imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(cv2.flip(maskBGR,1))
        imgMaskFull2[(pos[1]-(hf//2-hf_t)):(pos[1]+(hf_u-hf//2)), pos[0]-(wf-wf_l):pos[0], :] = maskBGRInv[hf_t:hf_u,wf_l:wf_r,:]
        
    if direction == 'center': 
        imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
        imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(maskBGR)
        imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

    imgBack = cv2.bitwise_and(imgBack, imgMaskFull2)
    imgBack = cv2.bitwise_or(imgBack, imgMaskFull)

    return imgBack

# 火の画像を指定した箇所に表示
def fire(image, page, pos=[0,0], direction='front', rotate=0):
    # 正面向きの火の画像を表示
    if direction == 'front':
        fire = cv2.imread(f'./image/fire_front/image_{str(page).zfill(3)}.png',cv2.IMREAD_UNCHANGED) # 指定した番号の正面画像を読み込み
        fire = cv2.resize(fire , (640, 360)) # 画像をリサイズ
        rgba = cv2.cvtColor(fire, cv2.COLOR_RGB2RGBA) # アルファチャンネルを含めた画像に変換
        rgba[..., 3] = np.where(np.all(fire < 50, axis=-1), 0, 255) # 画像中の色が50未満の値部分に透明チャンネルを加える
        image = cvzone.overlayPNG(image, rgba, [0,0]) # 火の画像を重ねる
        page = page+1 if page != 142 else 1 # 次に読み込む火の番号を更新
        return image, page
    else:
        fire = cv2.imread(f'./image/fireside/image_{str(page).zfill(3)}.png',cv2.IMREAD_UNCHANGED) # 指定した番号の正面画像を読み込み
        fire = cv2.resize(fire , (int(640-(140*0.1)),int(360-(140*0.1)))) # 画像をリサイズ
        rgba = cv2.cvtColor(fire, cv2.COLOR_RGB2RGBA) # アルファチャンネルを含めた画像に変換
        rgba[..., 3] = np.where(np.all(fire < 50, axis=-1), 0, 255) # 画像中の色が50未満の値部分に透明チャンネルを加える
        rgba = cvzone.rotateImage(rgba, rotate) # 顔の向いている方向に画像を回転させる
        page = page+1 if page != 95 else 1 # 次に読み込む火の番号を更新
        if direction == 'left':
            image = overlayPNG(image, rgba, 'left', pos) # 火の画像を重ねる
        else:
            image = overlayPNG(image, rgba, 'right', pos)

        return image, page