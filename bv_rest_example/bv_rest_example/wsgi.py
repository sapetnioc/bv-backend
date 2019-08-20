'''This is the WSGI entry point for bv_auth
'''

from functools import partial
import os
import os.path as osp

from flask import Flask

import bv_rest
import bv_rest_example

def create_app(test_config=None):
    app_name = osp.basename(osp.dirname(__file__))
    
    
    # create and configure the app
    app = Flask(app_name, instance_path=osp.join(bv_rest.config.services_dir, app_name), instance_relative_config=True)

    api = bv_rest.RestAPI(app,
        title='API REST de fausses données scientifiques',
        description='''Cette API permet de récupérer quatre types de données : des sujets, des centres, des données et des visites. Chacun de ces types de donnée est accessible via une URL de l'API : (`/subjects`, `/centers`, `/data` et `/visit`). Ce site est généré automatiquement à partir d'une description de l'API et permet de parcourir les différentes URLs pour obtenir des informations sur les paramètres des requêtes (dans cette API, il n'y en a jamais) et la structure des résultats.

Description des données
-----------------------

 Il y a quatre types de données (Subject, Center, Visit et Data) dont la structure est décrite dans la partie schéma ci-dessous (c'est auto-généré, `Exception` est ajoutée automatiquement pour décrire la réponse en cas de bug dans le serveur, elle peut être ignorée). Un *sujet* est une personne dont on ne connaît que le code, l'année de naissance et le sexe. Certains de ces sujets sont venu passer des *visites* dans des *centres*. Pendant ces visites on a acquis des *données*. Dans les données, il y a n'importe quoi (2 nombres et 2 chaînes aléatoires). Chaque visite est faite à une date (champ `when`) et référence une donnée ainsi qu'un sujet et un centre. Ces éléments sont identifiés de manière unique par un champ `id` dont la valeur est utilisé dans la visite.


Objectif de l'exercice
----------------------

Créer un mini site web pour afficher les données fournies par cette API et le mettre dans un projet GitHub. Le site sera réduit à une utilisation locale, c'est-à-dire sous forme de fichiers HTML (et autres) à utiliser directement dans un navigateur. La façon de présenter les données et les possibilités de navigation sont laissées volontairement libres.  
        ''',
        version='1.0.0',
    )

    bv_rest.init_api(api)
    bv_rest_example.init_api(api)

    return app

application = create_app()


if __name__ == '__main__':
    application.run()
