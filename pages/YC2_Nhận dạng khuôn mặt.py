import streamlit as st
import numpy as np
import cv2 as cv
import joblib
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

cap = cv.VideoCapture(0)

if 'stop' not in st.session_state:
    st.session_state.stop = False

if 'recognize' not in st.session_state:
    st.session_state.recognize = False

# Button for starting/stopping face recognition
recognize_button = st.button('Start/Stop Recognize')

if recognize_button:
    st.session_state.recognize = not st.session_state.recognize

if st.session_state.recognize:
    st.session_state.stop = False
    status_text.text('')
    if 'frame_stop' in st.session_state:
        st.session_state.pop('frame_stop')

    # Load face recognition model
    svc = joblib.load('ModelNhanDangKhuonMat/svc.pkl')
    mydict = ['Hoa', 'ThanhLong', 'Nguyen', 'Minh Quan',  'Son' ,'KhuongTam']

    def visualize(input, faces, names, fps, thickness=2):
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                coords = face[:-1].astype(np.int32)
                cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
                cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
                cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
                cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
                cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
                cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)
                cv.putText(input, names[idx], (coords[0], coords[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if __name__ == '__main__':
        detector = cv.FaceDetectorYN.create(
            'ModelNhanDangKhuonMat/face_detection_yunet_2023mar.onnx',
            "",
            (320, 320),
            0.9,
            0.3,
            5000)

        recognizer = cv.FaceRecognizerSF.create(
            'ModelNhanDangKhuonMat/face_recognition_sface_2021dec.onnx',"")

        tm = cv.TickMeter()

        frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        detector.setInputSize([frameWidth, frameHeight])

        while True:
            hasFrame, frame = cap.read()
            if not hasFrame:
                print('No frames grabbed!')
                break

            tm.start()
            faces = detector.detect(frame)
            tm.stop()

            names = []

            if faces[1] is not None:
                for face in faces[1]:
                    face_align = recognizer.alignCrop(frame, face)
                    face_feature = recognizer.feature(face_align)
                    test_predict = svc.predict(face_feature)
                    
                    if 0 <= test_predict[0] < len(mydict):
                        result = mydict[test_predict[0]]
                        names.append(result)
                    else:
                        names.append("Unknown")

            visualize(frame, faces, names, tm.getFPS())

            FRAME_WINDOW.image(frame, channels='BGR')

cv.destroyAllWindows()
