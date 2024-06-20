import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import keras
import threading
import streamlit as st
import base64

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('Background/Recognize_face .jpg') 

st.markdown('<style>h3{color: #0000FF;}</style>', unsafe_allow_html=True)
st.subheader('👦Nhận dạng khuôn mặt👧')
FRAME_WINDOW = st.image([])
status_text = st.empty()

label="Warmup..."
n_time_steps = 10
lm_list = []

#Khoi tao thu vien mediapipe
mpPose = mp.solutions.pose
pose=mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

#Load model
model = keras.models.load_model("Action_Recognition/model.h5")

#Doc anh tu webcam
cap= cv2.VideoCapture(0)
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def  make_landmark_timestep(results):
    print(results.pose_landmarks.landmark)
    c_lm =[]
    for id, lm in enumerate(results.pose_landmarks.landmark):
        c_lm.append(lm.x)
        c_lm.append(lm.y)
        c_lm.append(lm.z)
        c_lm.append(lm.visibility)
    return c_lm

def draw_landmark_on_image(mpDraw, results, img):
    #Ve cac duong noi
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
    #ve cac diem nut
    for id, lm in enumerate(results.pose_landmarks.landmark):
        h,w,c = img.shape
        print(id, lm)
        cx,cy = int(lm.x*w), int(lm.y*h)
        cv2.circle(img, (cx,cy), 5, (0,0,255), cv2.FILLED)
    return img

def draw_class_on_image(label, img):
    font =cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,30)
    fontScale = 1
    fontColor = (0,255,0)
    thickness =2
    lineType = 2
    cv2.putText(img, label,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)
    return img

def detect(model, lm_list):
    global label
    lm_list = np.array(lm_list)
    lm_list = np.expand_dims(lm_list, axis=0)
    results = model.predict(lm_list)
    if results[0][0] > 0.5:
        label ="SWING BODY"
    else:
        label ="SWING HAND"
    return label

i=0
warmup_frames=60

while True :
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    i = i+1
    if i> warmup_frames:
        print("Start dect")

        if results.pose_landmarks:
            #Ghi nhan thong so khung xuong
            c_lm = make_landmark_timestep(results)
            lm_list.append(c_lm)

            if len(lm_list)==n_time_steps:
                #Predict
                t1 = threading.Thread(target=detect, args=(model, lm_list,))
                t1.start()
                lm_list =[]

            #Ve khung xuong len anh
            img = draw_landmark_on_image(mpDraw, results, img)

    img = draw_class_on_image(label, img)
    FRAME_WINDOW.image(img, channels='BGR')

    #cv2.imshow("image", img)
    if cv2.waitKey(1) == ord('q'):
        break

#Write vao file csv
cap.release()
cv2.destroyAllWindows()