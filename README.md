# Projet P10 - SoftDesk
## Sommaire
- Présentation
- Mise en place
- Routes
- Divers
- Swagger
- Flake8

### Présentation
**Application développée dans le cadre de la formation OpenClassrooms, développeur d'application Python.**
Cette application est une APIrest qui a pour but de remonter et suivre des problèmes techniques.
### Mise en place 
1. Cloner le git dans le repertoire souhaité git clone: `https://github.com/Gremy44/P10.git`
2. Rendez vous dans le repertoire P10: `cd P10`
3. Créer votre environnement virtuel: `python -m venv p10env`
4. Activer l'environnement virtuel: `p10env\Scripts\activate`
5. Installer les librairies grâce au fichier 'requirements.txt' avec la commande: `pip install -r requirements.txt`
6. Demarrer le serveur local avec la commande: `python manage.py runserver`
7. Ouvrez PostMan et consultez la documentation à cette URL pour retrouver chaque endpoints :
https://documenter.getpostman.com/view/22806081/2s935pq46w

### Routes
Si l'url est laissée de base elle sera accessible à cette adresse :
{url_base} = http://127.0.0.1:8000/

#### Endpoints
- **Administration**
`{url_base}/admin/`
- **Projects**
`{url_base}/projects/`
`{url_base}/projects/{pk}/`
- **Contributors**
`{url_base}/projects/{project_pk}/users/`
`{url_base}/projects/{project_pk}/users/{pk}/`
- **Issues**
`{url_base}/projects/{project_pk}/issues/`
`{url_base}/projects/{project_pk}/issues/{pk}/`
- **Comments**
`{url_base}/projects/{project_pk}/issues{issue_pk}/comments`
`{url_base}/projects/{project_pk}/issues{issue_pk}/comments/{pk}/`

### Divers
- Il faudra au préalable être connecté via le système de token pour pouvoir utiliser toutes les fonctionnalités présentes ici.
- Pour accéder à la page d'administration, il vous faudra être connecté sur un profil administrateur.
- Une base donnée .sqlite3 est mise à votre disposition pour pouvoir faire des tests

**Structure de la DB pour vos tests**

User1 : 
username => ``admin``
password => ``admin``

User2 : 
username => ``crazyfrog``
password => ``Crazifrog!123``

User3 : 
username => ``renelataupe``
password => ``Renelataupe!123``

Projet1 : author => User1 || Issue1 || Comment1
Contributor => User2

Projet2 : author => User3 || Issue2 || Comment2
Contributor => None

## Authentification
Pour pouvoir utiliser pleinement les fonctionnalités de l'api, vous devrez vous connecter via le systeme de token. pour obtenir un token ou le refresh, dans Postman rendez vous dans ``Auth/obtain tokens``. Entrez l'username et le password de l'utilisateur voulu et ajouter le token obtenue dans l'environnement global de Postman, vous pourrez ainsi effectuer les requetes qui demande une authentification.

## Swagger
Une interface swagger est disponible en vous rendant dans votre navigateur à l'adresse du serveur générée par Django. Par défaut, cette adresse est : `http://127.0.0.1:8000/`.
Vous arriverez ainsi sur une page swagger qui apporte des compléments sur les endpoints de l'api. Vous pouvez aussi faire des tests de requetes à aprtir de là, pour cela il faudra vous générer un token à partir de la requete POST : 'auth/token/'
Vous pourrez ensuite allé en haut de la page et cliquer sur `authorize`, pour entrer la valeur suivante dans le champ 'value' : `Bearer <votre token>`.

## Rapport Flake8
Un rapport des directives Flake8 est présent dans le dossier. Si vous souhaitez tester vous-même si les scripts suivent les directives pep8, vous pouvez générer votre propre rapport en utilisant cette ligne de code : `flake8 --format=html --htmldir=flake-report`