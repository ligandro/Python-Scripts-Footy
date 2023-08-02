import streamlit as st
from pizza import show_pizza
from radar import show_radar
#from report import show_report

status1 = [  "Pizza Plots" ,"Comparision Radars"]
           #,"Player Match Report"]
           
page = st.sidebar.radio("Options",(status1))

if page == "Pizza Plots":
    show_pizza()
#elif page == "Player Match Report":
    show_report()
else:
    show_radar()
