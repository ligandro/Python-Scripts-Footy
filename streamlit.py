





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

def scrape(url,m):
    data = requests.get(url)
    df2 = pd.read_html(data.text, match= m)[0]
    df2.columns = df2.columns.droplevel()
    df2= df2[df2.Player != "Player"]
    return df2




df1 = scrape(url[1],matches[1])
df1["Rk"] =df1["Rk"].astype(int)
# replacing na values in college with No college
df1.fillna(0, inplace = True)


df1["Age"] =df1["Age"].astype(str)
def turn(x):
    b = x[:2]
    a = x[3:]
    a =a.lstrip("0")
    x =b +" Years, "+ a+ " Days"
    return x

df1["Age"]=df1["Age"].apply(lambda x : turn(x) )

# Change type of variable to floats
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



# **Passing Stats**

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
df2["Prog"] =df2["PrgP"].astype(float)

# applying merge with more parameters
liga = liga.merge(df2[["Rk",'Ast','xA','KP','1/3','PPA','CrsPA','Prog','Passes Completed','Passes%']], left_on="Rk", right_on="Rk",how = 'inner')





# **Pass Type Stats**

df3 = scrape(url[3],matches[3])
df3["Rk"] =df3["Rk"].astype(int)
# replacing na values in college with No college
df3.fillna(0, inplace = True)

df3["TB"] =df3["TB"].astype(float)
df3["Sw"] =df3["Sw"].astype(float)
df3["Crs"] =df3["Crs"].astype(float)

# applying merge with more parameters
# don't run this more than once
liga = liga.merge(df3[["Rk",'TB','Sw','Crs']], left_on="Rk", right_on="Rk",how = 'inner')



# **GCA AND SCA STATS**

df4 = scrape(url[4],matches[4])
df4["Rk"] =df4["Rk"].astype(int)
# replacing na values in college with No college
df4.fillna(0, inplace = True)



df4["SCA90"] =df4["SCA90"].astype(float)

# applying merge with more parameters
# don't run this more than once
liga = liga.merge(df4[["Rk",'SCA90']], left_on="Rk", right_on="Rk",how = 'inner')




# **POSSESSION STATS**

df6 = scrape(url[6],matches[6])
df6["Rk"] =df6["Rk"].astype(int)
# replacing na values in college with No college
df6.fillna(0, inplace = True)


df6["Att 3rd"] =df6["Att 3rd"].astype(float)
df6["Att Pen"] =df6["Att Pen"].astype(float)
df6["Drib"] =df6["Att"].astype(float)
df6["Drib Succ%"] =df6["Succ%"].astype(float)
df6["PRec"] =df6["Rec"].astype(float)
df6["PPRec"] =df6["PrgR"].astype(float)
df6["ProgC"] =df6["PrgC"].astype(float)
df6["CPA"] =df6["CPA"].astype(float)

# applying merge with more parameters
# don't run this more than once
liga = liga.merge(df6[["Rk","Att 3rd",'Att Pen','Drib','Drib Succ%','PRec',"PPRec","ProgC","CPA"]], left_on="Rk", right_on="Rk",how = 'inner')



# **DEFENSIVE STATS**

df5 = scrape(url[5],matches[5])
df5["Rk"] =df5["Rk"].astype(int)
# replacing na values in college with No college
df5.fillna(0, inplace = True)


df5["TklW"] =df5["TklW"].astype(float)
df5["Sh"] =df5["Sh"].astype(float)
df5["Int"] =df5["Int"].astype(float)
df5["Clr"] =df5["Clr"].astype(float)

# applying merge with more parameters
# don't run this more than once
liga = liga.merge(df5[["Rk","TklW",'Sh','Int','Clr']],left_on="Rk", right_on="Rk",how = 'inner')





# **MISCELLANEOUS STATS**

df8 = scrape(url[8],matches[8])
df8["Rk"] =df8["Rk"].astype(int)
# replacing na values in college with No college
df8.fillna(0, inplace = True)



df8["FoulsC"] =df8["Fls"].astype(float)
df8["FoulsW"] =df8["Fld"].astype(float)
df8["Recov"] =df8["Recov"].astype(float)
df8["AerialW"] =df8["Won"].astype(float)

# applying merge with more parameters
# don't run this more than once
liga = liga.merge(df8[["Rk","FoulsC",'FoulsW','Recov','AerialW']],left_on="Rk", right_on="Rk",how = 'inner')


# **FW TEMPLATE**


liga["Tkl+Int"] = liga["TklW"] + liga["Int"]


# Create extra dataframe
list0 = df2.iloc[:,0]
extra = pd.DataFrame()
extra["Rk"] =list0
list2 = df2.iloc[:, 20]
extra["Long"] = list2

# don't run this more than once
liga = liga.merge(extra[["Rk","Long"]],left_on="Rk", right_on="Rk",how = 'inner')





# saving the dataframe
liga.to_csv("data/streamlit.csv")