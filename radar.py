def show_radar():
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

    #@st.cache
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

    liga = pd.read_csv("data/streamlit.csv")
    del liga["Unnamed: 0"]
    
    from mplsoccer import Radar
    """ Functions to plot a grid of axes with an endnote and title."""

    import matplotlib.pyplot as plt
    import numpy as np

    __all__ = ['_grid_dimensions', '_draw_grid', 'grid', 'grid_dimensions']


    def _grid_dimensions(ax_aspect=1, figheight=9, nrows=1, ncols=1,
                         grid_height=0.715, grid_width=0.95, space=0.05,
                         left=None, bottom=None,
                         endnote_height=0, endnote_space=0.01,
                         title_height=0, title_space=0.01,
                         ):

        # dictionary for holding dimensions
        dimensions = {'figheight': figheight, 'nrows': nrows, 'ncols': ncols,
                      'grid_height': grid_height, 'grid_width': grid_width,
                      'title_height': title_height, 'endnote_height': endnote_height,
                      }

        if left is None:
            left = (1 - grid_width) / 2

        if title_height == 0:
            title_space = 0

        if endnote_height == 0:
            endnote_space = 0

        error_msg_height = ('The axes extends past the figure height. '
                            'Reduce one of the bottom, endnote_height, endnote_space, grid_height, '
                            'title_space or title_height so the total is ≤ 1.')
        error_msg_width = ('The grid axes extends past the figure width. '
                           'Reduce one of the grid_width or left so the total is ≤ 1.')

        axes_height = (endnote_height + endnote_space + grid_height +
                       title_height + title_space)
        if axes_height > 1:
            raise ValueError(error_msg_height)

        if bottom is None:
            bottom = (1 - axes_height) / 2

        if bottom + axes_height > 1:
            raise ValueError(error_msg_height)

        if left + grid_width > 1:
            raise ValueError(error_msg_width)

        dimensions['left'] = left
        dimensions['bottom'] = bottom
        dimensions['title_space'] = title_space
        dimensions['endnote_space'] = endnote_space

        if (nrows > 1) and (ncols > 1):
            dimensions['figwidth'] = figheight * grid_height / grid_width * (((1 - space) * ax_aspect *
                                                                              ncols / nrows) +
                                                                             (space * (ncols - 1) / (
                                                                                     nrows - 1)))
            dimensions['spaceheight'] = grid_height * space / (nrows - 1)
            dimensions['spacewidth'] = dimensions['spaceheight'] * figheight / dimensions['figwidth']
            dimensions['axheight'] = grid_height * (1 - space) / nrows

        elif (nrows > 1) and (ncols == 1):
            dimensions['figwidth'] = figheight * grid_height / grid_width * (
                    1 - space) * ax_aspect / nrows
            dimensions['spaceheight'] = grid_height * space / (nrows - 1)
            dimensions['spacewidth'] = 0
            dimensions['axheight'] = grid_height * (1 - space) / nrows

        elif (nrows == 1) and (ncols > 1):
            dimensions['figwidth'] = figheight * grid_height / grid_width * (space + ax_aspect * ncols)
            dimensions['spaceheight'] = 0
            dimensions['spacewidth'] = grid_height * space * figheight / dimensions['figwidth'] / (
                    ncols - 1)
            dimensions['axheight'] = grid_height

        else:  # nrows=1, ncols=1
            dimensions['figwidth'] = figheight * grid_height * ax_aspect / grid_width
            dimensions['spaceheight'] = 0
            dimensions['spacewidth'] = 0
            dimensions['axheight'] = grid_height

        dimensions['axwidth'] = dimensions['axheight'] * ax_aspect * figheight / dimensions['figwidth']

        return dimensions


    def _draw_grid(dimensions, left_pad=0, right_pad=0, axis=True, grid_key='grid'):

        dims = dimensions
        bottom_coordinates = np.tile(dims['spaceheight'] + dims['axheight'],
                                     reps=dims['nrows'] - 1).cumsum()
        bottom_coordinates = np.insert(bottom_coordinates, 0, 0.)
        bottom_coordinates = np.repeat(bottom_coordinates, dims['ncols'])
        grid_bottom = dims['bottom'] + dims['endnote_height'] + dims['endnote_space']
        bottom_coordinates = bottom_coordinates + grid_bottom
        bottom_coordinates = bottom_coordinates[::-1]

        left_coordinates = np.tile(dims['spacewidth'] + dims['axwidth'],
                                   reps=dims['ncols'] - 1).cumsum()
        left_coordinates = np.insert(left_coordinates, 0, 0.)
        left_coordinates = np.tile(left_coordinates, dims['nrows'])
        left_coordinates = left_coordinates + dims['left']

        fig = plt.figure(figsize=(dims['figwidth'], dims['figheight']))
        axs = []
        for idx, bottom_coord in enumerate(bottom_coordinates):
            axs.append(fig.add_axes((left_coordinates[idx], bottom_coord,
                                     dims['axwidth'], dims['axheight'])))
        axs = np.squeeze(np.array(axs).reshape((dims['nrows'], dims['ncols'])))
        if axs.size == 1:
            axs = axs.item()
        result_axes = {grid_key: axs}

        title_left = dims['left'] + left_pad
        title_width = dims['grid_width'] - left_pad - right_pad

        if dims['title_height'] > 0:
            ax_title = fig.add_axes(
                (title_left, grid_bottom + dims['grid_height'] + dims['title_space'],
                 title_width, dims['title_height']))
            if axis is False:
                ax_title.axis('off')
            result_axes['title'] = ax_title

        if dims['endnote_height'] > 0:
            ax_endnote = fig.add_axes((title_left, dims['bottom'],
                                       title_width, dims['endnote_height']))
            if axis is False:
                ax_endnote.axis('off')
            result_axes['endnote'] = ax_endnote

        if dims['title_height'] == 0 and dims['endnote_height'] == 0:
            return fig, result_axes[grid_key]  # no dictionary if just grid
        return fig, result_axes  # else dictionary


    def grid(ax_aspect=1, figheight=9, nrows=1, ncols=1,
             grid_height=0.715, grid_width=0.95, space=0.05,
             left=None, bottom=None,
             endnote_height=0, endnote_space=0.01,
             title_height=0, title_space=0.01, axis=True, grid_key='grid'):


        dimensions = _grid_dimensions(ax_aspect=ax_aspect, figheight=figheight, nrows=nrows,
                                      ncols=ncols,
                                      grid_height=grid_height, grid_width=grid_width, space=space,
                                      left=left, bottom=bottom,
                                      endnote_height=endnote_height, endnote_space=endnote_space,
                                      title_height=title_height, title_space=title_space,
                                      )
        fig, ax = _draw_grid(dimensions, axis=axis, grid_key=grid_key)
        return fig, ax



    def grid_dimensions(ax_aspect, figwidth, figheight, nrows, ncols, max_grid, space):

        if ncols > 1 and nrows == 1:
            grid1 = max_grid * figheight / figwidth * (space + ax_aspect * ncols)
            grid2 = max_grid / figheight * figwidth / (space + ax_aspect * ncols)
        elif ncols > 1 or nrows > 1:
            extra = space * (ncols - 1) / (nrows - 1)
            grid1 = max_grid * figheight / figwidth * (((1 - space) * ax_aspect *
                                                        ncols / nrows) + extra)
            grid2 = max_grid / figheight * figwidth / (((1 - space) * ax_aspect *
                                                        ncols / nrows) + extra)
        else:  # nrows=1, ncols=1
            grid1 = max_grid * figheight / figwidth * ax_aspect
            grid2 = max_grid / figheight * figwidth / ax_aspect

        # decide whether the max_grid is the grid_width or grid_height and set the other value
        if (grid1 > 1) | ((grid2 >= grid1) & (grid2 <= 1)):
            return max_grid, grid2
        return grid1, max_grid


    with open( "style2.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



    st.header(":soccer: PLAYER COMPARISION RADARS :space_invader: ")

    st.subheader(" :o: Create Radar Plots to compare any two player in Europe's Big 5 Leagues ")
    st.subheader(" :o: Compare stats with Big 5 or a specific league, set position and minimum 90s played")
    st.subheader(":o: NOTE : Set minimum 90s appropriately,set league accordingly")
    st.subheader("Data: FBREF Made by : Ligandro")
    st.dataframe(data=liga)
    st.subheader(":bar_chart: Plot:")


    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)





    col_list = liga["Player"].values.tolist()

    x1 = st.sidebar.selectbox("Name of Player 1 ",options = col_list)
    x2 = st.sidebar.selectbox("Name of Player 2 ",options = col_list)

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
    prem["Long"] =prem["Long"].astype(float)
    
    prem["npG"] =prem["npG"]/prem["90s"]
    prem["npxG"] =prem["npxG"]/prem["90s"]
    prem["Ast"] =prem["Ast"]/prem["90s"]
    prem["xA"] =prem["xA"]/prem["90s"]
    prem["KP"] =prem["KP"]/prem["90s"]
    prem["PPA"] =prem["PPA"]/prem["90s"]
    prem["1/3"] =prem["1/3"]/prem["90s"]
    prem["CrsPA"] =prem["CrsPA"]/prem["90s"]
    prem["Passes Completed"] =prem["Passes Completed"]/prem["90s"]
    prem["Prog"] =prem["Prog"]/prem["90s"]
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
    prem["ProgC"] =prem["ProgC"]/prem["90s"]
    prem["CPA"] =prem["CPA"]/prem["90s"]
    prem["Long"] =prem["Long"]/prem["90s"]



    player1 = prem.loc[prem['Player']==x1]
    player2 = prem.loc[prem['Player']==x2]

    time1 = float(player1.iloc[0,7])
    Name1 = str(player1.iloc[0,1])
    Team1 = str(player1.iloc[0,3])
    age1 =player1.iloc[0,6]

    time2 = float(player2.iloc[0,7])
    Name2 = str(player2.iloc[0,1])
    Team2 = str(player2.iloc[0,3])
    age2 =player2.iloc[0,6]


    pos1 = [ "Forward","Midfielder","Defender"]
    pos = st.sidebar.selectbox("Select Position",options = pos1)


    def forward():
        kik = prem[(prem["Pos"] == "FW") | (prem["Pos"] == "FW,DF") | (prem["Pos"] == "FW,MF")| (prem["Pos"] == "MF,FW")]

        # select stats
        playe1 = list(player1.iloc[0])
        stat1 = []
        stat1.extend([playe1[8],playe1[9],playe1[11],playe1[10],playe1[24],
              playe1[27],playe1[28],playe1[32],
              playe1[41],playe1[40],playe1[38],
              playe1[29],playe1[19] ,playe1[23],playe1[14],playe1[13]])
        # select stats
        playe2 = list(player2.iloc[0])
        stat2 = []
        stat2.extend([playe2[8],playe2[9],playe2[11],playe2[10],playe2[24],
              playe2[27],playe2[28],playe2[32],
              playe2[41],playe2[40],playe2[38],
              playe2[29],playe2[19] ,playe2[23],playe2[14],playe2[13]])


        lis = [8,9,11,10,24,27,28,32,41,40,38,29,19,23,14,13]
        params = []
        for x in lis:
            params.append(liga.columns[x])
        params[0] = "Non-Penalty\nGoals"
        params[3] = "Shots on\nTarget"
        params[4] = "Shot Creating\nActions"
        params[5] = "Dribbles\nAttempted"
        params[6] = "Dribble\nSuccess%"
        params[7] = "Carries into\nPen Box"
        params[8] = "Tackles+\nInterceptions"
        params[9] = "Aerials\nWon"
        params[10] = "Fouls\nWon"
        params[11] = "Passes\nRecieved"
        params[12] = "Passes\nCompleted"
        params[13] = "Crosses"
        params[14] = "Key\nPasses"
        params[15] = "xA"



        lower_is_better = []
        # minimum range value and maximum range value for parameters
        min_range= []
        max_range =[]
        for x in lis:
            min_range.append(kik.iloc[:,x].min())
            max_range.append(kik.iloc[:,x].max())          
        stat11 = [ round(x, 2) for x in stat1]        
        stat22 = [ round(x, 2) for x in stat2]  

        radar = Radar(params, min_range, max_range,
                  lower_is_better=lower_is_better,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*len(params),
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    # creating the figure using the grid function from mplsoccer:
        fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                        title_space=0, endnote_space=0, grid_key='radar', axis=False)

        # plot radar
        fig.set_facecolor('#15242e')
        # plot radar
        radar.setup_axis(ax=axs['radar'], facecolor='None')  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#15242e', edgecolor='white')
        radar_output = radar.draw_radar_compare(stat11, stat22, ax=axs['radar'],
                                                kwargs_radar={'facecolor': '#3FE2FF', 'alpha': 0.6,
                                                              'edgecolor': '#3FE2FF','linewidth': 4},
                                                kwargs_compare={'facecolor': '#F600BE', 'alpha': 0.6
                                                               ,'edgecolor': '#F600BE','linewidth': 4})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        #range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=17,font="monospace",color='#fcfcfc')
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=17,
                                               font="monospace",color='#fcfcfc',fontweight="bold")
        
        axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                                 c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                             c='#FF9EEC', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        
        # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
        # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
        title1_text = axs['title'].text(0.01, 0.3, Name1, fontsize=25, color='#3FE2FF',fontweight="bold",
                                    font="monospace", ha='left', va='center')
        title2_text = axs['title'].text(0.01, -0.05, Team1, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='left', va='center', color='#3FE2FF')
        title3_text = axs['title'].text(0.99, 0.3, Name2, fontsize=25,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title4_text = axs['title'].text(0.99, -0.05, Team2, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title5_text = axs['title'].text(0.099, -0.4, "90s:"+str(time1), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#3FE2FF')
        title6_text = axs['title'].text(0.99, -0.4, "90s:"+str(time2), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')

         # add subtitle
        fig.text(
        0.515, 1,
        f"Forward Stats/90 \n {League} Attackers FW,FW/MF,MF/FW,FW/DF",
        ha="center", font = "monospace",size =22,color="white",fontweight="bold"
        )
        
        
        
        # add credits
        notes = f'Only Players with 90s >= {minutes}'
        CREDIT_1 = "Data : Fbref"
        CREDIT_2 = "MPL Soccer"
        
        fig.text(
        0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )
        
        # add credits
        CREDIT_1 = "Viz : Ligandro22"
        
        fig.text(
        0.19, 0.005, f"{CREDIT_1}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )

        st.pyplot(fig)

    def mid():
        kik =  prem[(prem["Pos"] == "MF") | (prem["Pos"] == "MF,DF") ]
    
        # select stats
        playe1 = list(player1.iloc[0])
        stat1 = []
        stat1.extend([playe1[8],playe1[14],playe1[24],
              playe1[31], playe1[27],playe1[28],
              playe1[41],playe1[40],playe1[38],playe1[39],
               playe1[19], playe1[20], playe1[15],playe1[42],playe1[18],playe1[13]])

        # select stats
        playe2 = list(player2.iloc[0])
        stat2 = []
        stat2.extend([playe2[8],playe2[14],playe2[24],
              playe2[31], playe2[27],playe2[28],
              playe2[41],playe2[40],playe2[38],playe2[39],
               playe2[19], playe2[20], playe2[15],playe2[42],playe2[18],playe2[13]])


        lis = [8,14,24,31,27,28,41,40,38,39,19,20,15,42,18,13]
        params = []
        for x in lis:
            params.append(liga.columns[x])
        params[0] = "Non-Penalty\nGoals"
        params[1] = "Key\nPasses"
        params[2] = "Shot Creating\nActions"
        params[3] = "Progressive\nCarries"
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



        lower_is_better = []
        # minimum range value and maximum range value for parameters
        min_range= []
        max_range =[]
        for x in lis:
            min_range.append(kik.iloc[:,x].min())
            max_range.append(kik.iloc[:,x].max())          
        stat11 = [ round(x, 2) for x in stat1]        
        stat22 = [ round(x, 2) for x in stat2]  

        radar = Radar(params, min_range, max_range,
                  lower_is_better=lower_is_better,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*len(params),
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    # creating the figure using the grid function from mplsoccer:
        fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                        title_space=0, endnote_space=0, grid_key='radar', axis=False)

        # plot radar
           # plot radar
        fig.set_facecolor('#15242e')
        # plot radar
        radar.setup_axis(ax=axs['radar'], facecolor='None')  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#15242e', edgecolor='white')
        radar_output = radar.draw_radar_compare(stat11, stat22, ax=axs['radar'],
                                                kwargs_radar={'facecolor': '#3FE2FF', 'alpha': 0.6,
                                                              'edgecolor': '#3FE2FF','linewidth': 4},
                                                kwargs_compare={'facecolor': '#F600BE', 'alpha': 0.6
                                                               ,'edgecolor': '#F600BE','linewidth': 4})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        #range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=17,font="monospace",color='#fcfcfc')
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=17,
                                               font="monospace",color='#fcfcfc',fontweight="bold")
        
        axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                                 c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                             c='#FF9EEC', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        
        # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
        # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
        title1_text = axs['title'].text(0.01, 0.3, Name1, fontsize=25, color='#3FE2FF',fontweight="bold",
                                    font="monospace", ha='left', va='center')
        title2_text = axs['title'].text(0.01, -0.05, Team1, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='left', va='center', color='#3FE2FF')
        title3_text = axs['title'].text(0.99, 0.3, Name2, fontsize=25,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title4_text = axs['title'].text(0.99, -0.05, Team2, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title5_text = axs['title'].text(0.099, -0.4, "90s:"+str(time1), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#3FE2FF')
        title6_text = axs['title'].text(0.99, -0.4, "90s:"+str(time2), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')

         # add subtitle
        fig.text(
        0.515, 1,
        f"Midfielder Stats/90 \n {League} Midfielders MF,MF/DF",
        ha="center", font = "monospace",size =22,color="white",fontweight="bold"
        )
        
        
        
        # add credits
        notes = f'Only Players with 90s >= {minutes}'
        CREDIT_1 = "Data : Fbref"
        CREDIT_2 = "MPL Soccer"
        
        fig.text(
        0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )
        
        # add credits
        CREDIT_1 = "Viz : Ligandro22"
        
        fig.text(
        0.19, 0.005, f"{CREDIT_1}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )
        
        st.pyplot(fig)

    def defender():
        kik =  prem[(prem["Pos"] == "MF") | (prem["Pos"] == "MF,DF") ]

        # select stats
        playe1 = list(player1.iloc[0])
        stat1 = []
        stat1.extend([playe1[8],playe1[24],
              playe1[31], playe1[27],playe1[28],
              playe1[41],playe1[34],playe1[36],playe1[40],playe1[39],
              playe1[15],playe1[22],playe1[18],playe1[30],playe1[17],playe1[13]])

        playe2 = list(player2.iloc[0])
        stat2 = []
        stat2.extend([playe2[8],playe2[24],
              playe2[31], playe2[27],playe2[28],
              playe2[41],playe2[34],playe2[36],playe2[40],playe2[39],
              playe2[15],playe2[22],playe2[18],playe2[30],playe2[17],playe2[13]])


        lis = [8,24,31,27,28,41,34,36,40,39,15,22,18,30,17,13]
        params = []
        for x in lis:
            params.append(liga.columns[x])
        params[0] = "Non-Penalty\nGoals\n      "
        params[1] = "Shot Creating\nActions\n      "
        params[2] = "Progressive\nCarries\n      "
        params[3] = "Dribbles\nAttempted\n      "
        params[4] = "Dribble\nSuccess%\n      "
        params[5] = "     \nTackles+\nInterceptions"
        params[6] = "     \nShots\nBlocked"
        params[7] = "     \nClearances"
        params[8] = "     \nAerials\nWon"
        params[9] = "     \nBall\nRecoveries"
        params[10] = "     \nFinal 3rd\nPasses"
        params[11] = "     \nLong\nBalls"
        params[12] = "Progressive\nPasses\n      "
        params[13] = "Progressive\nPasses Recieved\n      "
        params[14] = "Crosses into\nPenalty Box\n      "
        params[15] = "xA\n   "



        lower_is_better = []
        # minimum range value and maximum range value for parameters
        min_range= []
        max_range =[]
        for x in lis:
            min_range.append(kik.iloc[:,x].min())
            max_range.append(kik.iloc[:,x].max())          
        stat11 = [ round(x, 2) for x in stat1]        
        stat22 = [ round(x, 2) for x in stat2]  

        radar = Radar(params, min_range, max_range,
                  lower_is_better=lower_is_better,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*len(params),
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    # creating the figure using the grid function from mplsoccer:
        fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                        title_space=0, endnote_space=0, grid_key='radar', axis=False)

        #
        fig.set_facecolor('#15242e')
        # plot radar
        radar.setup_axis(ax=axs['radar'], facecolor='None')  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#15242e', edgecolor='white')
        radar_output = radar.draw_radar_compare(stat11, stat22, ax=axs['radar'],
                                                kwargs_radar={'facecolor': '#3FE2FF', 'alpha': 0.6,
                                                              'edgecolor': '#3FE2FF','linewidth': 4},
                                                kwargs_compare={'facecolor': '#F600BE', 'alpha': 0.6
                                                               ,'edgecolor': '#F600BE','linewidth': 4})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        #range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=17,font="monospace",color='#fcfcfc')
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=17,
                                               font="monospace",color='#fcfcfc',fontweight="bold")
        
        axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                                 c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                             c='#FF9EEC', edgecolors='#6d6c6d', marker='o', s=65, zorder=2)
        
        # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
        # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
        title1_text = axs['title'].text(0.01, 0.3, Name1, fontsize=25, color='#3FE2FF',fontweight="bold",
                                    font="monospace", ha='left', va='center')
        title2_text = axs['title'].text(0.01, -0.05, Team1, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='left', va='center', color='#3FE2FF')
        title3_text = axs['title'].text(0.99, 0.3, Name2, fontsize=25,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title4_text = axs['title'].text(0.99, -0.05, Team2, fontsize=20,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')
        title5_text = axs['title'].text(0.099, -0.4, "90s:"+str(time1), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#3FE2FF')
        title6_text = axs['title'].text(0.99, -0.4, "90s:"+str(time2), fontsize=17,fontweight="bold",
                                        font="monospace",
                                        ha='right', va='center', color='#F600BE')

         # add subtitle
        fig.text(
        0.515, 1,
        f"Defender Stats/90 \n {League} Defenders DF,DF/FW,DF/MF",
        ha="center", font = "monospace",size =22,color="white",fontweight="bold"
        )
        
        
        
        # add credits
        notes = f'Only Players with 90s >= {minutes}'
        CREDIT_1 = "Data : Fbref"
        CREDIT_2 = "MPL Soccer"
        
        fig.text(
        0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )
        
        # add credits
        CREDIT_1 = "Viz : Ligandro22"
        
        fig.text(
        0.19, 0.005, f"{CREDIT_1}",
        font = "monospace",size =17,color="white",fontweight="bold",
        ha="right"
        )

        st.pyplot(fig)


    status1 = [ "No","Yes"]
    status = st.sidebar.radio("Show Plot",(status1))

    if status =="Yes":
        if pos == "Forward":
            forward()
        elif pos == "Midfielder":
            mid()
        elif pos== "Defender":
            defender()


    st.subheader("Follow me on Twitter [@Ligandro22](https://twitter.com/Ligandro22) ")
