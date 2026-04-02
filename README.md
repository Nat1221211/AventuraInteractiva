# AventuraInteractiva

Joc RPG amb combat segons prioritat (dona més importancia a la velocitat), els menus són menus amb moviment mitjançant w/s i enter per a enviar, enter per a seleccionar una opcio i q per a sortir, menicionant en cada menu quines opcions tensa, es a dir, si ports sortir amb q, o seleccionar amb enter...

Hi ha missions, zones, exits (logros / acheivements), multiples enitats, moviments, efectes d'estat (buffs / debuffs), exploracio amb probabilitat d etrobar objectes, rutes d'altres zones, ho activar / provocar / entrar en una missio de les acceptades.

Compte amb una opcio de guardat de partida, i carrega d'aquesta, però hi ha un sol slot de guardat.

El contiongut del joc és completament definit per els fitxers CSV i JSON, però esta limitat a les diferents opcions que es donen, mentre es segueixi una pauta similar-ment identica es pot afegir contingut al joc, però si hi ha alguna errada en els fitxers podria evocar en fallos del codi imprevisibles, desde un simple ara no faig dany fins a que el programa colapsi i digui, ha ocurrido un error.

S'ha de tenir en compte els noms dels fitxers en alguns casos al afegir contingut i sobretot els id de les diferents coses, com entitats, zones, missions, objectes, efectes d'estat, i altres detalls al crear contingut.

Finalment al afegir contingut recomano seguir creant clons dels diferents tipus de missions o zones, etc... i canviar petits detalls, com l'enemic, les recompenses i similar, afegir entitats és pot fer simplement seguint l'exemple dels ja creats que s'utilutzen en el joc, ja que els que no ho fan podrian no estar adaptats completament, asseguro que els 4 tipus de missio són funcionals aixì com les zones, botigues, entitats, objectes i altres detalls.
