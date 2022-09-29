Pour lancer le programme:

source bin/activate
pip install -r requirements.txt
python3 startup.py

tester le programme sur internet: IP_FRONTEND:8000

doc pour blob storage avec node.js:
  ->  https://learn.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-nodejs?tabs=environment-variable-linux

variable d'environement:
  -> export AZURE_STORAGE_CONNECTION_STRING="<yourconnectionstring>"

moodle:
  -> https://moodle.msengineering.ch/mod/page/view.php?id=148665

On doit peut etre faire le setup du blob storage dans le startup.py et après l'utiliser dans le code de index.js ?
