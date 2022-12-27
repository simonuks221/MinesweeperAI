# MinesweeperAI

Simono Riaukos ir Arno Piauloko modulio "Dirbtinis intelektas" galutinis projektas.

Trejuose folderiuose yra laikomi atitinkami failai skirtingiems modeliams.
*FullBoard - modelis priimantis visą lentą kaip įėjimą
*Kaimynai - modelis priimantis tik kaimynus kaip įėjimą
*SuConv2D - visos lentos modelis su konvoliucija

Visuose folderiuose bus keturi .py failai:
*DatasetGenerator - sugeneruoti atitinkamą datasetą tam modeliui
*ModelTrainer - treniruoti modeli
*ModelTester - ištestuoti modeli, sugneruoti grafikus arba sužaisti vieną žaidimą
*minesweeperGameLogic - vienodas failas visiems atsakingas už pačio žaidimo logiką, lentos saugojimą, jos generavimą.

Datasetai nėra pridėti dėl per didelio jų dydžio (naudoti nuo 0.6GB iki 3GB dydžio)
Modeliai turėtų būti pridėti visur.

-----------------------------------------------------------------------------------------------------------------------
# Išbandyti patiems

Išsirenkate aplankalą, atidarote atitinkamą modelTester.py failą, apačioje yra generateGraph kintamasis. True - sugeneruos graphAmount kiekį žaidimų ir jų atitinkamus laimėjimo bei ėjimų grafikus, False - sužais vieną "Minesweeper" žaidimą.
