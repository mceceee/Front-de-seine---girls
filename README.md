# Front de Seine à trois

Petit outil perso pour organiser nos cours de sport à trois : dispos, envies, propositions de la semaine
(un cours Force, un Cardio, un Mobilité), places restantes, réservations et invitations.

## Fichiers

- `index.html` : la page complète, générée. C'est elle qu'on ouvre.
- `head.html` : styles et structure. `script.html` : toute la logique.
- `data/` : le planning des deux clubs et le catalogue des cours.
- `build.py` : assemble `head.html`, `script.html` et `data/` en `index.html` (`python3 build.py`).
- `smoke.js` : test rapide de la logique (`node smoke.js index.html`).
- `captures/` : quelques captures d'écran.

## Partage des données

Ouverte telle quelle (fichier ou GitHub Pages), la page garde les données sur l'appareil de chacune :
rien n'est partagé. Le partage en direct fonctionne dans la version publiée comme artifact claude.ai,
qui fournit la base commune. Pour un partage hors de claude.ai, il faut brancher une base en ligne.
