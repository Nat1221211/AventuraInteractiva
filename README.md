# AventuraInteractiva
Joc Interactiu d'Interficie Grafica, amb combat, exploracio de zones per linies de text, missions, objectes utilitzables en combat (curacio), entre d'altres.

El joc es façilment ampliable en termes de contingut afegint imatges en assets entities, respectant el terme:
cada entitat id_sprite, dins la cual una imatge front i una back, en format .png.

Afegir entitats, moviments, zones, missions, utilitzant les d'exemple ja existents.

Les imatges de fons, poden ser de tipus combat (Battleground), o de Scene (GUIs), en aquestes, han de portar el noms amb el seguent format:
Scenes:
  - per zona: ZoneType_scene.png
  -  per id: id_scene.png

les de combat igualment, pero de moment només per zonetype_Battleground.png

Per a revisar la carrega d'imatges mirar el fitxer PreparariCridar, en els apartats, d'Entitats i Zones...

No afegir sense comprobar el funcionament dels sistemes anteriorment, o fer a base de prova i error degut a falta d'informació...
