import os


# funkcje mike index najlepiej sobie zwinac w pycharmie i przejsc na koniec skryptu


def sim11_index_unite(path):
    # puste listy i liczniki na pliki typu mike
    sim11_l = []
    res11_l = []
    sim11res_d = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".sim11"):
                print(file)
                # dodanie sciezki pliku do listy
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                sim11_l.append(element)
                # zaczytanie sciezki do pliku res11
                with open(element) as f:
                    lines = f.readlines()
                    index = lines.index("   [Results]\n")
                    sciezka = element.split("\\")
                    print(sciezka)
                    try:
                        hd_res = lines[index + 1].split("|")[1]
                        hd_res = hd_res.split("\\")
                        kropki = len(hd_res[0])
                        sciezka = sciezka[:-kropki]
                        hd_res = hd_res[1:]
                        sciezka = sciezka + hd_res
                    except:
                        hd_res = lines[index + 1].split("'")[1]
                        sciezka = sciezka[:-1]
                        print(sciezka)
                        hd_res = [hd_res]
                        print(hd_res)
                        sciezka = sciezka + hd_res
                        print(sciezka)

                    # sciezka = sciezka + hd_res
                    hd_res = "\\".join(sciezka)
                    sim11res_d[element] = hd_res
                    res11_l.append(hd_res)
                    print(sim11res_d)

    print(sim11_l)
    return sim11_l, sim11res_d, res11_l


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
