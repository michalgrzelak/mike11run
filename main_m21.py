from list_m21 import m21_index_unite
from run_m21 import run_m21

main_lok = "C:\\Modele"

m21_L, m21res_d, res_dfs = m21_index_unite(main_lok)
print(len(m21_L))
print(len(res_dfs))

for model in m21_L:
    print("Model:")
    print(model)
    res_dfs = m21res_d[model]
    print("Wynik:")
    print(res_dfs)
    run_m21(model, res_dfs)
