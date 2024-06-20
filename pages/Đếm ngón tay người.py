import cv2
import mediapipe as mp
import streamlit as st
import base64
import numpy as np

# Add background image
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

add_bg_from_local('Background/FingerCounter.jpg') 

# Streamlit setup
st.markdown('<style>h3{color: #0000FF;}</style>', unsafe_allow_html=True)
st.subheader('Đếm ngón tay của người🖐️')
FRAME_WINDOW = st.image([])
status_text = st.empty()

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    count = 0
    # Draw hand landmarks
    if result.multi_hand_landmarks:
        myHand = []
        count = 0
        for idx, hand in enumerate(result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(img, hand, mp_hand.HAND_CONNECTIONS)
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                myHand.append([int(lm.x * w), int(lm.y * h)])  # x=0, y=1
            if myHand[8][1] < myHand[5][1]:
                count = count + 1
            if myHand[12][1] < myHand[9][1]:
                count = count + 1
            if myHand[16][1] < myHand[13][1]:
                count = count + 1
            if myHand[20][1] < myHand[17][1]:
                count = count + 1
            if myHand[4][0] < myHand[2][0]:
                count = count + 1

    cv2.putText(img, str(count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    # Show the image in Streamlit
    FRAME_WINDOW.image(img, channels="BGR", use_column_width=True)
    # Display the count
    status_text.markdown(f'<p style="color:#09eb5c; font-weight: bold; font-size: 20px;">Count: {count}</p>', unsafe_allow_html=True)


    # Wait for a key event
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
