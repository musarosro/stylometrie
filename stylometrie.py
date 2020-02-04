#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A script for a stylometric evaluation of a Classical or Mediaeval Chinese text.
"""

import io
import sys

# datové proměnné
datavcelku = ''
data_bezsyntaxe = ''
data = []
datarazena = []
typy = ()
whitespace = ' \n\t\v\f，、。；？」「！：』『,.;:?!'
frekvence = {}
frekvence_slovnich_druhu = {}

# proměnné slovních druhů TOKEN
substantiva = 0
propria = 0
slovesa = 0
adjektiva = 0
adverbia = 0
cislovky = 0
numerativy = 0
zajmena = 0
predlozky = 0
spojky = 0
castice = 0
citoslovce = 0
stavovaslova = 0
modalnislovesa = 0
modalniadjektiva = 0
splynutinyYAN = 0
splynutinyWU = 0
splynutinyZHU = 0
splynutinyHE = 0
plnovyznamova = 0
gramaticka = 0
splynutiny = 0
injunktiva = 0
g_casticeYE = 0
g_casticeYI = 0
g_spojkaER = 0
g_zajmenoSUO = 0
g_zajmenoZHE = 0
g_citatorYUE = 0

# proměnné syntaktických funkcí
podmet = 0
prisudek_hlav = 0
prisudek_zav_impl = 0
prisudek_zav_expl = 0
privlastek = 0
prisl_urceno = 0
komplement = 0
konexak = 0
postmodifikator = 0
modalni_prvek = 0

# proměnné k celkové statistice
pocet_token = 0
pocet_type = 0
jednoslabicna = 0
viceslabicna = 0
viceslabicna_lemmata = 0

###############################################################################

def vypocet_frekvence():
# výpočet frekvence jednotlivých slov (resp. jedinečných kombinací znak+slovní druh),
# výsledek tvaru {'也[p' : 125, ...}
    def MyFunc(e):
        return e[1]
    iterator = 0
    frekv_seznam = []
    for lemma in data_bezsyntaxe:
        if not(data_bezsyntaxe[iterator] in frekv_seznam):
            frekv_seznam = frekv_seznam.append([lemma, data.count(lemma[-2:])])
            iterator += 1
        else:
            pass
    frekv_seznam.sort(key=MyFunc)
    frekvence = dict(frekv_seznam)

def vypocet_sldruhu_type():
# výpočet výskytu slovních druhů a polysyllab ve slovníku,
# výsledek tvaru {'a' : 859, ...}
    seznamdruhu = 'ngzvadsqmrcpihjefbkx'
    frekv_seznam = [[c, 0] for c in seznamdruhu]
    frekvence_slovnich_druhu = dict(frekv_seznam)
    for lemma1 in typy:
        frekvence_slovnich_druhu[lemma1[-1]] += 1
    for lemma2 in typy_delene:
        if len(lemma2[0]) > 1: viceslabicna_lemmata += 1

def prcTO(cislo): # vrací řetězec: procentuální zastoupení TOKEN
    procento = str(cislo/pocet_token*100) + ' %'
    return procento

def prcTY(cislo): # vrací řetězec: procentuální zastoupení TYPE
    procento = str(cislo/pocet_type*100 + ' %'
    return procento

##############################################################################

jmeno_souboru = input('Zadejte jméno souboru včetně cesty: ')
print('Načítání dat.')

# čtení ze souboru
with open(jmeno_souboru) as soubor:
    nactena_data = soubor.read()
    datavcelku = str(nactena_data.strip(whitespace))
    soubor.close()

data = datavcelku.split(']') # rozkouskování na ['也[p+(x)', '也[p+x', ...]
for vyrez in data: # doplnění chybějících syntaktických značek na výplňkové 'x'
    if '+' not in vyrez: vyrez += '+x'
for vyrez in data: # vytvoření dat bez syntaktických značek
    data_bezsyntaxe.append(vyrez[:-2])
typy = set(data_bezsyntaxe) # lemmatizace, výsledný tvar: ('也[p', atd.)
typy_delene = (v.split('[', 1) for v in typy] # rozkouskování lemmat, výsledný tvar (['也', p], ['也', p], ...)
data_razena = [v.split('[', 1) for v in data] # rozkouskování na [[也, p+x], [也, p+x], ...]
data_def = tuple(data_razena) # zamražení dat v N-ticích
pocet_token = len(data_def) # délka souboru ve znacích
pocet_type = len(typy) # rozsah slovníku

print ('Data načtena.')
print ('Vyhodnocování slovních druhů.')

# vyhodnocení slovních druhů TOKEN
pozice = 0
for polozka in data_def:
    slovni_druh = polozka[1][0]
    pozice += 1
    if slovni_druh == 'n':
        substantiva += 1
        plnovyznamova += 1
    elif slovni_druh == 'a':
        adjektiva += 1
        plnovyznamova += 1
    elif slovni_druh == 'v':
        slovesa += 1
        plnovyznamova += 1
    elif slovni_druh == 'd':
        adverbia += 1
        gramaticka += 1
    elif slovni_druh == 'q':
        cislovky += 1
        plnovyznamova += 1
    elif slovni_druh == 'm':
        numerativy += 1
        gramaticka += 1
    elif slovni_druh == 'r':
        predlozky += 1
        gramaticka += 1
    elif slovni_druh == 'c':
        spojky += 1
        gramaticka += 1
    elif slovni_druh == 'p':
        castice += 1
        gramaticka += 1
    elif slovni_druh == 'i':
        citoslovce += 1
    elif slovni_druh == 'z':
        zajmena += 1
        gramaticka += 1
    elif slovni_druh == 's':
        stavovaslova += 1
        plnovyznamova += 1
    elif slovni_druh == 'h':
        modalnislovesa += 1
        plnovyznamova += 1
    elif slovni_druh == 'j':
        modalniadjektiva += 1
        plnovyznamova += 1
    elif slovni_druh == 'e':
        splynutinyYAN += 1
        predlozky += 1
        zajmena += 1
        gramaticka += 1
    elif slovni_druh == 'f':
        splynutinyWU += 1
        adverbia += 1
        zajmena += 1
        gramaticka += 1
    elif slovni_druh == 'b':
        splynutinyZHU
        predlozky += 1
        zajmena += 1
        gramaticka += 1
    elif slovni_druh == 'k':
        splynutinyHE += 1
        zajmena += 1
        adverbia += 1
        gramaticka += 1
    elif slovni_druh == 'g':
        propria += 1
        plnovyznamova += 1
    else print("Chybná hodnota na pozici ", pozice, '!')

vypocet_sldruhu_type()	#  výpočet zastoupení slovních druhů ve slovníku

print ('Slovní druhy vyhodnoceny.')
print ('Vyhodnocování syntaktických funkcí.')

# vyhodnocení syntaktických funkcí TOKEN
pozice = 0
for polozka in data_def:
    syntax = polozka[1][-1]
    pozice += 1
    if syntax == 's':
        podmet += 1
    elif syntax == 'p':
        prisudek_hlav += 1
    elif syntax == 'q':
        prisudek_zav_impl += 1
    elif syntax == 'r':
        prisudek_zav_expl += 1
    elif syntax == 'a':
        privlastek += 1
    elif syntax == 'd':
        prisl_urceni += 1
    elif syntax == 'c':
        komplement += 1
    elif syntax == 'k':
        konexak += 1
    elif syntax == 'm'
        postmodifikator += 1
    elif syntax == 'h'
        modalni_prvek += 1
    else print("Chybná hodnota na pozici", pozice, '!')

print ('Syntaktické funkce vyhodnoceny.')
print ('Vyhodnocování diagnostických znaků.')
pozice = 0

for polozka in data_def: # výpočet frekvence diagnostických slov
    pozice += 1
    znak = polozka[0]
    druh = polozka[1]
    if len(znak) > 1:
        viceslabicna += 1
    else:
        jednoslabicna += 1
    if znak = '也':
        g_casticeYE += 1
    elif znak == '矣':
        g_casticeYI += 1
    elif znak == '而':
        g_spojkaER += 1
    elif znak == '所' and druh = 'z':
        g_zajmenoSUO += 1
    elif znak == '者' and druh = 'z':
        g_zajmenoZHE += 1
    elif znak == '曰':
        g_citatorYUE += 1
    elif druh == 'k' or 'e'or 'f' or 'b':
        splynutiny += 1
    elif (znak == '無' or '毋' or '勿') and (druh == 'd' or 'f')
        injunktiva += 1

print('Diagnostické znaky vyhodnoceny.')
print('Výpočet frekvencí.')
vypocet_frekvence()
print('Frekvence vypočteny.')

# tisk stylometrických parameterů
print('Celkové/smíšené charakteristiky:\n')

print ('Poměr type/token:\n', pocet_type/pocet_token)
print('Tokenové charakteristiky (celkový počet tokenů: '+ pocet_token + '):')
print('Vlastní jména:', prcTO(propria))
print('Víceslabičné lexikum:', prcTO(viceslabicna))
print('Gramatická slova:', prcTO(gramaticka))
print('Splynutiny:', prcTO(splynutiny))
print('Částice:', prcTO(castice))
print('Spojky:', prcTO(spojky))
print('Injunktivní záporky:', prcTO(injunktiva))
print('Zájmena:', prcTO(zajmena))
print('Poměr YE a YI:', g_casticeYE/g_casticeYI)
print('Zastoupení ER:', prcTO(g_spojkaER))
print('Zastoupení ZHE:', prcTO(g_zajmenoZHE), 'a SUO: ', prcTO(g_zajmenoSUO))
print('Zastoupení YUE:', prcTO(g_citatorYUE))
print('Index adverbiální modifikace - token:', prcTO(adverbia))

print('Typové charakteristiky (celkový počet typů:', pocet_type + '):'))
print('Víceslabičná lemmata:', prcTY(viceslabicna_lemmata))

print('Ukládání výsledků do souborů.')

with open('vystupy_stylometrie1.txt') as vystup_soubor: # zápis do souboru
    vystup_soubor.write('Celkové/smíšené charakteristiky:\n\n')
    vystup_soubor.write('Poměr type/token: ' + str(pocet_type/pocet_token)+'\n\n')
    vystup_soubor.write('Tokenové charakteristiky (celkový počet tokenů: '+ str(pocet_token) + '):\n')
    vystup_soubor.write('Vlastní jména: ' + prcTO(propria) + '\n')
    vystup_soubor.write('Víceslabičné lexikum TOKEN: ' + prcTO(viceslabicna) + '\n')
    vystup_soubor.write('Víceslabičná lemmata TYPE: ' + prcTY(viceslabicna_lemmata) + '\n')
    vystup_soubor.write('Gramatická slova: ' + prcTO(gramaticka) + '\n')
    vystup_soubor.write('Splynutiny: ' + prcTO(splynutiny) + '\n')
    vystup_soubor.write('Částice: ' + prcTO(castice) + '\n')
    vystup_soubor.write('Spojky: ' + prcTO(spojky) + '\n')
    vystup_soubor.write('Injunktivní záporky: ' + prcTO(injunktiva) + '\n')
    vystup_soubor.write('Zájmena: ' + prcTO(zajmena) + '\n')
    vystup_soubor.write('Poměr YE a YI: ' + str(g_casticeYE/g_casticeYI) + '\n')
    vystup_soubor.write('Zastoupení ER: ', prcTO(g_spojkaER+ \’n’))
    vystup_soubor.write('Zastoupení ZHE: ' + prcTO(g_zajmenoZHE) + 'a SUO: ' + prcTO(g_zajmenoSUO) + '\n')
    vystup_soubor.write('Zastoupení YUE: ' + prcTO(g_citatorYUE) + '\n')
    vystup_soubor.write('Index adverbiální modifikace - token: ' + prcTO(adverbia) + '\n')
    vystup_soubor.close()

with open('vystupy_stylometrie2.txt') as vystup_soubor2: # zápis frekvenčních statistik slovních druhů do jiného souboru
    vystup_soubor2.write('\nFrekvenční statistika slovních druhů (TOKEN):\n')
    vystup_soubor2.write('Podstatná jména: ' + prcTO(substantiva) + '\n')	
    vystup_soubor2.write('Vlastní jména: ' + prcTO(propria) + '\n')
    vystup_soubor2.write('Slovesa: ' + prcTO(slovesa) + '\n')
    vystup_soubor2.write('Modální slovesa: ' + prcTO(modalnislovesa) + '\n')	
    vystup_soubor2.write('Adjektiva: ' + prcTO(adjektiva) + '\n')
    vystup_soubor2.write('Modální adjektiva: ' + prcTO(modalniadjektiva) + '\n')
    vystup_soubor2.write('Příslovce: ' + prcTO(adverbia) + '\n')
    vystup_soubor2.write('Stavová slova: ' + prcTO(stavovaslova) + '\n')
    vystup_soubor2.write('Číslovky : ' + prcTO(cislovky) + '\n')
    vystup_soubor2.write('Numerativy: ' + prcTO(numerativy) + '\n')
    vystup_soubor2.write('Zájmena: ' + prcTO(zajmena) + '\n')
    vystup_soubor2.write('Předložky: ' + prcTO(predlozky) + '\n')	
    vystup_soubor2.write('Spojky: ' + prcTO(spojky) + '\n')
    vystup_soubor2.write('Částice: ' + prcTO(castice) + '\n')
    vystup_soubor2.write('Citoslovce: ' + prcTO(citoslovce) + '\n')
    vystup_soubor2.write('Gramatická slova: ' + prcTO(gramaticka) + '\n')
    vystup_soubor2.write('Splynutiny: ' + prcTO(splynutiny) + '\n')
    vystup_soubor2.write('Injunktivní záporky: ' + prcTO(injunktiva) + '\n')
   	vystup_soubor2.write('\nStatistika zastoupení slovních druhů ve slovníku (TYPE):\n')
    vystup_soubor2.write('Podstatná jména: ' + prcTY(frekvence_slovnich_druhu['n']) + '\n')	
    vystup_soubor2.write('Vlastní jména: ' + prcTY(frekvence_slovnich_druhu['g']) + '\n')
    vystup_soubor2.write('Slovesa: ' + prcTY(frekvence_slovnich_druhu['v']) + '\n')
    vystup_soubor2.write('Modální slovesa: ' + prcTY(frekvence_slovnich_druhu['h']) + '\n')	
    vystup_soubor2.write('Adjektiva: ' + prcTY(frekvence_slovnich_druhu['a']) + '\n')
    vystup_soubor2.write('Modální adjektiva: ' + prcTY(frekvence_slovnich_druhu['j']) + '\n')
    vystup_soubor2.write('Příslovce: ' + prcTY(frekvence_slovnich_druhu['d']) + '\n')
    vystup_soubor2.write('Stavová slova: ' + prcTY(frekvence_slovnich_druhu['s']) + '\n')
    vystup_soubor2.write('Číslovky : ' + prcTY(frekvence_slovnich_druhu['q']) + '\n')
    vystup_soubor2.write('Numerativy: ' + prcTY(frekvence_slovnich_druhu['m']) + '\n')
    vystup_soubor2.write('Zájmena: ' + prcTY(frekvence_slovnich_druhu['z']) + '\n')
    vystup_soubor2.write('Předložky: ' + prcTY(frekvence_slovnich_druhu['r']) + '\n')	
    vystup_soubor2.write('Spojky: ' + prcTY(frekvence_slovnich_druhu['c']) + '\n')
    vystup_soubor2.write('Částice: ' + prcTY(frekvence_slovnich_druhu['p']) + '\n')
    vystup_soubor2.write('Citoslovce: ' + prcTY(frekvence_slovnich_druhu['i']) + '\n')
    vystup_soubor2.write('Víceslabičná lemmata TYPE: ' + prcTY(viceslabicna_lemmata) + '\n')
    vystup_soubor2.close()

with open ('vystupy_stylometrie3.txt') as vystup_soubor3: # zápis Zipfovského přehledu do souboru
    iterator = 0
    for radka_vystupu1, radka_vystupu2 in frekvence.items():
        iterator += 1
        vystup_soubor2.write(str(iterator) + '\t' + radka_vystupu1 + str(radka_vystupu2) + '\n')
    vystup_soubor3.close()

print('Výsledky uloženy.')
print('Stylometrická statistika úspěšně ukončena.')
input('Chcete-li ukončit program, zmáčkněte ENTER.')#!/usr/bin/env python
