# WinGhost Monitor

![Logo](./atbswp/img/logo_chu.png)

**WinGhost Monitor** enregistre vos actions souris/clavier et les rejoue à
l'identique autant de fois que nécessaire. C'est un fork de
[atbswp](https://github.com/RMPR/atbswp) enrichi pour l'automatisation et le
**monitoring du temps de réponse** de scénarios applicatifs.

## Fonctionnalités

- **Gestion de scénarios (sessions)** — enregistrez plusieurs captures nommées
  et basculez de l'une à l'autre via une liste déroulante (Nouveau / Renommer /
  Supprimer). Le scénario actif est mémorisé entre les sessions.
- **Rejeu automatique (bouton « Auto »)** — rejoue le scénario actif à
  intervalle régulier, paramétrable (**30 minutes par défaut**).
- **Monitoring du temps de réponse** — un chrono démarre au début de chaque
  boucle et s'arrête à la fin du rejeu (retour de l'input validé). Le bouton
  **Rapport** affiche et exporte le détail :

  ```
  Scénario "X" ; 15 boucle(s) de 30 minutes (auto-play interval)

  Boucle 1 : de 09:00 à 09:30 -> 5 min
  Boucle 2 : de 09:30 à 10:00 -> 4.5 min
  ...
  Temps de réponse moyen : ...
  ```

- **Enregistrement progressif des sessions** — chaque boucle est écrite au fur
  et à mesure dans un fichier CSV (UTF-8, ouvrable dans Excel) sous
  `%APPDATA%\atbswp_reports`.
- **Bouton STOP** — arrête d'un coup l'enregistrement et le rejeu automatique
  (également via un **double appui sur Échap**).
- **Habillage CHU** — logo et palette de couleurs du projet
  [winghost-monitor](https://github.com/pronoiaque/winghost-monitor).

## Installation (Windows)

Téléchargez le fichier **`win-atbswp.exe`** depuis la page
[Releases](https://github.com/pronoiaque/win-atbswp/releases) et lancez-le —
aucune installation de Python n'est nécessaire. L'exécutable est un fichier
unique (monobloc), construit automatiquement sur un runner Windows
(voir `.github/workflows/build-windows.yml`).

## Utilisation

| Bouton | Rôle |
|--------|------|
| Charger | Charger une capture depuis le disque |
| Enregistrer | Sauvegarder la capture courante |
| ⏺ (rouge) | Démarrer / arrêter l'enregistrement |
| ⏹ STOP | Tout arrêter (ou double appui sur Échap) |
| ▶ (vert) | Rejouer le scénario |
| ⏱ Auto | Activer le rejeu automatique planifié |
| 📊 Rapport | Afficher / exporter le rapport de temps de réponse |
| ⚙ | Paramètres (intervalle, raccourcis, répétitions…) |

### Raccourcis clavier

- **F2–F12** : touches d'enregistrement / de lecture (configurables dans les
  Paramètres).
- **Échap × 2** (en moins d'une seconde) : tout arrêter.

## Où sont stockées mes données ?

- Scénarios : `%APPDATA%\atbswp_scenarios\<nom>.py`
- Rapports de monitoring : `%APPDATA%\atbswp_reports\<scénario>_<horodatage>.csv`
- Configuration : `%APPDATA%\atbswp.cfg`

## Crédits

- Projet d'origine : [atbswp](https://github.com/RMPR/atbswp) par Paul Mairo
  (GNU GPL v3).
- Logo et palette : [winghost-monitor](https://github.com/pronoiaque/winghost-monitor).
- Icônes : [Font Awesome Free](https://fontawesome.com) (CC BY 4.0).

## Licence

GNU General Public License v3 — voir [LICENSE](./LICENSE).
