import base64
import requests
import streamlit as st
from utils.user import *
from utils.components import component_hide_sidebar

def main():
    show_login_page()
        
def show_login_page():
    col1, col2 = st.columns([4,1.5])
    col1.write("## DashBoard Escritorio FB")
    with open("./assets/imgs/logo_FB.png", "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode()
    # Inserir imagem com altura customizada (ex: 100px)
    col2.markdown(
        f'<img src="data:image/png;base64,{b64_image}" style="height:100px;">',
        unsafe_allow_html=True
    )

    userName = st.text_input(label="", value="", placeholder="login")
    userPassword = st.text_input(label="", value="", placeholder="Senha",type="password")
    
    if st.button("login"):
            st.switch_page("pages/home.py")
            st.experimental_rerun()

if __name__ == "__main__":
    st.set_page_config(
    page_title="login | Escritorio FB",
    page_icon="./assets/imgs/logo_FB.png",
    layout="centered",
    )

    component_hide_sidebar()
    main()