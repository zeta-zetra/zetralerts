"""
Front end of the application

Date  : 2023-07-26
Author: Zetra
"""

import base64
import streamlit as st 
import streamlit.components.v1 as components
import time 

from pathlib import Path
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Zetralerts", page_icon=":alarm_clock:", layout="wide")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    
# Add css 
with open( "frontend/static/css/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Get images 
def img_to_bytes(img_path: str) -> str:
    """
    Convert image to bytes
    
    :params img_path is path to the image 
    :type :str 
    
    :return: (str)
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
  
def img_to_html(img_path: str) -> str:
    """
    Take image path and create an image html tag 
    
    :params img_path is path to the image 
    :type :str 
    
    :return: (str)
    """
    img_html = "<img src='data:image/png;base64,{}' style='height:70%!important ;width:100%; background-color:#D3DCD9'>".format(
      img_to_bytes(img_path)
    )
    return img_html

# Utility functions
def display_card(img_src: str, title:str, desc: str) -> str:
      """
      Display the html card 
      
      :params img_src is the image source
      :type :str 
      
      :params title is the card title 
      :type :str 
      
      :params desc is the body description
      :type :str 
      
      :return: (str)
      """
      image = img_to_html(img_src)
      card = f"""<div class='card'>
                  {image}
                  <div class='container'>
                    <h4>
                      <b>{title}</b>
                    </h4>
                    <p>{desc}</p>
                    <button class='activate'> Activate </button>
                  </div>
                </div>"""     
      
      return card

selected = option_menu(
  menu_title=None,
  options=["Home", "Register", "Alerts", "Settings","Contact"],
  orientation="horizontal",
  icons=['house', 'list-task', "alarm", 'gear', "envelope"],
  styles={
    "container": {"padding": "0!important", "background-color": "#F4F4F4"},
    "icon": {"color": "#F4F4F4", "font-size": "25px"}, 
    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#47595D"},
}
)

if selected == "Home":
  

  st.title("Get alerts when it matters.")
  st.write("Send notifications to your Telegram bot when high probability setups are in play.")


  st.write("##")

  # -- First row 
  container = st.container()
  col1, col2, col3, col4 = container.columns(4)
  
  col1.markdown(display_card('frontend/static/images/triple-tops.png', 'Triple Tops', 'This is a chart pattern'), unsafe_allow_html=True)
  col2.markdown(display_card('frontend/static/images/inv-hs.png', 'Inverse Head and Shoulders', 'This is a chart pattern'), unsafe_allow_html=True)
  col3.markdown(display_card('frontend/static/images/hs.png', 'Head and Shoulders', 'This is a chart pattern'), unsafe_allow_html=True)      
  col4.markdown(display_card('frontend/static/images/triangle.png', 'Triangle', 'This is a chart pattern'), unsafe_allow_html=True) 

if selected == "Register":
  
  with st.form("register_form"):
    st.title("Register Your Telegram Bot")
    
    bot_name = st.text_input("Bot Name", "")
    token    = st.text_input("Bot Token", "")
     
    submit = st.form_submit_button("Test")
    
    if submit:
          if not bot_name or not token:
            st.error("Fill in the necessary information")
          else:
              with st.spinner('Wait for it...'):
                  time.sleep(5)
              st.success('Done!')

  
if selected == "Alerts":
  st.write("Alerts")
  
if selected == "Settings":
        
 with st.form("settings_form"):
    st.title("Settings")
    
    alert_interval   = st.number_input("Alert Interval")
    trigger_interval = st.number_input("Trigger Interval")
    currency_pair    = st.selectbox(
        "Select currency pair",
        ("EUR/USD", "USD/CAD", "GBP/USD"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
    timeframe = st.selectbox(
        "Select trading timeframe",
        ("15min", "30min", "1H", "4H", "1D"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
     
    submit = st.form_submit_button("Save")
    
    if submit:
          if not alert_interval or not trigger_interval or not currency_pair or not timeframe:
            st.error("Fill in the necessary information")
          else:
              with st.spinner('Wait for it...'):
                  time.sleep(5)
              st.success('Done!')   
              
                 
if selected == "Contact":
       st.title("How to reach us.")

       st.write("##")
       
       container   = st.container()
       col1, col2, col3, col4, col5 = container.columns(5)
       
       col1.markdown("<a href='https://www.youtube.com/channel/UC87AaqcveNqlkodJrr5zUsw' target='_blank'>Youtube</a>", unsafe_allow_html=True)
       col2.markdown("<a href='https://github.com/zeta-zetra/code' target='_blank'>Github</a>", unsafe_allow_html=True)
       col3.markdown("<a href='https://www.instagram.com/zetratrading/' target='_blank'>Instagram</a>", unsafe_allow_html=True)
       col4.markdown("<a href='https://www.facebook.com/people/Zetra-Trading/100090523216602/' target='_blank'>Facebook</a>", unsafe_allow_html=True)
       col5.markdown("<a href='https://zeta-zetra.github.io/docs-forex-strategies-python/' target='_blank'>Online Book</a>", unsafe_allow_html=True)