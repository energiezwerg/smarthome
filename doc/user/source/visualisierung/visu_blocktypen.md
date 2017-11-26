# Unterschiedliche Blocktypen

## Möglichkeiten

Die smartVISU unterstützt Blöcke zusätzlich zu den Standard-Blöcken auch Blöcke mit "2 Seiten", die in den bisherigen Releases von smarthome/smarthomeNG nicht unterstützt wurden.

Im aktuellen Release können auch diese Dual-Blöcke in der automatischen Seitengenerierung verwendet werden.

Hier ein Beispiel, wie ein solcher DualBlock aussehen kann:

![Dual-Block](assets/blocktype_dual_1.jpg)


![Dual-Block 2](assets/blocktype_dual_2.jpg)

Ein solcher Dual-Block hat immer die Größe eines großen Blocks. Damit die Visu-Seite "aufgeräumt" aussieht, sollte für den daneben liegenden Block die große Form gewählt werden (``sv_blocksize = 1``). Diehe dazu auch Seite [Unterschiedliche Blockgrößen](https://github.com/smarthomeNG/smarthome/wiki/visu_smartvisu_autogen_blocksizes).

Hier ist ein Beispiel auf einer Visu Seite:

![Navigation Trenner](assets/blocktype_dual_visu.jpg)

