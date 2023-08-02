import streamlit as st
from pizza import show_pizza
from radar import show_radar
from report import show_report

status1 = [ "Player Match Report", "Pizza Plots" ,"Comparision Radars"]
           
page = st.sidebar.radio("Options",(status1))

if page == "Pizza":
    show_pizza()
elif page == "Player Match Report":
    show_report()
else:
    show_radar()
