import codecs
import os

import geopandas
import pandas as pd
from shapely.geometry import Point

pd.options.mode.chained_assignment = None  # default='warn'


def convert_res11(res11_lok):
    nazwa = os.path.basename(res11_lok)
    nazwa = os.path.splitext(nazwa)[0]
    if "HDAdd" not in nazwa:
        # lokalizacja progframiku mike do konwersji res11
        read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2012\\bin\\RES11READ.exe\""
        # stworzenie folderu do zapisu wynikow
        lok_file = os.path.dirname(res11_lok)
        if not os.path.exists(lok_file + "\\GIS"):
            os.makedirs(lok_file + "\\GIS")

        res_lok = lok_file + "\\GIS"
        # ------------------------------------------------------------------------------------------------------------------------
        # wywołanie programiku res11read do konwersji res 11 na cos przystepnego xy
        os.system(read11res_lok + " -xyh " + res11_lok + " " + res_lok + "\\" + nazwa + ".csv")

        # wywalenie majkowej inwokacji pliku
        with open(res_lok + "\\" + nazwa + ".csv", 'r') as fin:
            data = fin.read().splitlines(True)

        with open(res_lok + "\\" + nazwa + ".csv", 'w') as fout:
            fout.writelines(data[19:-3])

        # dodanie nagłówka pliku na sztywny zdefiniowany w line 37
        plik = codecs.open(res_lok + "\\" + nazwa + ".csv", "r", encoding='windows-1250')
        napis = plik.readline()
        plik2 = codecs.open(res_lok + "\\" + nazwa + "_out.csv", "w", encoding='utf-8')
        # "X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\n",
        title = [" X ", "Y ", "River ", "Chainage ", "Type ", "Bottom ", "LeftBank ", "RightBank ", "X_Left ",
                 "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\r\n"]
        plik2.writelines(title)

        # usuwa powielajace sie znaki podzialu, programik z mike dzieli spacjami w roznej ilosci, tak zeby bylo
        # czytelne dla ludzi
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
        # ------------------------------------------------------------------------------------------------------------------------
        # wywolanie programiku res11read do konwersji res 11 na cos przystepnego h
        # -allres -OutputFrequency10
        os.system(read11res_lok + " -allres -FloodWatch " + res11_lok + " " + res_lok + "/" + nazwa + "_h.csv")

        with open(res_lok + "\\" + nazwa + "_h.csv") as f:
            lines = f.read().splitlines()
            ts = []
            for line in lines:
                line2 = line.split(';')
                ts.append(line2)
            # print("test ts")
            # print(ts[26][1])

        with open(res_lok + "\\" + nazwa + "_out.csv") as f:
            lines = f.read().splitlines()
            srednie_l = []
            xy = []
            for line in lines:
                line2 = line.split(' ')
                xy.append(line2[1:])
            kroki_czasowe = len(ts) - 1
            df_xy = {}
            xy[0].append("H_elev")
            for i in range(len(xy) - 1):
                srednia = (float(ts[kroki_czasowe][i + 1]) + float(ts[kroki_czasowe - 1][i + 1]) + float(
                    ts[kroki_czasowe - 2][i + 1])) / 3
                last = float(ts[kroki_czasowe][i + 1])
                differ = srednia - last

                xy[i + 1].append(last)

                srednie_l.append(differ)

            xy2 = [[row[i] for row in xy] for i in range(len(xy[0]))]
            xy = xy2
            print(xy)

            for x in range(len(xy)):
                df_xy[xy[x][0]] = xy[x][1:]

            df = pd.DataFrame(data=df_xy)
            print(df.head())

        total_rows = df.shape[0]
        print("Ilosc wierszy: ")
        print(total_rows)
        m1 = []
        m2 = []
        m3 = []
        for i in range(total_rows):
            m1.append("m1")
            m2.append("m2")
            m3.append("m3")

        m1 = pd.Series(data=m1)
        m2 = pd.Series(data=m2)
        m3 = pd.Series(data=m3)

        koryto = df[['X', 'Y', 'H_elev', 'River', 'Chainage', ]]
        koryto['M'] = m2.values

        lewy = df[['X_Marker_1', 'Y_Marker_1', 'H_elev', 'River', 'Chainage', ]]
        lewy = lewy.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y'})
        lewy['M'] = m1.values

        prawy = df[['X_Marker_3', 'Y_Marker_3', 'H_elev', 'River', 'Chainage', ]]
        prawy = prawy.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y'})
        prawy['M'] = m3.values
        frames = [koryto, lewy, prawy]

        zbiorcza = pd.concat(frames)

        writer = pd.ExcelWriter(res_lok + "\\" + nazwa + '.xlsx')
        zbiorcza.to_excel(writer, 'Sheet1')
        # df_left.to_excel(writer,'LewyBrzeg')
        # df_right.to_excel(writer,'PrawyBrzeg')
        writer.save()
        writer.close()

        zbiorcza['geometry'] = zbiorcza.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        zbiorcza = geopandas.GeoDataFrame(zbiorcza, geometry='geometry')
        zbiorcza.to_file(res_lok + "\\" + nazwa + '.shp', driver='ESRI Shapefile')

    else:
        pass
    return 0
