import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cvlib as cv

model=load_model('gender_detection_pre.model')

cap=cv2.VideoCapture(0)

classes=['man','woman']

while cap.isOpened():
    success,frame=cap.read()
    face,confidence=cv.detect_face(frame)

    for idx, f in enumerate(face):
        (startX,startY)=f[0],f[1]
        (endX,endY)=f[2],f[3]
        cv2.rectangle(frame,(startX,startY),(endX,endY),(0,255,0),2)
        face_crop=np.copy(frame[startY:endY,startX:endX])

        if(face_crop.shape[0]<10 or face_crop.shape[1]<10):
            continue

        face_crop=cv2.resize(face_crop,(96,96))
        face_crop=face_crop.astype("float")/255.0
        face_crop=img_to_array(face_crop)
        face_crop=np.expand_dims(face_crop,axis=0)

        conf=model.predict(face_crop)[0]

        idx=np.argmax(conf)
        label=classes[idx]

        label="{}: {:.2f}%".format(label,conf[idx]*100)

        Y=startY-10 if startY-10>10 else startY+10

        cv2.putText(frame,label,(startX,Y),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow('Gender Detection',frame)

    if cv2.waitKey(1) ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()    