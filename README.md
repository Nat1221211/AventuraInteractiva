# AventuraInteractiva

Actualment 23/12/2025, al crear una entitat els moviements els fa en la clase i en el self.Moves però totes les entitats de tipus Entity els comparteixen per alguna rao un cop son generades.

Mateix dia, arreglat colocant en def init damunt de DefinirStats, que crida DefinirMoves, un self.Moves = list(), efectivament resetejant el valor ja contingut en aquest.
A veure per a errors que hagi provocat aixó.

Comprovat que els enemics no perden el moviments, per tant es pot deduir que era un problema acumulatiu, caad nova entitat generada en global (misions), afegia el seus moviments a les creades més tard.
