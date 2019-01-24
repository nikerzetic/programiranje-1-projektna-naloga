# Najbolje ocenjene fantazijske knjige na spletni strani Goodreads

Pri predmetu Programiranje 1 pripraviti projektno nalogo iz analize podatkov. Najprej sem s pomočjo programa v Pythonu s spletne strani [Goodreads](https://www.goodreads.com/shelf/show/fantasy) pobral podatke o najbolje ocenjenih fantazijskih knjigah (pri tem k fantazijskim knjiga prištevam dela, ki sledijo Tolkienovemu zgledu) na strani in jih uredil v .csv in .json datoteki s podatki o avtorju, letu izida, povprečni oceni, številu glasov, številu *shranitev na polico* in izdajami. Podatke sem nato obdelal v Jupyter-u s knjižnico Pandas za Python.

V mapi *edited_data*, so shranjene sledeče datoteke, z urejenimi podatki:
- *authors.csv*: imena avtorjev in njihove knjige
- *books.csv*: naslov, število *shranitev na polico*, povprečna ocena, število ocen in leto izida
- *books.json*: vsi zajeti podatki shranjeni v .json format
- *series.csv*: serije knjig, naslovi posameznih del in zaporedna številka njige v seriji

Prenešenih spletnih strani nisem nalagal, sem pa dodal datoteko *main_python_file.py*, s katero sem podatke pobral s spleta.

## Navodila za uporabo

Program v datoteki *main_python_file.py* je prilagojen za spletno stran Goodreads, natančneje za seznam, s katerega sem pobiral podatke - iz tega razloda močno, davomim, da bi program bil uporaben za katerokoli drugo stran, celo znotraj mesta Goodreads. 

Spletne strani poberemo s pomočjo datoteke *main_python_file*. Na začetku podamo naslov strani za prijavo - *sign_in_page*, uporabnikovo spletno pošto - *user_email* - in geslo - *user_password* (v kodi sta že zapisana uporabniško ime in geslo računa, ki sem ga ustvaril s tem namenom) ter naslov prve strani - *frontpage_url*. Poimenujemo datoteki za shranjevanje strani in urejenih podatkov - *downloaded_sites_directory* in *edited_data_directory*, ter podamo regularni  izraz - *user_regex*.

Program uporablja razred *Browser* iz knjižnice *Splinter*, ker narava spletne strani Goodreads neprijavljenemu uporabniku dovoljuje dostop le do prve strani. V repozitoriju je priložena tudi apllikacija *geckodriver.exe*, ki Pythonu omogoča delovanje v brskalniku *Firefox*. 
