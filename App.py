import streamlit as st
from pizza import show_pizza
from radar import show_radar

page = st.selectbox("Pizza Plots or Comparision Radars", ("Pizza", "Radar"))

if page == "Pizza":
    show_pizza()
else:
    show_radar()
