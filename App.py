import streamlit as st
from pizza import show_pizza
from radar import show_radar


status1 = [  "Pizza Plots" ,"Comparision Radars"]
           #,"Player Match Report"]
           
page = st.sidebar.radio("Options",(status1))

if page == "Pizza Plots":
    show_pizza()
else:
    show_radar()
