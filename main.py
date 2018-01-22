from time import sleep
from tkinter import *
from tkinter import filedialog

from func_convert_sim11 import convert_res11
from listowanie_sim11 import sim11_index_unite

root = Tk()
root.filename = filedialog.askdirectory(initialdir="/", title="Wybierz folder do przeszukiwania (sim11)")
main_lok = root.filename

# main_lok = "E:\\Robocze\\model_testowy"
# root.filename = filedialog.askdirectory(initialdir="/", title="Wybierz folder do zapisu raportów")
# folder = root.filename

sim11_L, sim11res_d, res11_L = sim11_index_unite(main_lok)

for model in sim11_L:
    print("Model:")
    print(model)
    res11_lok = sim11res_d[model]
    # run_sim11(model, res11_lok)

    print("Wynik:")
    print(res11_lok)
    convert_res11(res11_lok)
    sleep(2)

sleep(3)
