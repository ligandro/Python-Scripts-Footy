import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, NoNorm
from matplotlib import cm
import matplotlib.gridspec as gridspec
import numpy as np
from mplsoccer import PyPizza, add_image, FontManager


from PIL import Image
import urllib
import json
import os
import math

#import modules and packages
import requests
from bs4 import BeautifulSoup
import json
import datetime



url = ["https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats",
                 "https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats"]
                 
matches = ["Stats","Shooting","Passing","Pass","Goal","Defensive","Possession","Playing","Miscellaneous"]                 

with open( "style2.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)




def scrape(url,m):
    data = requests.get(url)
    df2 = pd.read_html(data.text, match= m)[0]
    df2.columns = df2.columns.droplevel()
    df2= df2[df2.Player != "Player"]
    return df2

@st.cache
def getting_data():
    df1 = scrape(url[1],matches[1])
    df1["Rk"] =df1["Rk"].astype(int)
# replacing na values in college with No college
    df1.fillna(0, inplace = True)
 
 
    df1["Age"] =df1["Age"].astype(str)
    def turn(x):
        b = x[:2]
        a = x[3:]
        a =a.strip("0")
        x =b +" Years, "+ a+ " Days"
        return x


    df1["Age"]=df1["Age"].apply(lambda x : turn(x) )



        # Change type of variable to floats
    df1["Player"] =df1["Player"].astype(str)
    df1["Nation"] =df1["Nation"].astype(str)
    df1["Squad"] =df1["Squad"].astype(str)
    df1["Comp"] =df1["Comp"].astype(str)
    df1["Pos"] =df1["Pos"].astype(str)
    df1["90s"] =df1["90s"].astype(float)
    df1["Gls"] =df1["Gls"].astype(float)
    df1["SoT/90"] =df1["SoT/90"].astype(float)
    df1["npxG"] =df1["npxG"].astype(float)
    df1["npxG/Sh"] =df1["npxG/Sh"].astype(float)
    df1["PK"] =df1["PK"].astype(float)

        #Create new columns
    df1["npG"] = df1["Gls"] -df1["PK"]

        # Create main dataframe
    list1 = df1.iloc[:,0]
    liga = pd.DataFrame()
    liga["Rk"] =list1

        # applying merge with more parameters
    liga = liga.merge(df1[["Player","Rk",'Pos','Squad','Nation',"Comp",'Age','90s','npG','npxG','SoT/90',"npxG/Sh"]], left_on="Rk", right_on="Rk",how = 'inner')
        
    # Passing Stats
    df2 = scrape(url[2],matches[2])
    df2["Rk"] =df2["Rk"].astype(int)
    # replacing na values in college with No college
    df2.fillna(0, inplace = True)


    list1 = df2.iloc[:, 9]
    df2["Passes Completed"] = list1
    list1 = df2.iloc[:, 11]
    df2["Passes%"] = list1


    df2["xA"] =df2["xA"].astype(float)
    df2["Passes%"] =df2["Passes%"].astype(float)
    df2["1/3"] =df2["1/3"].astype(float)
    df2["KP"] =df2["KP"].astype(float)
    df2["CrsPA"] =df2["CrsPA"].astype(float) 
    df2["PPA"] =df2["PPA"].astype(float)
    df2["Ast"] =df2["Ast"].astype(float)
    df2["Passes Completed"] =df2["Passes Completed"].astype(float)
    df2["Prog"] =df2["Prog"].astype(float)


     # applying merge with more parameters
    liga = liga.merge(df2[["Rk",'Ast','xA','KP','1/3','PPA','CrsPA','Prog','Passes Completed','Passes%']], left_on="Rk", right_on="Rk",how = 'inner')

    
    # Pass Type Stats
    df3 = scrape(url[3],matches[3])
    df3["Rk"] =df3["Rk"].astype(int)
    # replacing na values in college with No college
    df3.fillna(0, inplace = True)


    df3["TB"] =df3["TB"].astype(float)
    df3["Sw"] =df3["Sw"].astype(float)
    df3["Crs"] =df3["Crs"].astype(float)

    liga = liga.merge(df3[["Rk",'TB','Sw','Crs']], left_on="Rk", right_on="Rk",how = 'inner')



    df4 = scrape(url[4],matches[4])
    df4["Rk"] =df4["Rk"].astype(int)
    # replacing na values in college with No college
    df4.fillna(0, inplace = True)


    df4["SCA90"] =df4["SCA90"].astype(float)

    liga = liga.merge(df4[["Rk",'SCA90']], left_on="Rk", right_on="Rk",how = 'inner')



    df6 = scrape(url[6],matches[6])
    df6["Rk"] =df6["Rk"].astype(int)
    # replacing na values in college with No college
    df6.fillna(0, inplace = True)

    df6["Att 3rd"] =df6["Att 3rd"].astype(float)
    df6["Att Pen"] =df6["Att Pen"].astype(float)
    df6["Drib"] =df6["Att"].astype(float)
    df6["Drib Succ%"] =df6["Succ%"].astype(float)
    df6["PRec"] =df6["Rec"].astype(float)
    df6["PPRec"] =df6["Prog"].astype(float)


    liga = liga.merge(df6[["Rk","Att 3rd",'Att Pen','Drib','Drib Succ%','PRec',"PPRec"]], left_on="Rk", right_on="Rk",how = 'inner')


    df5 = scrape(url[5],matches[5])
    df5["Rk"] =df5["Rk"].astype(int)
    df5.fillna(0, inplace = True)

    df5["TklW"] =df5["TklW"].astype(float)
    df5["Sh"] =df5["Sh"].astype(float)
    df5["Int"] =df5["Int"].astype(float)
    df5["Clr"] =df5["Clr"].astype(float)

    # applying merge with more parameters
    # don't run this more than once
    liga = liga.merge(df5[["Rk","TklW",'Sh','Int','Clr']],left_on="Rk", right_on="Rk",how = 'inner')


    df8 = scrape(url[8],matches[8])
    df8["Rk"] =df8["Rk"].astype(int)
    # replacing na values in college with No college
    df8.fillna(0, inplace = True)

    df8["FoulsC"] =df8["Fls"].astype(float)
    df8["FoulsW"] =df8["Fld"].astype(float)
    df8["Recov"] =df8["Recov"].astype(float)
    df8["AerialW"] =df8["Won"].astype(float)

    liga = liga.merge(df8[["Rk","FoulsC",'FoulsW','Recov','AerialW']],left_on="Rk", right_on="Rk",how = 'inner')

    liga["Tkl+Int"] = liga["TklW"] + liga["Int"]
    
        
    return liga

liga = getting_data()



with open( "style2.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



st.header(":soccer: PIZZA PLOTTER :pizza: ")

st.subheader(" :o: Create Pizza Plots for any player in Europe's Big 5 Leagues ")
st.subheader(" :o: Compare stats with Big 5 or a specific league, set position and minimum 90s played")
st.subheader(":o: NOTE : Set minimum 90s appropriately,set league accordingly")
st.subheader("Data: FBREF Made by : Ligandro")
st.dataframe(data=liga)
st.subheader(":bar_chart: Plot:")


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)





col_list = liga["Player"].values.tolist()

x = st.sidebar.selectbox("Name of Player ",options = col_list)


league = [ "eng Premier League","fr Ligue 1","de Bundesliga","it Serie A","es La Liga","Big 5"]
League = st.sidebar.selectbox("Select League ",options = league)

a3 = League
if a3 != "Big 5":
    prem = liga[liga["Comp"] == League]
    League = a3[3:]
else:
    prem = liga.copy()
    League = a3
  
  
minutes = st.sidebar.slider("Select Minimum 90s Played",0,38)
 
prem = prem[prem["90s"] >= minutes ]

prem["npG"] =prem["npG"]/prem["90s"]
prem["npxG"] =prem["npxG"]/prem["90s"]
prem["Ast"] =prem["Ast"]/prem["90s"]
prem["xA"] =prem["xA"]/prem["90s"]
prem["KP"] =prem["KP"]/prem["90s"]
prem["PPA"] =prem["PPA"]/prem["90s"]
prem["1/3"] =prem["1/3"]/prem["90s"]
prem["CrsPA"] =prem["CrsPA"]/prem["90s"]
prem["Passes Completed"] =prem["Passes Completed"]/prem["90s"]
prem["TB"] =prem["TB"]/prem["90s"]
prem["Sw"] =prem["Sw"]/prem["90s"]
prem["Crs"] =prem["Crs"]/prem["90s"]
prem["Att 3rd"] =prem["Att 3rd"]/prem["90s"]
prem["Att Pen"] =prem["Att Pen"]/prem["90s"]
prem["Drib"] =prem["Drib"]/prem["90s"]
prem["TB"] =prem["TB"]/prem["90s"]
prem["Sw"] =prem["Sw"]/prem["90s"]
prem["PRec"] =prem["PRec"]/prem["90s"]
prem["PPRec"] =prem["PPRec"]/prem["90s"]
prem["TklW"] =prem["TklW"]/prem["90s"]
prem["Sh"] =prem["Sh"]/prem["90s"]
prem["Int"] =prem["Int"]/prem["90s"]
prem["Clr"] =prem["Clr"]/prem["90s"]
prem["FoulsC"] =prem["FoulsC"]/prem["90s"]
prem["FoulsW"] =prem["FoulsW"]/prem["90s"]
prem["Recov"] =prem["Recov"]/prem["90s"]
prem["AerialW"] =prem["AerialW"]/prem["90s"]
prem["Tkl+Int"] =prem["Tkl+Int"]/prem["90s"]


player = prem.loc[prem['Player']==x]
time = float(player.iloc[0,7])
Name = str(player.iloc[0,1])
Team = str(player.iloc[0,3])
age =player.iloc[0,6]


pos1 = [ "Forward","Midfielder","Defender"]
pos = st.sidebar.selectbox("Select Position",options = pos1)


def forward():
    kik = prem[(prem["Pos"] == "FW") | (prem["Pos"] == "FW,DF") | (prem["Pos"] == "FW,MF")| (prem["Pos"] == "MF,FW")]
    
    # select stats
    playe = list(player.iloc[0])

    stat = []
    stat.extend([playe[8],playe[9],playe[11],playe[10],playe[24],
          playe[27],playe[28],playe[25],
          playe[39],playe[38],playe[36],
          playe[29],playe[19] ,playe[23],playe[14],playe[13]])
    lis = [8,9,11,10,24,27,28,25,39,38,36,29,19,23,14,13]
    params = []
    for x in lis:
        params.append(liga.columns[x])
    params[0] = "Non-Penalty\nGoals"
    params[3] = "Shots on\nTarget"
    params[4] = "Shot Creating\nActions"
    params[5] = "Dribbles\nAttempted"
    params[6] = "Dribble\nSuccess%"
    params[7] = "Attacking 3rd\nTouches"
    params[8] = "Tackles+\nInterceptions"
    params[9] = "Aerials\nWon"
    params[10] = "Fouls\nWon"
    params[11] = "Passes\nRecieved"
    params[12] = "Passes\nCompleted"
    params[13] = "Crosses"
    params[14] = "Key\nPasses"
    params[15] = "xA"
    
    
    
    
    # minimum range value and maximum range value for parameters
    min_range= []
    max_range =[]
    for x in lis:
        min_range.append(kik.iloc[:,x].min())
        max_range.append(kik.iloc[:,x].max())          
    stat1 = [ round(x, 2) for x in stat]         
    # color for the slices and text
    slice_colors = ["#FF6161"] * 5 + ["#56AEFF"] * 3 + ["#94C450"] * 3 + ["#FFD230"] * 5
    text_colors = ["black"] * 16 
    
    # instantiate PyPizza class
    baker = PyPizza(
        params=params,
        min_range=min_range,        # min range values
        max_range=max_range, 
        background_color="#FAF7F3",
        straight_line_color="#FAF7F3",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=1,              # linewidth for other circles
        inner_circle_size=10,
        other_circle_ls="-." 
    )

    colors = []
    for x in params:
        colors.append("#EFEEED")
    # plot pizza
    fig, ax = baker.make_pizza(
        stat1,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space=slice_colors,        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#FAF7F3", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            font = "monospace",size =11,color="black",fontweight="bold", va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            font = "monospace",size =9,color="black",fontweight="bold", zorder=3,
            bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
            )
        )    
    )


    fig.set_facecolor('#FAF7F3')
    ax.patch.set_facecolor('#FAF7F3')

    
    # add title
    fig.text(
    0.515, 1.02, f"{Name}-{Team}",
    path_effects=[path_effects.Stroke(linewidth=0.2, foreground="black"), path_effects.Normal()],
    ha="center", font = "monospace",size =32,color="black",fontweight="bold"
    )

    # add subtitle
    fig.text(
    0.515, 0.982,
    f"Forward Player Stats/90 | {League} Attackers FW,FW/MF,MF/FW,FW/DF",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )
    fig.text(
    0.515, 0.948,
    f" 90s Played : {time} | Age : {age} | Season : 22-23",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )



    # add credits
    notes = f'Only Players with 90s >= {minutes}'
    CREDIT_1 = "Data : Fbref"
    CREDIT_2 = "MPL Soccer"

    fig.text(
    0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
    font = "monospace",size =12,color="black",fontweight="bold",
    ha="right"
    )

    # add image
    im1 = plt.imread('https://i.postimg.cc/Kzj8dZS2/LOGO1.png')
    ax_image = add_image(
    im1, fig, left=0.4778, bottom=0.46, width=0.07, height=0.07
    ) 
    
    
     # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/br7tLZ5r/3.png')
    ax_image = add_image(
    im3, fig, left=0.08, bottom=-0.015, width=0.17, height=0.17
    )   # these values might differ when you are plotting


    # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/RFCQnnrz/4.png')
    ax_image = add_image(
    im3, fig, left=0.85, bottom=0.815, width=0.12, height=0.12
    )   # these values might differ when you are plotting 
   
    
    st.pyplot(fig)

def mid():
    kik =  prem[(prem["Pos"] == "MF") | (prem["Pos"] == "MF,DF") ]
    
    # select stats
    playe = list(player.iloc[0])

    stat = []
    stat.extend([playe[9],playe[14],playe[24],
          playe[25], playe[27],playe[28],
          playe[39],playe[38],playe[36],playe[37],
           playe[19], playe[20], playe[15],playe[22],playe[18],playe[13]])
    lis = [9,14,24,25,27,28,39,33,36,37,19,20,15,22,18,13]
    params = []
    for x in lis:
        params.append(liga.columns[x])
    params[0] = "Non-Penalty\nxG"
    params[1] = "Key\nPasses"
    params[2] = "Shot Creating\nActions"
    params[3] = "Attacking 3rd\nTouches"
    params[4] = "Dribbles\nAttempted"
    params[5] = "Dribble\nSuccess%"
    params[6] = "Tackles+\nInterceptions"
    params[7] = "Aerials\nWon"
    params[8] = "Fouls\nWon"
    params[9] = "Ball\nRecoveries"
    params[10] = "Passes\nCompleted"
    params[11] = "Passes\nCompletion%"
    params[12] = "Final 3rd\nPasses"
    params[13] = "Long\nBalls"
    params[14] = "Progressive\nPasses"
    params[15] = "xA"
    
    
    
    
    # minimum range value and maximum range value for parameters
    min_range= []
    max_range =[]
    for x in lis:
        min_range.append(kik.iloc[:,x].min())
        max_range.append(kik.iloc[:,x].max())          
    stat1 = [ round(x, 2) for x in stat]         
    # color for the slices and text
    slice_colors = ["#FF6161"] * 3 + ["#56AEFF"] * 3 + ["#94C450"] * 4 + ["#FFD230"] * 6
    text_colors = ["black"] * 16 
    
    # instantiate PyPizza class
    baker = PyPizza(
        params=params,
        min_range=min_range,        # min range values
        max_range=max_range, 
        background_color="#FAF7F3",
        straight_line_color="#FAF7F3",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=1,              # linewidth for other circles
        inner_circle_size=10,
        other_circle_ls="-." 
    )

    colors = []
    for x in params:
        colors.append("#EFEEED")
    # plot pizza
    fig, ax = baker.make_pizza(
        stat1,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space=slice_colors,        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#FAF7F3", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            font = "monospace",size =11,color="black",fontweight="bold", va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            font = "monospace",size =9,color="black",fontweight="bold", zorder=3,
            bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
            )
        )    
    )


    fig.set_facecolor('#FAF7F3')
    ax.patch.set_facecolor('#FAF7F3')
    
    
    # add title
    fig.text(
    0.515, 1.02, f"{Name}-{Team}",
    path_effects=[path_effects.Stroke(linewidth=0.2, foreground="black"), path_effects.Normal()],
    ha="center", font = "monospace",size =32,color="black",fontweight="bold"
    )

    # add subtitle
    fig.text(
    0.515, 0.982,
    f"Midfielder Stats/90 | {League} Midfielders MF,MF/DF",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )
    fig.text(
    0.515, 0.948,
    f" 90s Played : {time} | Age : {age} | Season : 22-23",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )



    # add credits
    notes = 'Only Players with 90s >= 3'
    CREDIT_1 = "Data : Fbref"
    CREDIT_2 = "MPL Soccer"

    fig.text(
    0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
    font = "Monospace",size =12,color="black",fontweight="bold",
    ha="right"
    )

    # add image
    # add image
    im1 = plt.imread('https://i.postimg.cc/Kzj8dZS2/LOGO1.png')
    ax_image = add_image(
    im1, fig, left=0.4778, bottom=0.46, width=0.07, height=0.07
    )
    
     # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/br7tLZ5r/3.png')
    ax_image = add_image(
    im3, fig, left=0.08, bottom=-0.015, width=0.17, height=0.17
    )   # these values might differ when you are plotting


    # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/Y9XNNqkL/5.png')
    ax_image = add_image(
    im3, fig, left=0.85, bottom=0.815, width=0.12, height=0.12
    )   # these values might differ when you are plotting 
   
    
    st.pyplot(fig)
   
def defender():
    kik = prem[(prem["Pos"] == "DF") | (prem["Pos"] == "DF,MF") | (prem["Pos"] == "DF,FW")]
    
    # select stats
    playe = list(player.iloc[0])

    
    stat = []
    stat.extend([playe[8],playe[24],
          playe[25], playe[27],playe[28],
          playe[39],playe[32],playe[34],playe[38],playe[37],
          playe[15],playe[22],playe[18],playe[30],playe[17],playe[13]])
    lis = [9,14,24,25,27,28,39,33,36,37,19,20,15,22,18,13]
    params = []
    for x in lis:
        params.append(liga.columns[x])
    params[0] = "Non-Penalty\nGoals"
    params[1] = "Shot Creating\nActions"
    params[2] = "Attacking 3rd\nTouches"
    params[3] = "Dribbles\nAttempted"
    params[4] = "Dribble\nSuccess%"
    params[5] = "Tackles+\nInterceptions"
    params[6] = "Shots\nBlocked"
    params[7] = "Clearances"
    params[8] = "Aerials\nWon"
    params[9] = "Ball\nRecoveries"
    params[10] = "Final 3rd\nPasses"
    params[11] = "Long\nBalls"
    params[12] = "Progressive\nPasses"
    params[13] = "Progressive\nPasses Recieved"
    params[14] = "Crosses into\nPenalty Box"
    params[15] = "xA"
    
    
    
    # minimum range value and maximum range value for parameters
    min_range= []
    max_range =[]
    for x in lis:
        min_range.append(kik.iloc[:,x].min())
        max_range.append(kik.iloc[:,x].max())          
    stat1 = [ round(x, 2) for x in stat]         
    # color for the slices and text
    slice_colors = ["#FF6161"] * 2 + ["#56AEFF"] * 3 + ["#94C450"] * 5 + ["#FFD230"] * 6
    text_colors = ["black"] * 16 
    
    # instantiate PyPizza class
    baker = PyPizza(
        params=params,
        min_range=min_range,        # min range values
        max_range=max_range, 
        background_color="#FAF7F3",
        straight_line_color="#FAF7F3",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=1,              # linewidth for other circles
        inner_circle_size=10,
        other_circle_ls="-." 
    )

    colors = []
    for x in params:
        colors.append("#EFEEED")
    # plot pizza
    fig, ax = baker.make_pizza(
        stat1,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space=slice_colors,        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#FAF7F3", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            font = "monospace",size =11,color="black",fontweight="bold", va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            font = "monospace",size =9,color="black",fontweight="bold", zorder=3,
            bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
            )
        )    
    )


    fig.set_facecolor('#FAF7F3')
    ax.patch.set_facecolor('#FAF7F3')

    
    # add title
    fig.text(
    0.515, 1.02, f"{Name}-{Team}",
    path_effects=[path_effects.Stroke(linewidth=0.2, foreground="black"), path_effects.Normal()],
    ha="center", font = "monospace",size =32,color="black",fontweight="bold"
    )

    # add subtitle
    fig.text(
    0.515, 0.982,
    f"Defender Stats/90 | {League} Defenders DF,DF/FW,DF,MF",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )
    fig.text(
    0.515, 0.948,
    f" 90s Played : {time} | Age : {age} | Season : 22-23",
    ha="center", font = "monospace",size =13,color="black",fontweight="bold"
    )



    # add credits
    notes = f'Only Players with 90s >= {minutes}'
    CREDIT_1 = "Data : Fbref"
    CREDIT_2 = "MPL Soccer"

    fig.text(
    0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
    font = "monospace",size =12,color="black",fontweight="bold",
    ha="right"
    )

    # add image
    im1 = plt.imread('https://i.postimg.cc/Kzj8dZS2/LOGO1.png')
    ax_image = add_image(
    im1, fig, left=0.4778, bottom=0.46, width=0.07, height=0.07
    ) 
    
    
     # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/br7tLZ5r/3.png')
    ax_image = add_image(
    im3, fig, left=0.08, bottom=-0.015, width=0.17, height=0.17
    )   # these values might differ when you are plotting


    # these values might differ when you are plotting
    im3 = plt.imread('https://i.postimg.cc/nrzX68LJ/6.png')
    ax_image = add_image(
    im3, fig, left=0.85, bottom=0.815, width=0.12, height=0.12
    )   # these values might differ when you are plotting 
   
    st.pyplot(fig)


status1 = [ "No","Yes"]
status = st.sidebar.selectbox("Show Plot",options = status1)

if status =="Yes":
    if pos == "Forward":
        forward()
    elif pos == "Midfielder":
        mid()
    elif pos== "Defender":
        defender()


st.subheader("Follow me on Twitter @Ligandro22")
