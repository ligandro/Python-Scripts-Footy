import streamlit as st
from pizza import show_pizza
from radar import show_radar

page = st.selectbox("Pizza Plots or Comparision Radars", ("Pizza", "Radar"))
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1475650522725-015d35677789?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

    # Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Pizza", page_icon=":pizza:", layout="wide")
st.markdown(page_bg_img, unsafe_allow_html=True)
if page == "Pizza":
    show_pizza()
else:
    show_radar()
