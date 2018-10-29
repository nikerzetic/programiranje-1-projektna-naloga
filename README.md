# Najbolje ocenjene fantazijske knjige na spletni strani Goodreads

Pri predmetu Programiranje 1 pripraviti projektno nalogo iz analize podatkov. Najprej bom s pomočjo programa v Python s spletne strani [Goodreads](https://www.goodreads.com/shelf/show/fantasy) pobral podatke o najbolje ocenjenih fantazijskih knjigah (pri tem k fantazijskim knjiga prištevam dela, ki sledijo Tolkienovemu zgledu) na strani in jih uredil v .csv in .json datoteki s podatki o avtorju, letu izida, povprečni oceni, številu glasov, številu *shranitev na polico* in izdajami. 

V mapi *edited_data*, so shranjene sledeče datoteke, z urejenimi podatki:
- *authors.csv*: imena avtorjev in njihove knjige
- *books.csv*: naslov, število *shranitev na polico*, povprečna ocena, število ocen in leto izida
- *books.json*: vsi zajeti podatki shranjeni v .json format
- *series.csv*: serije knjig, naslovi posameznih del in zaporedna številka njige v seriji

Prenešenih spletnih strani nisem nalagal, sem pa dodal datoteko *main_python_file.py*, s katero sem podatke pobral s spleta.

Delovne hipoteze:
- Ali se povprečna ocena in število *shranitev na polico* skladata?
- Knjige iz katere serije so najbolje ocenjene?
- Knjige katerega avtorja so najbolje ocenjene?
- Povprečne ocene knjig po desetletjih izida.
- Povezava med številom glasov in povprečno oceno.
- Povezava med številom glasov in številom shranitev
