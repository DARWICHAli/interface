# Interface

## Idées

* Créer une interface Web sur laquelle on peut upload des images et qui formatte la réponse du modèle.

* Les calculs doivent être fait sur le client.

* L'interface doit être découplée du modèle.

* L'interface doit être deployable via un conteneur Docker.

* HTTPS


## Proposition d'itérations

1. Interface "upload + affichage texte" sans Docker.  
 	-> nécessite de prendre en main les outils.

2. Interface précédente dans un conteneur Docker.  
	-> .gitlab-ci.yml adapté.  
	-> familiarisation avec Docker.  

3. Mise à jour automatique sur le serveur.
	-> Scripting

4. _Incrémentations successives..._

_..._
