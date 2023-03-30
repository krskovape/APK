# Generalizace budov

Tato aplikace umožňuje vykreslit vybranou polygonovou vrstvu budov a tu následně generalizovat s využitím algoritmů Minimum Area Enclosing Rectange, 
Wall Average a Longest Edge.

### Spuštění aplikace

Pro správné fungování aplikace je zapotřebí mít v jedné složce umístěné soubory `mainform.py`, `draw.py`, `algorithms.py` a složku `icons` 
obsahující obrázky s ikonami. Pro zapnutí aplikace je poté zapotřebí spustit soubor `mainform.py`.

### Vstupní data

Aplikace vykresluje polygony načtené z vybraného souboru ve formátu `*shp`. Vstupní data musejí být v souřadnicovém systému S-JTSK, 
případně v jiném systému, který definuje souřadnice také v metrech.
