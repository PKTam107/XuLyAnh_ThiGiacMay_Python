import streamlit as st
import math
import base64

st.set_page_config(page_title="Giải phương trình bậc 2", page_icon="📌")
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

add_bg_from_local('Background/ptb2.jpg')  

st.subheader("Giải phương trình bậc 2")
st.sidebar.header("Giải phương trình bậc 2")

with st.form(key='my-form'):
    a = st.text_input('Nhập a:')
    b = st.text_input('Nhập b:')
    c = st.text_input('Nhập c:')
    submit_button_giai = st.form_submit_button(label='Giải')

if submit_button_giai:
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        st.warning("Vui lòng nhập số hợp lệ cho a, b, và c.")
    else:
        if a == 0.0:
            if b == 0.0:
                if c == 0.0:
                    ket_qua = 'PT vô số nghiệm'
                else:
                    ket_qua = 'PT vô nghiệm'
            else:
                x = -c/b
                ket_qua = 'PT có nghiệm x = %.2f' % x
        else:
            delta = b**2 - 4*a*c
            if delta < 0:
                ket_qua = 'PT vô nghiệm'
            else:
                x1 = (-b + math.sqrt(delta))/(2*a)
                x2 = (-b - math.sqrt(delta))/(2*a)

                ket_qua = 'PT có nghiệm x1 = %.2f và x2 = %.2f' % (x1, x2)
        
        st.write(f"<span style='color:#FF6666; font-size:32px;'>{ket_qua}</span>", unsafe_allow_html=True)
