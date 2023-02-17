# Extracteur d'informations à partir de journaux du XIXe siècle

## Résumé

Scripts Python permettant d'extraire des noms propres d'un corpus d'image. Les programmes ont été réalisés par Siepka Aurélien et Vallée Mathieu.

Le premier script sert à télécharger des numéros de journaux ou des images appartenant à la BnF sur Gallica.

Le second permet de traiter toutes les images téléchargées.

Le troisième permet de récupérer les noms propres sur les textes des images.

Le dernier permet de créer un graph qui relie tous les noms qui apparaissent dans le même paragraphe.

## Installation

### Tesseract

Tesseract pour l'océrisation des images.

Sur Windows (il faut bien penser à installer la langue "French" et mettre Tesseract dans le ClassPath à l’installation) : \
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev-205-ge205c59.exe

Sur Linux :
```
sudo apt install tesseract-ocr
sudo apt-get install tesseract-ocr-fra
```

### Modules

Toutes les librairies utilisées.

```
pip install pytesseract
pip install Pillow
pip install scipy
pip install opencv-python
pip install torch torchvision torchaudio
pip install tensorflow --user
pip install transformers
pip install transformers[sentencepiece]
pip install autocorrect
pip install networkx
pip install matplotlib
```

### Modèle camembert-ner

Le modèle servant à la détection des noms propres créée et entrainé par par Jean-Baptiste Polle sur Hugging Face.

```
git lfs install
git clone https://huggingface.co/Jean-Baptiste/camembert-ner
```

## Lancement

Le programme a été divisé en quatre fichier pour éviter que le tout prenne trop de temps. Voici la particularité de chacun de ces fichiers :

### I - Recuperation des journaux.py

Ce script télécharge toutes les images souhaitées dans un dossier 'images'. Les données d'entrée doivent être stockées dans le fichier 'datas/journaux.json' sous un format JSON.

Voici un exemple :
```
{
    "L'Univers" : {
        "url" : "https://gallica.bnf.fr/ark:/12148/cb34520232c/date",
        "title": "L'Univers",
        "year": 1867,
        "month": 10,
        "day": 24,
        "item": 1,
        "rate": 1,
        "firstpage": 1,
        "lastpage": 12,
        "resolution": "full"
    }
}
```

Explication des paramètres :

— url : Pour récupérer les images d’une série de numéros de périodiques, on part de l’adresse du périodique avec
les dates.

— title : on choisit un titre qui sera indiqué dans le nom du fichier.

— year, month, day : la date du premier numéro que l’on souhaite télécharger.

— item : le nombre de numéros que l’on veut récupérer. Par exemple pour avoir toute une année on peut mettre 365.

— rate : le nombre de jours entre chaque numéro – cela fonctionne bien pour les quotidiens (on indique 1), les
hebdomadaires (on indique 7) ; en cas de problème, on peut inscrire 1 et préciser dans “item” le nombre total
de jours dans la période qu’on veut télécharger (par exemple, pour un an on inscrira 365), cela permettra
d’être certain de télécharger tous les numéros, même si cela produit des erreurs (les dates sans numéros).

— firstpage et lastpage : la première et la dernière page de chaque numéro qu’on veut télécharger ; ceci peut
permettre par exemple de ne télécharger que les unes. Pour être certain de télécharger toutes les pages d’un
périodique, il faut ici tenir compte de la pagination ; on peut gonfler le nombre de pages au cas ou certains
documents comportent plus de pages, les erreurs s’afficheront dans le shell avant que le programme ne continue
avec le numéro suivant du périodique. Par exemple, pour un journal de 8 pages, il vaut mieux indiquer 12
pages pour être certain que des numéros plus longs seront entièrement téléchargés.

— resolution : changer la résolution des images obtenues pour avoir une plus ou moins bonne qualité. Cela peut
être un nombre comme 3000 ou 5000, pour avoir la qualité maximale nous pouvons mettre ’full’ au lieu d’un
nombre.

### II - Traitement des images.py

Ce script a pour effet de traiter toutes les images qui sont dans le dossier 'images'.

### III - Recuperation des noms propres.py

Récupère les noms propres grâce au model camembert-ner. Utilise Tesseract pour océriser les images du fichier 'images'. Le résultat est stocké dans 'result/noms.json' sous la forme d'un fichier JSON.

### IV - Creation de graphe.py

Crée un graphe en fonction du résultat du programme III. Le graphe est sauvegardé dans le dossier 'result', et affiché quand le script est lancé.

Ces quatre scripts sont à exécuter les uns à la suite des autres car ils se suivent. Il est tout à fait possible de tous les réunir en un fichier.
