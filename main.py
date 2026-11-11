#zpracování dat skoku

import numpy as np
import pandas as pd #knihovna na tabulky

import matplotlib.pyplot as plt #knihovna na vykreslování grafů

data = pd.read_excel("AMTI/Proband_1_pokus1.mat.xlsx", header=None)

print(data.head())
print(data.shape)

#reakční síly
fz_leva = data.iloc[:, 2] # 3. sloupec
fz_prava = data.iloc[:, 7] # 7. sloupec
fz_celkem = fz_leva + fz_prava

#výpočet hmotnosti účastníka testování
#používám klidovou část měření, konktrétně prvních tisíc hodnot
fg = fz_celkem.iloc[:1000].mean() #toto je zatím jenom průměrná síla [N]
m = fg/9.81 #výpočet hmotnosti z reakční síly a gravitační konstanty

#vykreslování grafů pomocí importované knihovny
#tvorba časové osy
cas = np.arange(len(fz_celkem)) / 1000
plt.plot(cas, fz_celkem)
plt.xlabel("Čas [s]")
plt.ylabel("Síla [F]")
#plt.show()  #POKUD NECHCE OPERATOR PROGRAMU VIDET GRAF A ALTTABOVAT, TAK TO NECHAT OKOMENTOVANE!!!

#definice letové fáze
let = fz_celkem < 10 #síla menší než 10N je pro nás pomyslnou nulou

#průběžná kontrola výsledných hodnot

print(fz_celkem.head())
print(f"Hmotnost účastníka testování: {m:.2f} kg")
print(f"Letová fáze = {let.iloc[2200:2210]} s") #tohle printuje jenom od snímku 2200 po 2210
print(f"Kolik vzorků je pod 10N?= {let.sum()}") #zjišťuju kolik snímků je pod 10N
print(f"Řádky se vzorky pod 10N: {let[let].index}") #vzorky od 2153 do 2508 sjou pod 10N
print(f"kontrola s prvními dvaceti položkami: {print(let[let].index[:20])}")