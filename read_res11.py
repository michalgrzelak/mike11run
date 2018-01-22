import codecs
import os
from tkinter import *
from tkinter import filedialog
from shapely.geometry import Point
import geopandas

import pandas as pd

# Selekcja pliku wynikowego res11 do stworzenia tabeli.
root = Tk()
root.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik .res11")

res11_lok = root.filename
nazwa = os.path.basename(res11_lok)
nazwa = os.path.splitext(nazwa)[0]
# lokalizacja progframiku mike do konwersji res11
read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2011\\bin\\RES11READ.exe\""
# pobranie folderu do zapisu wynikow
root.filename = filedialog.askdirectory(initialdir="/", title="Wybierz folder zapisu")
res_lok = root.filename

# wywołanie programiku res11read do konwersji res 11 na cos przystepnego
os.system(read11res_lok + " -xy -max1 " + res11_lok + " " + res_lok + "/" + nazwa + ".csv")

# wywalenie majkowej inwokacji pliku
with open(res_lok + "/" + nazwa + ".csv", 'r') as fin:
    data = fin.read().splitlines(True)

with open(res_lok + "/" + nazwa + ".csv", 'w') as fout:
    fout.writelines(data[19:-3])

# dodanie nagłówka pliku na sztywny zdefiniowany w line 37
plik = codecs.open(res_lok + "\\" + nazwa + ".csv", "r", encoding='windows-1250')
napis = plik.readline()
plik2 = codecs.open(res_lok + "\\" + nazwa + "_out.csv", "w", encoding='utf-8')
title = [" X ", "Y ", "River ", "Chainage ", "Type ", "Bottom ", "LeftBank ", "RightBank ", "X_Left ", "Y_Left ",
         "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\n", "\r\n"]
plik2.writelines(title)

# usuwa powielajace sie znaki podzialu, programik z mike dzieli spacjami w roznej ilosci, tak zeby bylo czytelne dla
# ludzi
while napis != '':
    licznik = 0
    napis = list(napis)
    while licznik < len(napis):
        if napis[licznik] == " ":
            while napis[licznik + 1] == " ":
                del napis[licznik]
        licznik += 1
    napis = "".join(napis)
    # print(napis)
    plik2.writelines(napis)
    napis = plik.readline()
plik.close()
plik2.close()

# stworzenie osobnych dataframe dla korytka i markerow jako lewy i prawy brzeg
df = pd.read_csv(res_lok + "\\" + nazwa + "_out.csv", header=0, sep=' ', index_col=0)
# print(df.head())
df_bottom = df[['X', 'Y', 'Bottom', 'River', 'Chainage', 'Type']]
df_bottom = df_bottom.rename(columns={'Bottom': 'Z'})
df_left = df[['X_Marker_1', 'Y_Marker_1', 'LeftBank', 'River', 'Chainage', 'Type']]
df_left = df_left.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y', 'LeftBank': 'Z'})
df_right = df[['X_Marker_3', 'Y_Marker_3', 'RightBank', 'River', 'Chainage', 'Type']]
df_right = df_right.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y', 'RightBank': 'Z'})

# zapisanie do excela 3 arkusze korytko lewy i prawy brzeg
writer = pd.ExcelWriter(res_lok + "\\" + nazwa + '.xlsx')
df_bottom.to_excel(writer, 'KorytoGL')
df_left.to_excel(writer, 'LewyBrzeg')
df_right.to_excel(writer, 'PrawyBrzeg')
writer.save()
writer.close()

# agregacja datafreme do jednej tabeli
frames = [df_bottom, df_left, df_right]
zbiorcza = pd.concat(frames)
# konwersja dataframe na shp

zbiorcza['geometry'] = zbiorcza.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)

zbiorcza = geopandas.GeoDataFrame(zbiorcza, geometry='geometry')
zbiorcza.to_file(res_lok + "\\" + nazwa + '.shp', driver='ESRI Shapefile')
