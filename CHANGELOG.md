# Journal des modifications

Toutes les évolutions notables de **WinGhost Monitor** sont consignées ici.
Le projet est un fork de [atbswp](https://github.com/RMPR/atbswp).

## [0.4.2]

### Ajouté
- **Bouton STOP** pour tout arrêter d'un coup (enregistrement + rejeu
  automatique + rejeu en cours), également déclenchable par un **double appui
  sur Échap** (en moins d'une seconde).
- **Enregistrement progressif des sessions** : chaque boucle de monitoring est
  écrite au fur et à mesure dans un fichier CSV (UTF-8) sous
  `%APPDATA%\atbswp_reports`.

### Modifié
- **Interface et documentation en français par défaut** (application, README,
  changelog).
- Suppression des informations d'installation/utilisation sous Linux
  (projet ciblant Windows).

### Corrigé
- **Caractères accentués** dans les traductions (notamment le menu Paramètres) :
  les fichiers de langue sont désormais lus en UTF-8.

## [0.4.1]

### Ajouté
- **Monitoring du temps de réponse d'un scénario** : un chrono mesure chaque
  boucle de rejeu automatique de bout en bout ; bouton **Rapport** (affichage
  et export `.txt`).

### Modifié
- Boutons **« Auto »** et **« Rapport »** transformés en boutons-icônes au même
  design que les boutons historiques.
- Contrôles de scénario traduits en français (Nouveau / Renommer / Supprimer…).
- Nouveau nom de produit professionnel : **WinGhost Monitor**.

### Supprimé
- Boutons « Transformer en exécutable » et « Aide ».

## [0.3.1]

### Ajouté
- **Gestion de scénarios (sessions)** : captures nommées, sélection,
  création / renommage / suppression.
- **Rejeu automatique (« Auto »)** à intervalle configurable (30 min par
  défaut).
- Habillage **CHU** (logo et palette) inspiré de winghost-monitor.
- Construction d'un exécutable Windows **monobloc** via GitHub Actions,
  publié dans les Releases.
