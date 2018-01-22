from subprocess import call


def run_m21(m21_lok, res_lok):
    # sim11_lok = "E:\Warianty_W0_na_21.12\Mala_panew_W0\M11\Q1%_DOD\mpn2.sim11"
    licznik = 0
    flag = 1
    size1 = 0
    size0 = 0

    cmd = "\"C:\\Program Files (x86)\\DHI\\2012\\bin\\MzLaunch.exe\" \"" + m21_lok + "\"" + " -y4 -x"
    print(cmd)
    p = call(cmd, shell=True)
    # tu nie dziala sprawdzanie wielkosci pliku, trzeba czyms zastąpic (data edycji)
    """
    while flag == 1 and licznik < 10:
        flag = 0
        p = Popen(cmd, shell=True)
        while p.poll() is None:
            print("idzie")
            time.sleep(120)
            if os.path.exists(res_lok) != True:
                print("nie ruszylo")
                p.kill()
                p.terminate()
                time.sleep(20)
                licznik +=1; flag = 1
            else:
                pass
            size0 = size1
            size1 = os.path.getsize(res_lok)
            print(size0, size1)
            if size1 == size0:
                print("stoi, zamykanie")
                try:
                    p.kill()
                    p.terminate()

                    time.sleep(20)
                    licznik += 1; flag = 1
                    size0 = 0; size1 = 0
                except OSError:
                    pass
            print(flag)
    """
    return p
