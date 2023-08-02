
# make sure you have done pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import json
import yaml

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
import matplotlib.colors as mcolors
from matplotlib import cm
from highlight_text import fig_text, ax_text
from matplotlib.colors import LinearSegmentedColormap, NoNorm
from matplotlib import cm
import matplotlib.gridspec as gridspec
import numpy as np
from mplsoccer import PyPizza, add_image, FontManager
from mplsoccer import Pitch, VerticalPitch
import cmasher as cmr
import matplotlib.patches as mpatches
from matplotlib.patches import RegularPolygon
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
from ast import literal_eval

from matplotlib.colors import LinearSegmentedColormap  
pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#15242e', '#4393c4'], N=10)

red_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#FFBEBE', '#FF0000'], N=10)
el_greco_violet_cmap = LinearSegmentedColormap.from_list("El Greco Violet - 10 colors",
                                                         ['#332a49', '#8e78a0'], N=10)
el_greco_yellow_cmap = LinearSegmentedColormap.from_list("El Greco Yellow - 10 colors",
                                                         ['#7c2e2a', '#f2dd44'], N=10)
flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 10 colors",
                                                  ['#e3aca7', '#c03a1d'], N=10)
# same color maps but with 100 colors
pearl_earring_cmap_100 = LinearSegmentedColormap.from_list("Pearl Earring - 100 colors",
                                                           ['#15242e', '#4393c4'], N=100)
el_greco_violet_cmap_100 = LinearSegmentedColormap.from_list("El Greco Violet - 100 colors",
                                                             ['#3b3154', '#8e78a0'], N=100)
el_greco_yellow_cmap_100 = LinearSegmentedColormap.from_list("El Greco Yellow - 100 colors",
                                                             ['#7c2e2a', '#f2dd44'], N=100)
flamingo_cmap_100 = LinearSegmentedColormap.from_list("Flamingo - 100 colors",
                                                      ['#e3aca7', '#c03a1d'], N=100)

def show_report():
    # create the driver by passing in the path of the chromedriver
    driver = webdriver.Chrome('/Users/ligandrosy/Documents/VSCODE Folders/Streamlit Pizza/Python-Scripts-Footy/driver/chromedriver')

    url = input('Enter match url:') + "#chalkboard"
    url = url.replace("Show","Live")     
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    scripts = soup.find_all('script')

    #get only the Match Centre Data
    for z in range(45,100):
        try:
            strings = scripts[z]
            if str(strings).find('matchCentreData:')>0:
                break
        except:
            pass
        


    data = strings.string

    my_new_string = data.replace("\n            ", "")
    my_new_string = my_new_string.replace("\n        ", "")
    my_new_string = my_new_string.replace(";\n    ", "")
    my_new_string = my_new_string.replace('require.config.params["args"] = ', "")
    my_new_string = my_new_string.replace("'", "")


    data =yaml.full_load(my_new_string)

    datadict = data['matchCentreData']['playerIdNameDictionary']
    datadict
    player_df = pd.DataFrame.from_dict(datadict, orient ='index') 

    player_df.columns = ['Name']

    player_df["OptaId"] = player_df.index

    player_df["OptaId"]= player_df["OptaId"].astype(float)

    ft_score = data['matchCentreData']['ftScore']


    date = data['matchCentreData']['startDate'][:10]

    codes = { "Liverpool" :26,  "Manchester City" :  167,"Arsenal" :13, "Tottenham" :  30, "Brighton" :211,
                            "Leeds United" :19,
                            "Chelsea" :15,
                        "Brentford" :189,
                "Newcastle Utd" :23,
                            "Fulham" :170, "Crystal Palace" :162,
                "Manchester Utd" :32,
                            "Everton" :31,
                        "Southampton":18,
                        "Aston Villa" :24,
                "Nott'ham Forest":174,
        "Wolves":161,
                            "West Ham" :29,
                        "Leicester City" : 14,
                    "Bournemouth" :183}


    home_team=data['matchCentreData']['home']['teamId']
    home_team = list(codes.keys())[list(codes.values()).index(home_team)]


    away_team=data['matchCentreData']['away']['teamId']
    away_team= list(codes.keys())[list(codes.values()).index(away_team)]


    codes_logo = { "Liverpool" :8650,  "Manchester City" :  8456,"Arsenal" :9825, "Tottenham" :  8586, "Brighton" :10204,
                            "Leeds United" :8463,
                            "Chelsea" :8455,
                        "Brentford" :9937,
                "Newcastle Utd" :10261,
                            "Fulham" :9879, "Crystal Palace" :9826,
                "Manchester Utd" :10260,
                            "Everton" :8668,
                        "Southampton":8466,
                        "Aston Villa" :10252,
                "Nott'ham Forest":10203,
        "Wolves":8602,
                            "West Ham" :8654,
                        "Leicester City" : 8197,
                    "Bournemouth" :8678}

    datadict = data['matchCentreData']['events']

    event_df = pd.DataFrame.from_dict(datadict) 

    event_df = event_df.merge(player_df[["OptaId","Name"]],left_on='playerId',right_on='OptaId',how='left')

    for index, row in event_df.iterrows():
        x = event_df.loc[index, 'type']
        event_df.loc[index, 'type'] = x["displayName"]
        y = event_df.loc[index, 'outcomeType']
        event_df.loc[index, 'outcomeType'] = y["displayName"]
        
    def heatmap_data():
        global player_name
        df = event_df.copy()
        ars = df[(df["isTouch"] == True)]
        data_touch = ars[ars.Name == player_name]
        return data_touch


    def drib(ax1):
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "TakeOn") ]

        data_drib = ars[ars.Name == player_name]
        pitch = VerticalPitch(
            pitch_color='#15242e',pitch_type='opta',goal_type='box',linewidth=.85,
            line_color='#cfcfcf')
        pitch.draw(ax = ax1)
        
            
        # -- We plot the scatter (also with inverted coords)
        df_plot_succ = data_drib[data_drib["outcomeType"] == "Successful"]
        df_plot_unsucc = data_drib[data_drib["outcomeType"] == "Unsuccessful"]
        ax.scatter(df_plot_unsucc.y, df_plot_unsucc.x, s=15, alpha=1, lw=0.7,ec="black", color='#9C1735', zorder=5)
        ax.scatter(df_plot_succ.y, df_plot_succ.x, s=80, alpha=1, lw=0.5,ec="black", color='#FFD230', zorder=5,marker="*")
        
        ars = df[(df["isTouch"] == True)]
        data_touch = ars[ars.Name == player_name]
        pitch.kdeplot(
        data_touch.x, data_touch.y, 
        ax=ax1, shade=True, 
        levels=30, shade_lowest=True,
        cut=4, zorder=-1, cmap=pearl_earring_cmap_100)
        ax1.scatter(data_touch.y, data_touch.x, s=5, alpha=0.8, lw=1.2, color='#00BB02', zorder=3)
        
    def drib_data():
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "TakeOn") ]

        data_drib = ars[ars.Name == player_name]
        return data_drib


    def check_if_pass_is_progressive(x, y, end_x, end_y):
        '''
        This function returns "True" if the pass meets the criteria
        for a progressive pass.
        '''
        # -- Start position
        height_start = abs(x - 100)
        length_start = abs(y - 50)
        distance_sq_start = height_start**2 + length_start**2
        distance_start = distance_sq_start**(1/2)
        # -- End position
        height_end = abs(end_x - 100)
        length_end = abs(end_y - 50)
        distance_sq_end = height_end**2 + length_end**2
        distance_end = distance_sq_end**(1/2)
        # -- Calculate change in distance
        delta_distance = distance_end/distance_start - 1
        if delta_distance <= -0.25:
            return True
        else:
            return False

    def passmap(ax1):  
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "Pass") ]
        data_passes =ars[ars.Name == player_name]

        pd.options.mode.chained_assignment = None  # default='warn'
        data_passes["is_assist"] = False
        goal_id = [47,48,49,50,51,52]
        for index, row in data_passes.iterrows():
            if len(set(goal_id).intersection(set(row["satisfiedEventsTypes"]))) > 0:
                data_passes.loc[index, 'is_assist'] = True
                

        data_passes["is_key"] = False
        goal_id = [39,40,41,42,43,44,45,46,47,48,49,50,51,52]
        for index, row in data_passes.iterrows():
            if len(set(goal_id).intersection(set(row["satisfiedEventsTypes"]))) > 0:
                data_passes.loc[index, 'is_key'] = True
                
        data_passes['is_progressive'] = data_passes.apply(lambda x: 
                                                    check_if_pass_is_progressive(x['x'], x['y'],
                                                                                x['endX'], x['endY']),
                                                    axis=1)

        
        pitch = VerticalPitch(line_color='#cfcfcf',
                line_zorder=2, 
                pitch_color='#15242e',
                pitch_type='opta',
                goal_type='box',
                linewidth=.85
                    )
        pitch.draw(ax = ax1)

        #pitch = VerticalPitch(line_color='#cfcfcf', line_zorder=2, pitch_color='#15242e')
        
        # - We need to invert the coordinates because of the Vertical Pitch!!
        for index, pass_made in data_passes.iterrows():
            if pass_made["outcomeType"] == "Successful":
                color = '#00BB02'
            else:
                color = '#FF2600'
            x = pass_made['y']
            y = pass_made['x']
            dx = pass_made['endY']
            dy = pass_made['endX']
            pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec='None',
                                                fc='#efe9e6',arrowstyle='-|>,head_length=2.6,head_width=1.2', zorder=4)
            ax.add_patch(pass_arrow)
            pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec=color,
                                                fc='None',arrowstyle='-|>,head_length=3,head_width=2', zorder=2)
            ax1.add_patch(pass_arrow)
            # - We need to invert the coordinates because of the Vertical Pitch!!
        for index, pass_made in data_passes.iterrows():
            if (pass_made["is_assist"] == True) | (pass_made["is_key"] ==  True):
                if pass_made["is_assist"] == True:
                    color = '#38B6FF'
                elif pass_made["is_key"] ==  True:
                    color = '#FDEC09'
                x = pass_made['y']
                y = pass_made['x']
                dx = pass_made['endY']
                dy = pass_made['endX']
                pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec='None',
                                                fc='#efe9e6',arrowstyle='-|>,head_length=2.6,head_width=1.2', zorder=4)
                ax1.add_patch(pass_arrow)
                pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec=color,
                                                fc='None',arrowstyle='-|>,head_length=3,head_width=2', zorder=2)
                ax1.add_patch(pass_arrow)
                
                
        from matplotlib.colors import LinearSegmentedColormap  
        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#15242e', '#4393c4'], N=10)
        pitch.kdeplot(
        data_passes.x, data_passes.y, 
        ax=ax1, shade=True, 
        levels=20,
        cut=4, zorder=-5,
        cmap=pearl_earring_cmap_100 )
        
        # -- We plot the scatter (also with inverted coords)
        df_plot_passes_succ = data_passes[data_passes["outcomeType"] =="Successful"]
        success = len(df_plot_passes_succ)
        df_plot_passes_unsucc = data_passes[data_passes["outcomeType"] !="Successful"]
        #ax1.scatter(df_plot_passes_succ.y, df_plot_passes_succ.x, s=10, alpha=0.8, lw=0.5,ec="white", color='#00BB02', zorder=4)
        #ax1.scatter(df_plot_passes_unsucc.y, df_plot_passes_unsucc.x, s=7, alpha=0.8, lw=0.3,ec="white", color='#FF2600', zorder=4)
        prog =len(data_passes[data_passes['is_progressive'] == True] )
        return data_passes 

    def passmap_data():  
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "Pass") ]
        data_passes =ars[ars.Name == player_name]

        pd.options.mode.chained_assignment = None  # default='warn'
        data_passes["is_assist"] = False
        goal_id = [47,48,49,50,51,52]
        for index, row in data_passes.iterrows():
            if len(set(goal_id).intersection(set(row["satisfiedEventsTypes"]))) > 0:
                data_passes.loc[index, 'is_assist'] = True
                

        data_passes["is_key"] = False
        goal_id = [39,40,41,42,43,44,45,46,47,48,49,50,51,52]
        for index, row in data_passes.iterrows():
            if len(set(goal_id).intersection(set(row["satisfiedEventsTypes"]))) > 0:
                data_passes.loc[index, 'is_key'] = True
                
                
        data_passes['is_progressive'] = data_passes.apply(lambda x: 
                                                    check_if_pass_is_progressive(x['x'], x['y'],
                                                                                x['endX'], x['endY']),
                                                    axis=1)


        return data_passes





    zone_areas = {
        'zone_1':{
            'x_lower_bound': 79, 'x_upper_bound': 100,
            'y_lower_bound': 83, 'y_upper_bound': 100,
        },
        'zone_2':{
            'x_lower_bound': 0, 'x_upper_bound': 21,
            'y_lower_bound': 83, 'y_upper_bound': 100,
        },
        'zone_3':{
            'x_lower_bound': 79, 'x_upper_bound': 100,
            'y_lower_bound': 20, 'y_upper_bound': 83,
        },
        'zone_4':{
            'x_lower_bound': 0, 'x_upper_bound': 21,
            'y_lower_bound': 20, 'y_upper_bound': 83,
        },
        'zone_5':{
            'x_lower_bound': 21, 'x_upper_bound': 36.8,
            'y_lower_bound': 83, 'y_upper_bound': 100,
        },
        'zone_6':{
            'x_lower_bound': 63.2, 'x_upper_bound': 79,
            'y_lower_bound': 83, 'y_upper_bound': 100,
        },
        'zone_7':{
            'x_lower_bound': 36.8, 'x_upper_bound': 63.2,
            'y_lower_bound': 83, 'y_upper_bound': 94.1,
        },
        'zone_8':{
            'x_lower_bound': 36.8, 'x_upper_bound': 63.2,
            'y_lower_bound': 94.1, 'y_upper_bound': 100,
        },
        'zone_9':{
            'x_lower_bound': 21, 'x_upper_bound': 36.8,
            'y_lower_bound': 70, 'y_upper_bound': 83,
        },
        'zone_10':{
            'x_lower_bound': 63.2, 'x_upper_bound': 79,
            'y_lower_bound': 70, 'y_upper_bound': 83,
        },
        'zone_11':{
            'x_lower_bound': 36.8, 'x_upper_bound': 63.2,
            'y_lower_bound': 70, 'y_upper_bound': 83,
        },
        'zone_12':{
            'x_lower_bound': 21, 'x_upper_bound': 79,
            'y_lower_bound': 20, 'y_upper_bound': 70,
        }
    }



    def assign_shot_zone(x,y):
        '''
        This function returns the zone based on the x & y coordinates of the shot
        taken.
        Args:
            - x (float): the x position of the shot based on a vertical grid.
            - y (float): the y position of the shot based on a vertical grid.
        '''

        global zone_areas

        # Conditions

        for zone in zone_areas:
            if (y >= zone_areas[zone]['x_lower_bound']) & (y <= zone_areas[zone]['x_upper_bound']):
                if (x >= zone_areas[zone]['y_lower_bound']) & (x <= zone_areas[zone]['y_upper_bound']):
                    return zone


    def shotmap(ax1):
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["isShot"] == True) ]
        aux_data =ars[ars.Name == player_name]
        
        pd.options.mode.chained_assignment = None  # default='warn'
        aux_data['is_target'] = False
        goal_id = [9]
        for index, row in aux_data.iterrows():
            if len(set(goal_id).intersection((set(row["satisfiedEventsTypes"])))) > 0:
                aux_data.loc[index, 'is_target'] = True
                
                
        aux_data['zone_area'] = [assign_shot_zone(x,y) for x,y in zip(aux_data['x'], aux_data['y'])]


        
        pitch = VerticalPitch(
            pitch_color='#15242e',pitch_type='opta',goal_type='box',linewidth=.85,
            line_color='#cfcfcf',
            half = True)
        
        pitch.draw(ax = ax1)
        
        data_shot_groupped = aux_data.groupby(['zone_area']).size().reset_index(name='count')
        
        for zone in data_shot_groupped['zone_area']:
            shot_pct = data_shot_groupped[data_shot_groupped['zone_area'] == zone]['count']
            x_lim = [zone_areas[zone]['x_lower_bound'], zone_areas[zone]['x_upper_bound']]
            y1 = zone_areas[zone]['y_lower_bound']
            y2 = zone_areas[zone]['y_upper_bound']
            ax1.fill_between(
                x=x_lim, 
                y1=y1, y2=y2, 
                color="#38B6FF", alpha=(shot_pct/len(aux_data)),zorder=1, ec='None')
            
        # -- We plot the scatter (also with inverted coords)
        df_plot_succ = aux_data[(aux_data['isGoal'] == True) & (aux_data['is_target'] == True)]
        df_plot_succ_t = aux_data[(aux_data['isGoal'] == True) & (aux_data['is_target'] == False)]
        df_plot_unsucc = aux_data[(aux_data['isGoal'] != True) & (aux_data['is_target'] == True)]
        df_plot_unsucc_t = aux_data[(aux_data['isGoal'] != True) & (aux_data['is_target'] == False)]
        ax1.scatter(df_plot_succ.y, df_plot_succ.x, s=20, alpha=1,marker ="^", lw=0.3,ec="white", color='#FFDF37', zorder=5)
        ax1.scatter(df_plot_unsucc.y, df_plot_unsucc.x, s=20, alpha=1,marker ="^", lw=0.3, ec="white",color='#EA1F29', zorder=5)
        ax1.scatter(df_plot_succ_t.y, df_plot_succ_t.x, s=18, alpha=1, lw=1.2, color='#FFDF37', zorder=5)
        ax1.scatter(df_plot_unsucc_t.y, df_plot_unsucc_t.x, s=18, alpha=1, lw=1.2, color='#EA1F29', zorder=5)



        # - We need to invert the coordinates because of the Vertical Pitch!!
        for index, shot_made in df_plot_succ.iterrows():
            x = shot_made['y']
            y = shot_made['x']
            dx = shot_made['goalMouthY']
            dy = 101
            pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec='None',
                                                fc='#FFDF37',arrowstyle='-|>,head_length=0.1,head_width=1', zorder=4)
            ax1.add_patch(pass_arrow)
            pass_arrow = mpatches.FancyArrowPatch((x,y), (dx, dy), ec="#FFDF37",
                                                fc='None',arrowstyle='-|>,head_length=2.8,head_width=1.5', zorder=2)
            ax1.add_patch(pass_arrow)
            
            
        return aux_data



    def shotmap_data():
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["isShot"] == True) ]
        aux_data =ars[ars.Name == player_name]
        
        pd.options.mode.chained_assignment = None  # default='warn'
        aux_data['is_target'] = False
        goal_id = [9]
        for index, row in aux_data.iterrows():
            if len(set(goal_id).intersection((set(row["satisfiedEventsTypes"])))) > 0:
                aux_data.loc[index, 'is_target'] = True
                
        aux_data['zone_area'] = [assign_shot_zone(x,y) for x,y in zip(aux_data['x'], aux_data['y'])]

            
        return aux_data



    def ball(ax1):
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "BallRecovery") ]
        data_recoveries = ars[ars.Name == player_name]



        total = len(data_recoveries)
        pitch = VerticalPitch(
            pitch_color='#15242e',pitch_type='opta',goal_type='box',linewidth=.85,
            line_color='#cfcfcf')
        pitch.draw(ax = ax1)
        # Here we can get the positional dimensions
        pos_x = pitch.dim.positional_x
        pos_y = pitch.dim.positional_y

        
        
        data_recoveries = data_recoveries.assign(bins_x = lambda x: pd.cut(x.y, bins=pos_x))
        data_recoveries = data_recoveries.assign(bins_y = lambda x: pd.cut(x.x, bins=pos_y))
        data_recoveries_groupped = data_recoveries.groupby(['bins_x', 'bins_y']).size().reset_index(name='count')
        data_recoveries_groupped['left_x'] = data_recoveries_groupped['bins_x'].apply(lambda x: x.left)
        data_recoveries_groupped['right_x'] = data_recoveries_groupped['bins_x'].apply(lambda x: x.right)
        data_recoveries_groupped['left_y'] = data_recoveries_groupped['bins_y'].apply(lambda x: x.left)
        data_recoveries_groupped['right_y'] = data_recoveries_groupped['bins_y'].apply(lambda x: x.right)






        counter = 1
        for index_y, y in enumerate(pos_y):
            for index_x, x in enumerate(pos_x):
                try:
                    lower_y = pos_y[index_y]
                    lower_x = pos_x[index_x]
                    upper_y = pos_y[index_y + 1]
                    upper_x = pos_x[index_x + 1]
                except:
                    continue
                condition_bounds = (data_recoveries_groupped['left_x'] >= lower_x) & (data_recoveries_groupped['right_x'] <= upper_x)& (data_recoveries_groupped['left_y'] >= lower_y) & (data_recoveries_groupped['right_y'] <= upper_y)
                alpha = data_recoveries_groupped[condition_bounds]['count'].iloc[0]/data_recoveries_groupped['count'].max()
                if alpha > 0:
                    ax.fill_between(
                    x=[lower_x, upper_x],
                    y1=lower_y,
                    y2=upper_y,
                    color='#38B6FF',
                    zorder=0,
                    alpha=alpha*.6,
                    ec='None'
                )
            counter += 1
            
            
        ax.scatter(data_recoveries.y, data_recoveries.x, 
            s=40, alpha=0.85, lw=0.85, fc='#FFFFFF', ec='#EA1F29', zorder=3)


    def ball_recovdata():
        global player_name
        df = event_df.copy()
        ars = event_df[(event_df["type"] == "BallRecovery") ]
        data_recoveries = ars[ars.Name == player_name]
        return data_recoveries


    fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (12,6), dpi = 100)

    fig.set_facecolor('#15242e')
    plt.rcParams['hatch.linewidth'] = .02

    names =[x for x in player_df.Name.values]
    numbers = [ x for x in range(1,len(player_df)+1)]

    user_input = 0

    input_message = "Pick an option:\n"

    for index, item in enumerate(names):
        input_message += f'{index+1}) {item}\n'

    input_message += 'Your choice: '

    while user_input not in numbers:
        user_input = int(input(input_message))

    print('You picked: ' + names[int(user_input) -1])


    # one-liner
    player_name =names[int(user_input) -1]

    fotmob_id = int(event_df[event_df.Name == player_name].teamId.unique())
    fotmob_id = list(codes.keys())[list(codes.values()).index(fotmob_id)]
    fotmob_id = codes_logo[fotmob_id]



    names =["Attacker","Defender"]
    numbers = [ x for x in range(1,len(names)+1)]

    user_input = 0

    input_message = "Pick an option:\n"

    for index, item in enumerate(names):
        input_message += f'{index+1}) {item}\n'

    input_message += 'Your choice: '

    while user_input not in numbers:
        user_input = int(input(input_message))

    print('You picked: ' + names[int(user_input) -1])

    if user_input ==1 :
        for index, ax in enumerate(axes.flat):
            if index == 0:
                drib(ax)
            elif index == 1:
                passmap(ax)
            else :
                shotmap(ax)

    else :
        for index, ax in enumerate(axes.flat):
            if index == 0:
                drib(ax)
            elif index == 1:
                passmap(ax)
            else :
                ball(ax)


    if len(player_name) > 20:
        fn = 15
    elif len(player_name) > 15:
        fn = 17
    else : 
        fn = 23


    # NAME
    #FFD230,38B6FF
    fig_text(
        x = 0.193, y = .932, 
        s = f'<{player_name}>',
        highlight_textprops=[{"color":"#FFD230", "style":"italic"}],
        fontname ="Rockwell",path_effects=[path_effects.Stroke(linewidth=0.4, foreground="#BD8B00"), path_effects.Normal()],
        va = 'bottom', ha = 'left',
        fontsize = fn,  weight = 'bold',color="white"
    )


    # HEATMAP
    data_touch = heatmap_data()
    str_text = f'''Total Touches: <{len(data_touch)}> '''
    fig_text(
        x = 0.2, y = 0.88, 
        s = str_text,highlight_textprops=[{'color':'#00BB02', 'weight':'bold'}],
        va = 'bottom', ha = 'left',fontname ="Futura",
        fontsize = 10,color ='white'
    )

    # DRIBBLE
    data_drib = drib_data()
    str_text = f'''Dribbles Attempted : {len(data_drib)} | Successful : <{len(data_drib[data_drib["outcomeType"] == "Successful"])}> '''
    fig_text(
        x = 0.135, y = 0.847, 
        s = str_text,highlight_textprops=[{'color':'#FFD230', 'weight':'bold'}],
        va = 'bottom', ha = 'left',fontname ="Futura",
        fontsize = 10,color ='white'
    )


    # PASSMAP
    data_passes = passmap_data()
    total =len(data_passes)

    df_plot_passes_succ = data_passes[data_passes["outcomeType"] =="Successful"]

    succes_rate = df_plot_passes_succ.shape[0]/(data_passes.shape[0])
    prog = len(data_passes[data_passes['is_progressive'] == True] )

    str_text = f'''Passes attempted : {total} | Successful :<{succes_rate:.0%}>\nProgressive Passes : {prog}|  Assist : <{len(data_passes[data_passes["is_assist"] == True])}> | Key Passes : <{len(data_passes[data_passes["is_key"] == True])}>
    '''


    fig_text(
        x = 0.38, y = 0.837, 
        s = str_text,highlight_textprops=[{'color':'#00FF5B', 'weight':'bold'},{'color':'#38B6FF', 'weight':'bold'},{'color':'#FDEC09', 'weight':'bold'}],
        va = 'bottom', ha = 'left',fontname ="Futura",
        fontsize = 10,color ='white'
    )


    # SHOTMAP


    if user_input ==1 :
        h =138
        fig_text(
            x = 0.712, y = .373,  s = "Goal : ",fontname ="Futura",
            va = 'bottom', ha = 'left',
            fontsize = 8,  weight = 'bold',color="white")
        
        ax.scatter(70, 57, s=18, alpha=1, lw=1.2, color='#FFDF37', zorder=5)
        
        fig_text(
        x = 0.69, y = .343, 
        s = "Non-Goal :",
        fontname ="Futura",
        va = 'bottom', ha = 'left',
        fontsize = 8,  weight = 'bold',color="white"
        )
        
        ax.scatter(70,52, s=18, alpha=1, lw=1.2, color='#EA1F29', zorder=5)
        
        fig_text(
            x = 0.82, y = .372, s = "On Target : ",
        fontname ="Futura",
        va = 'bottom', ha = 'left',
        fontsize = 8,  weight = 'bold',color="white")
        
        ax.scatter(8, 57, s=20, alpha=1,marker ="^", lw=0.3,ec="white",color='#FFDF37', zorder=5)

        aux_data= shotmap_data()
        total  = len(aux_data)
        str_text = f'''Total Shots : <{total}> | Shots on Target : {len(aux_data[ (aux_data['is_target'] == True)] )} | Goals: <{len(aux_data[(aux_data['isGoal'] == True)])}>'''


        fig_text(
        x = 0.662, y = 0.697, 
        s = str_text,highlight_textprops=[{'color':'#00FF5B', 'weight':'bold'},{'color':'#FFDF37', 'weight':'bold'}],
        va = 'bottom', ha = 'left',fontname ="Futura",
        fontsize = 10,color ='white')
            
    else :
        h = 110
        ball_recov= ball_recovdata()
        total  = len(ball_recov)
        str_text = f'''Total Ball Recoveries : <{total}> '''
        fig_text(
                x = 0.712, y = 0.843, 
                s = str_text,highlight_textprops=[{'color':'#00FF5B', 'weight':'bold'}],
                va = 'bottom', ha = 'left',fontname ="Futura",
                fontsize = 10,color ='white')
        str_text = f'''Ball Recoveries include Tackles,\nInterceptions,Clearances and Aerials '''
        fig_text(
                x = 0.712, y = 0.105, 
                s = str_text,
                va = 'bottom', ha = 'left',fontname ="Futura",
                fontsize = 8,color ='white')

        
        
    # add league logo PREM,L1,SI,LIGA,uefa,euro
    im1 = plt.imread('/Users/ligandrosy/Downloads/PREM.png')
    ax_image = add_image(
            im1, fig, left=0.1, bottom=0.892, width=0.12, height=0.12
        )   # these values might differ when you are plotting





    clubs = fotmob_id 

    # -- Add Fancy Logo and Text
    DC_to_FC = ax.transData.transform
    FC_to_NFC = fig.transFigure.inverted().transform
    # -- Take data coordinates and transform them to normalized figure coordinates
    DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))
    ax_coords = DC_to_NFC((30,h))
    ax_size = .09
    image_ax = fig.add_axes(
        [ax_coords[0], ax_coords[1], ax_size, ax_size],
        fc='None'
    )
    fotmob_url = 'https://images.fotmob.com/image_resources/logo/teamlogo/'
    player_face = Image.open(urllib.request.urlopen(f"{fotmob_url}{clubs}.png"))
    image_ax.imshow(player_face)
    image_ax.axis("off")




    # CREDIT
    str_text = f'''Viz by @Ligandro22 | Data source: Opta '''


    fig_text(
        x = 0.405, y = 0.111, 
        s = str_text,
        va = 'bottom', ha = 'left',fontname ="Futura",
        fontsize = 10,color ='white'
    )


    # Match
    str_text = f"{home_team} <{ft_score}> {away_team}\n         {date}"
    

    fig_text(
        x = 0.48, y = 0.94, 
        s = str_text,highlight_textprops=[{'color':'#00FF5B', 'weight':'bold'}],
        va = 'bottom', ha = 'left',fontname ="Rockwell",
        fontsize = 10,color ='white'
    )
    st.pyplot(fig)
            