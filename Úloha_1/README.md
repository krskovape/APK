# Geometrické vyhledávání bodu

Tato aplikace umožňuje vykreslit vybranou polygonovou vrstvu a kliknutím určit polohu bodu. Po spuštění analýzi dojde ke zvýraznění polygonu, 
v němž se polygon nachází. Pokud bod leží na hraně polygonů nebo v některém z jeho vrcholů, dojde ke zvýraznění všech polygonů, kterým daná hrana
nebo vrchol také náleží.

### Spuštění aplikace

Pro správné fungování aplikace je zapotřebí mít v jedné složce umístěné soubory `mainform.py`, `draw.py`, `algorithms.py` a složku `icons` 
obsahující pět obrázků s ikonami. Pro zapnutí aplikace je poté zapotřebí spustit soubor `mainform.py`.

### Vstupní data

Aplikace vykresluje polygony načtené z vybraného souboru ve formátu `*shp`. Vstupní data musejí být v souřadnicovém systému S-JTSK, 
případně v jiném systému, který definuje souřadnice také v metrech.

Ukázková vstupní data jsou polygony městských částí v Praze dostupné z portálu pražských [Opendat](https://www.geoportalpraha.cz/cs/data/otevrena-data/E9E20135-18B3-4163-B516-45613956B856).
