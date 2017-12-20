import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import codecs
from shapely.geometry import Point
import geopandas

def convert_res11(res11_lok):

    nazwa = os.path.basename(res11_lok)
    nazwa = os.path.splitext(nazwa)[0]
    if "HDAdd" not in nazwa:
        #lokalizacja progframiku mike do konwersji res11
        read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2011\\bin\\RES11READ.exe\""
        #stworzenie folderu do zapisu wynikow
        lok_file = os.path.dirname(res11_lok)
        if not os.path.exists(lok_file+"\\GIS"):
            os.makedirs(lok_file+"\\GIS")

        res_lok = lok_file+"\\GIS"
    #------------------------------------------------------------------------------------------------------------------------
        # wywołanie programiku res11read do konwersji res 11 na cos przystepnego xy
        os.system(read11res_lok + " -xyh " + res11_lok + " " + res_lok+"\\"+nazwa+".csv")


        #wywalenie majkowej inwokacji pliku
        with open(res_lok+"\\"+nazwa+".csv", 'r') as fin:
            data = fin.read().splitlines(True)

        with open(res_lok+"\\"+nazwa+".csv", 'w') as fout:
            fout.writelines(data[19:-3])

        #dodanie nagłówka pliku na sztywny zdefiniowany w line 37
        plik = codecs.open(res_lok+"\\"+nazwa+".csv", "r", encoding = 'windows-1250')
        napis = plik.readline()
        plik2 = codecs.open(res_lok+"\\"+nazwa+"_out.csv", "w", encoding = 'utf-8')
        #"X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\n",
        title = [" X ", "Y ", "River ", "Chainage ", "Type ", "Bottom ", "LeftBank ", "RightBank ", "X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\r\n"]
        plik2.writelines(title)

        # usuwa powielajace sie znaki podzialu, programik z mike dzieli spacjami w roznej ilosci, tak zeby bylo czytelne dla ludzi
        while napis != '':
            licznik = 0
            napis = list(napis)
            while licznik < len(napis):
                if napis[licznik] == " ":
                    while napis[licznik + 1] == " ":
                        del napis[licznik]
                licznik += 1
            napis = "".join(napis)
            #print(napis)
            plik2.writelines(napis)
            napis = plik.readline()
        plik.close()
        plik2.close()
    #------------------------------------------------------------------------------------------------------------------------
        # wywolanie programiku res11read do konwersji res 11 na cos przystepnego h
        #-allres -OutputFrequency10
        os.system(read11res_lok + " -allres -FloodWatch " + res11_lok + " " + res_lok+"/"+nazwa+"_h.csv")

        """
        #wywalenie majkowej inwokacji pliku
        with open(res_lok+"/"+nazwa+"_h.csv", 'r') as fin:
            data = fin.read().splitlines(True)

        with open(res_lok+"/"+nazwa+"_h.csv", 'w') as fout:
            fout.writelines(data[20:-3])
        
        #dodanie nagłówka pliku na sztywny zdefiniowany w line 37
        plik = codecs.open(res_lok+"\\"+nazwa+"_h.csv", "r", encoding = 'windows-1250')
        napis = plik.readline()

        plik2 = codecs.open(res_lok+"\\"+nazwa+"_out_h.csv", "w", encoding = 'utf-8')
        #title = [" River2 ", "Chainage2 ", "h_elev","\r\n"]
        #plik2.writelines(title)

        # usuwa powielajace sie znaki podzialu, programik z mike dzieli spacjami w roznej ilosci, tak zeby bylo czytelne dla ludzi
        licznik_lines = 0
        while napis != '':
            licznik = 0
            napis = list(napis)
            while licznik < len(napis):
                if napis[licznik] == " ":
                    while napis[licznik + 1] == " ":
                        del napis[licznik]
                licznik += 1

            napis = "".join(napis)
            print(napis)
            if licznik_lines < 2 :
                napis = napis.split(" ")
                print(napis)
                napis[0]= "Data"
                print(napis)
            if licznik_lines >= 2:
                napis = napis.split(" ")
                data = napis[:6]
                new_data = ""
                for item in data:
                    if len(item)<2:
                        new_item = "-0"+str(item)
                        new_data = new_data + new_item
                    elif len(item)>1 and len(item)<3:
                        new_data = new_data+"-"+str(item)
                    elif len(item)>3:
                        new_data = new_data + str(item)
                dane = napis[6:]
                print(new_data, dane)
                dane.insert(0,new_data)
                napis = dane
            licznik_lines += 1

            napis = "".join(napis)
            plik2.writelines(napis)
            napis = plik.readline()
        plik.close()
        plik2.close()
        """
    #------------------------------------------------------------------------------------------------------------------------
        """
        #stworzenie osobnych dataframe dla korytka i markerow jako lewy i prawy brzeg
        df = pd.read_csv(res_lok+"\\"+nazwa+"_out.csv", header=0, sep=' ',index_col=0)
        #print(df.head())
        df_bottom = df
        #[['X', 'Y', 'Bottom', 'River', 'Chainage', 'Type']]
        df_bottom = df_bottom[df_bottom.Type != 2]
        df_bottom = df_bottom.rename(columns={'Bottom': 'Z'})
        df = pd.read_csv(res_lok+"\\"+nazwa+"_h.csv", header=0, sep=';',index_col=0)
        #df_bottom = pd.concat([df_bottom, df], axis=1)
        #df_bottom = df_bottom[['X', 'Y', 'Z', 'h_elev', 'River', 'Chainage', 'X_Marker_1', 'Y_Marker_1', 'X_Marker_3', 'Y_Marker_3']]
        print(df.head())
        #df_left = df[['X_Marker_1', 'Y_Marker_1', 'LeftBank', 'River', 'Chainage', 'Type']]
        #df_left = df_left.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y', 'LeftBank': 'Z'})
        #df_right = df[['X_Marker_3', 'Y_Marker_3', 'RightBank', 'River', 'Chainage', 'Type']]
        #df_right = df_right.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y', 'RightBank': 'Z'})
        

        #zapisanie do excela 3 arkusze korytko lewy i prawy brzeg
        writer = pd.ExcelWriter(res_lok+"\\"+nazwa+'.xlsx')
        df_bottom.to_excel(writer,'KorytoGL')
        #df_left.to_excel(writer,'LewyBrzeg')
        #df_right.to_excel(writer,'PrawyBrzeg')
        writer.save()
        writer.close()

        #agregacja datafreme do jednej tabeli
        #frames = [df_bottom, nnn]
        #zbiorcza = pd.concat(frames)
        zbiorcza = df_bottom
        #konwersja dataframe na shp

        """

        with open(res_lok+"\\"+nazwa+"_h.csv") as f:
            lines = f.read().splitlines()
            TS = []
            for line in lines:
                line2 = line.split(';')
                TS.append(line2)
            #print("test TS")
            #print(TS[26][1])

        with open(res_lok+"\\"+nazwa+"_out.csv") as f:
            lines = f.read().splitlines()
            srednie_L=[]
            XY = []
            for line in lines:
                line2 = line.split(' ')
                XY.append(line2[1:])
            kroki_czasowe = len(TS)-1
            df_XY = {}
            XY[0].append("H_elev")
            for i in range(len(XY)-1):

                srednia = (float(TS[kroki_czasowe][i+1])+float(TS[kroki_czasowe-1][i+1])+float(TS[kroki_czasowe-2][i+1]))/3
                last = float(TS[kroki_czasowe][i+1])
                differ = srednia - last

                XY[i+1].append(last)

                srednie_L.append(differ)


            XY2 = [[row[i] for row in XY] for i in range(len(XY[0]))]
            XY = XY2
            print(XY)

            for x in range(len(XY)):
                df_XY[XY[x][0]] = XY[x][1:]

            df = pd.DataFrame(data=df_XY)
            print(df.head())

        total_rows = df.shape[0]
        print("Ilosc wierszy: ")
        print(total_rows)
        M1 = []
        M2 = []
        M3 = []
        for i in range(total_rows):
            M1.append("M1")
            M2.append("M2")
            M3.append("M3")

        M1 = pd.Series(data=M1); M2 = pd.Series(data=M2); M3 = pd.Series(data=M3)

        koryto = df[['X', 'Y', 'H_elev', 'River', 'Chainage',]]
        koryto['M'] = M2.values

        lewy = df[['X_Marker_1', 'Y_Marker_1', 'H_elev', 'River', 'Chainage',]]
        lewy = lewy.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y'})
        lewy['M'] = M1.values

        prawy = df[['X_Marker_3', 'Y_Marker_3', 'H_elev', 'River', 'Chainage', ]]
        prawy = prawy.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y'})
        prawy['M'] = M3.values
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


        """
        koryto['geometry'] = koryto.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        koryto = geopandas.GeoDataFrame(koryto, geometry='geometry')
        koryto.to_file(res_lok + "\\" + nazwa + '_koryto.shp', driver='ESRI Shapefile')

        lewy['geometry'] = lewy.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        lewy = geopandas.GeoDataFrame(lewy, geometry='geometry')
        lewy.to_file(res_lok + "\\" + nazwa + '_lewy.shp', driver='ESRI Shapefile')

        prawy['geometry'] = prawy.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        prawy = geopandas.GeoDataFrame(prawy, geometry='geometry')
        prawy.to_file(res_lok + "\\" + nazwa + '_prawy.shp', driver='ESRI Shapefile')
        """
    else:
        pass
    return (0)

