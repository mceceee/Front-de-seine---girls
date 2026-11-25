# Front de Seine à trois

Petit outil perso pour organiser nos cours de sport à trois : dispos, envies, propositions de la semaine
(un cours Force, un Cardio, un Mobilité), places restantes, réservations et invitations.

## Fichiers

- `index.html` : le site complet, généré. C'est lui que Vercel sert.
- `artifact.html` : la même page au format attendu par claude.ai.
- `head.html` : styles et structure. `script.html` : toute la logique.
- `data/` : le planning des deux clubs et le catalogue des cours.
- `build.py` : assemble le tout (`python3 build.py`).
- `firestore.rules` : les règles de sécurité à coller dans Firebase.
- `smoke.js` : test rapide de la logique (`node smoke.js artifact.html`).

## Partage des données

- Dans claude.ai, la page utilise la base de l'artifact.
- Sur Vercel, elle utilise Firebase si le fichier `firebase-config.json` est présent à la racine
  (le bloc `firebaseConfig` du projet, au format JSON), puis `python3 build.py`.
  Les données d'un groupe sont rangées sous un code secret contenu dans le lien (`?g=…`) :
  il faut ce lien pour lire ou modifier le planning. Menu « ⋯ » → « Copier le lien pour Coco et Clem ».
- Sans ce fichier, la page garde les données sur l'appareil de chacune.
