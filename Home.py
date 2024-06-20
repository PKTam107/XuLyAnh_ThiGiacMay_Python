import streamlit as st
import base64

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("<h1 style='font-size: 55px;color:black'>👋Chào mừng bạn đến với website của Phạm Khương Tâm! 🍀🍀🍀</h1>", unsafe_allow_html=True)
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
add_bg_from_local('Background/Home.jpg')  
  
st.markdown(
    """
    <style>
    .red-text {
        color: #3333FF;
        font-size:25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="red-text">
         <p><b style="font-size: 40px; color:black;">Thông tin cá nhân:</b></p>
        <div style="color:#FF33CC; font-size: 20px;">
	    - Họ tên: Phạm Khương Tâm</p>
        - Mã số sinh viên: 21110638</p>
        - Khoa: Công nghệ thông tin</p>
        - Trường: Đại học Sư phạm Kỹ thuật thành phố Hồ Chí Minh
        </div>
	<p><b style="font-size: 40px; color:black;">Thông tin liên hệ:</b></p>
	<div>
        <p><b style="color:#3333FF; font-size: 20px;">- Email: </b><a style="color:red; font-size: 20px;" href=" 21110638@student.hcmute.edu.vn"> 21110638@student.hcmute.edu.vn</a></p>
        <p><b style="color:#3333FF; font-size: 20px;">- Phone: </b><a style="color:red; font-size: 20px;" href="0949704663"> 0949704663</a></p>
	</div>
	<p><b style="font-size: 40px; color:black;">Thông tin giáo viên hướng dẫn:</b></p>
   	<div>
        <p><b style="color:#3333FF; font-size: 20px;">- Teacher: Tran Tien Duc</b></p>
        <p><b style="color:#3333FF; font-size: 20px;">- Email: </b><a style="color:red; font-size: 20px;" href="ductt@hcmute.edu.vn"> ductt@hcmute.edu.vn</a></p>
        <p><b style="color:#3333FF; font-size: 20px;">- Phone: </b><a style="color:red; font-size: 20px;" href="ductt@hcmute.edu.vn"> 0919622862</a></p>
        <p><b style="color:#3333FF; font-size: 20px;">- Github: </b><a style="color:red; font-size: 20px;" href="https://github.com/TranTienDuc">https://github.com/TranTienDuc</a><p>
	</div>
    </div>
    """,
    unsafe_allow_html=True
)