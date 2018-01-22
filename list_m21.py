import os


# funkcje mike index najlepiej sobie zwinac w pycharmie i przejsc na koniec skryptu


def m21_index_unite(path):
    # puste listy i liczniki na pliki typu mike
    m21_l = []
    res_dfs = []
    m21res_d = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".m21"):
                # print(file)
                # dodanie sciezki pliku do listy
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                m21_l.append(element)
                # zaczytanie sciezki do pliku res11
                with open(element) as f:
                    lines = f.readlines()
                    index = lines.index("         [OUTPUT_AREA_1]\n")
                    sciezka = element.split("\\")

                    try:
                        hd_res = lines[index + 11].split("|")[1]
                        hd_res = hd_res.split("\\")
                        kropki = len(hd_res[0])
                        sciezka = sciezka[:-kropki]
                        hd_res = hd_res[1:]
                        sciezka = sciezka + hd_res
                    except:
                        hd_res = lines[index + 11].split("'")[1]
                        sciezka = sciezka[:-1]

                        hd_res = [hd_res]

                        sciezka = sciezka + hd_res

                    hd_res = "\\".join(sciezka)
                    m21res_d[element] = hd_res
                    res_dfs.append(hd_res)

    return m21_l, m21res_d, res_dfs


def file_index(path, rozsz):
    # puste listy i liczniki na pliki typu mike
    lista = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("." + rozsz):
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                lista.append(element)

    return lista
