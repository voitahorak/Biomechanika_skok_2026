#zpracování dat skoku

import numpy as np
import pandas as pd #knihovna na tabulky
import matplotlib.pyplot as plt #knihovna na vykreslování grafů
#tato knihovna má snad pomoct s postupnou itegrací
from scipy.integrate import cumulative_trapezoid

data = pd.read_excel("AMTI/Proband_1_pokus1.mat.xlsx", header=None)

print(data.head())
print(data.shape)

fvz = 1000 #vzorkovací frekvence 1000Hz
#reakční síly
fz_leva = data.iloc[:, 2] # 3. sloupec
fz_prava = data.iloc[:, 7] # 7. sloupec
fz_celkem = fz_leva + fz_prava


## sekce s *většinou proměnných
#výpočet hmotnosti účastníka testování
#používám klidovou část měření, konktrétně prvních tisíc hodnot
fg = fz_celkem.iloc[:1000].mean() #toto je zatím jenom průměrná síla [N]
hmotnost = fg / 9.81 #výpočet hmotnosti z reakční síly a gravitační konstanty
#definice letové fáze
let = fz_celkem < 10 #síla menší než 10N je pro nás pomyslnou nulou
zacatek_letu = let[let].index[0] #zde ukládám letovou fázi do proměnné, také se jedná o první vzorek, který je pod 10N
konec_letu = let[let].index[-1] #konec letu...
#doba letu
doba_letu = (konec_letu - zacatek_letu)/fvz
#výška skoku z času letu -> h=(g*t^2)/8
vyska_skoku_casletu = (9.81 * doba_letu ** 2) / 8

#výška skoku z impulzu síly
#při klidném stoji bude výsledná síla NULOVÁ!!!
fz_vysledna = fz_celkem - fg #fz_vysledna je síla způsobující zrychlení těžiště účastníka testování
#víme, že stojící člověk má nulovou rychlost...
zrychleni = fz_vysledna / hmotnost #MÁME TU VÝPOČET ZRYCHLENÍ JOOOOOOOOOOOOO
rychlost = cumulative_trapezoid(zrychleni, dx=1/fvz, initial=0) #výpočet rychlosti snad...
rychlost_odrazu = rychlost[zacatek_letu - 1]
#vzorec pro výpočet z impulzu síly: h = v^2/2g
vyska_skoku_impulzsily = (rychlost_odrazu**2)/(2*9.81)


#vykreslování grafů pomocí importované knihovny
#tvorba časové osy
cas = np.arange(len(fz_celkem)) / 1000
plt.plot(cas, fz_celkem, label="Celková síla")
plt.plot(cas, fz_vysledna, label="Výsledná síla")
plt.xlabel("Čas [s]")
plt.ylabel("Síla [F]")
plt.title("Vertikální síly")
plt.legend() #když mám tohle, tak to použije to co je napsané za " , label="" "

#graf rychlosti
plt.figure()
plt.plot(cas, rychlost)
plt.xlabel("Čas [s]")
plt.ylabel("Rychlost [m/s]")
plt.title("Vertikální rychlost těžiště")


#plt.show()  #POKUD NECHCE OPERATOR PROGRAMU VIDET GRAF A ALT-TABOVAT, TAK TO NECHAT OKOMENTOVANE!!!

#rozdíl výšky skoků
rozdil_vysek = abs(vyska_skoku_casletu - vyska_skoku_impulzsily)

#tabulka rozdílů
tabulka = pd.DataFrame({
    "Metoda": ["Z doby letu", "Z impulzu síly", "Absolutní rozdíl"],
    "Výška [m]": [vyska_skoku_casletu, vyska_skoku_impulzsily, rozdil_vysek]
})

#průběžná kontrola výsledných hodnot

print(fz_celkem.head())
print(f"Hmotnost účastníka testování: {hmotnost:.2f} kg")
print(f"Letová fáze = {let.iloc[2200:2210]} s") #tohle printuje jenom od snímku 2200 po 2210
print(f"Kolik vzorků je pod 10N?= {let.sum()}") #zjišťuju kolik snímků je pod 10N
print(f"Řádky se vzorky pod 10N: {let[let].index}") #vzorky od 2153 do 2508 sjou pod 10N
print(f"Kontrola s prvními dvaceti položkami: {let[let].index[:20]}")
print(f"Začátek letu : {zacatek_letu}-tý vzorek")
print(f"Začátek letu : {konec_letu}-tý vzorek")
print(f"Doba letu: {doba_letu}s")
print(f"Výška skoku z času letu: {vyska_skoku_casletu:.3f} m")
print(f"Rychlost při odrazu: {rychlost[zacatek_letu - 1]:.3f} m/s")
print(f"Výška skoku z impulzu síly: {vyska_skoku_impulzsily:.3f} m")
print(f"Rozdíl výšek skoků: {rozdil_vysek:.3f} m")
print(f"Metody výpočtu {tabulka}")


#po tom co mi začal fungovat skript jsem začal dělat tohle, což má spočítat úplně všechno...
vysledky = []
#forcyklus co funguje na prvni pokus, spousta věcí se zde opakuje z předešlých řádků

for ucastnik in range(1, 10):
    for pokus in range(1, 4):
        nazev = f"AMTI/Proband_{ucastnik}_pokus{pokus}.mat.xlsx"
        data = pd.read_excel(nazev, header=None)

        #síla z plošin (osa z)
        fz_leva = data.iloc[:, 2]
        fz_prava = data.iloc[:, 7]
        fz_celkem = fz_leva + fz_prava

        fg = fz_celkem.iloc[:1000].mean()
        m = fg / 9.81

        #jak dlouha byla letova faze
        # jak dlouha byla letova faze
        let = fz_celkem < 10



        #prepocitavame impulz síly na rychlost
        fz_vysledna = fz_celkem - fg
        zrychleni = fz_vysledna / m
        rychlost = cumulative_trapezoid(zrychleni, dx=1 / 1000, initial=0)

        rychlost_odrazu = rychlost[zacatek_letu - 1]
        vyska_impulz = (rychlost_odrazu ** 2 / (2 * 9.81))*100

        #rozdíl výsledků metod
        rozdil_vysek = (abs(vyska_skoku - vyska_impulz))

        #ukládáme výsledky do slovníku, kterej funguje a bojím se na něj šahat
        vysledky.append({
            "Účastník": ucastnik,
            "Pokus": pokus,
            "Výška z letu [cm]": vyska_skoku,
            "Výška z impulzu [cm]": vyska_impulz,
            "Rozdíl [cm]": rozdil_vysek
        })

        print(nazev, data.shape)
        # print(vysledky)

#úžasná tabulka
tabulka = pd.DataFrame(vysledky)
print(tabulka.round(3))

from pathlib import Path

soubor = Path("vysledky_CMJ_vsichni_ucastnici_v6.xlsx")  #přidávám verzi .xlsx souboru

if soubor.exists():
    print("Soubor už existuje. Nebudu ho přepisovat!")
else:
    tabulka.to_excel(soubor, index=False)
    print("Nový Excel byl úspěšně vytvořen.")

