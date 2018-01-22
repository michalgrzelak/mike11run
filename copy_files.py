import os
import shutil
from tkinter import *
from tkinter import filedialog

# ----------------------------------------------------------------------------------------------------------------------
# LISTA ROZSZERZEN DO KOPIOWANIA---------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
lista = ["cpg", "dbf", "prj", "sbn", "sbx", "shp", "shx"]


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# funkcja tworzy stringi ze sciezka pliku kopiowanego i docelowego, nastepnie wykonuje kopiowanie (shutil)
def multi_kopiarka(search_patch, paste_patch, ext):
    # puste listy i liczniki na pliki typu mike

    for root, dirs, files in os.walk(search_patch):
        for file in files:
            if file.endswith("." + ext):
                # dodanie sciezki pliku do listy
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                print(element)
                p_element = str(os.path.join(paste_patch, file))
                p_element = p_element.replace("/", "\\")
                print(p_element)
                shutil.copy(element, p_element)
    return 0


# ----------------------------------------------------------------------------------------------------------------------
# pobiera lokacje przeszukania i wklejania
root = Tk()
root.filename = filedialog.askdirectory(initialdir="/", title="Wybierz folder do przeszukiwania plikow shp")
search_lok = root.filename

root.filename = filedialog.askdirectory(initialdir="/", title="Wybierz folder do wklejenia")
paste_lok = root.filename

# ----------------------------------------------------------------------------------------------------------------------
# wywolanie kopiowania dla kazdego rozszerzenia z listy
for rozsz in lista:
    multi_kopiarka(search_lok, paste_lok, rozsz)
