Pour lancer le programme:

source bin/activate
pip install -r requirements.txt
python3 startup.py

tester le programme sur internet: IP_FRONTEND:8000

doc pour blob storage avec node.js:
  ->  https://learn.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-nodejs?tabs=environment-variable-linux

moodle:
  -> https://moodle.msengineering.ch/mod/page/view.php?id=148665

INFOS:

Microsoft Azure provides excellent object storage with  Azure Blob Storage, which offers unmatched durability, virtually infinite capacity and multiple tiers of storage, all at very convenient rates. However, because Azure Blob Storage was developed before the world decided to “standardize” on the S3 APIs, the two use different interfaces, and so most applications and libraries designed to work with Amazon S3 do not support Azure out-of-the-box.
-> https://cloudblogs.microsoft.com/opensource/2017/11/09/s3cmd-amazon-s3-compatible-apps-azure-storage/


Deploiement:

1- export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=cloudlab1;AccountKey=Dj7nJbfXaUy+U8+WEgfX0yB/wJ0k+havtFTLkuZIKAUuAuj+5T6wflQJ5zpQSNxUNrCfTnCZZsLe+AStlP02Vg==;EndpointSuffix=core.windows.net"


2- export AZURE_SUBSCRIPTION_ID=f0514094-5bb5-4925-9323-de8fc229bb63

Notes:

- tips -> appeler les VMs "BACK" et "FRONT"
- se connecter -> dans le terminal: ssh -i thomas-aids.pem azureuser@IP_FRONT (ou IP_BACK)
- /!\ modifier l'ip du backend dans le script du frontend
- les SG -> FRONT = inbound source any:* dst any:8000
            BACK  = inbound source any:* dst any:3000

https://media-exp1.licdn.com/dms/image/D4D03AQFod2XwsQFf2A/profile-displayphoto-shrink_800_800/0/1662067030074?e=1669852800&v=beta&t=2TTtgKV9UM5xcfT20NxII7jSQ90Xvq00G0KkjUyKC3Q


Pour lancer le script:

sudo apt install python3.8-venv
python3 -m venv .venv
source .venv/bin/activate
export AZURE_SUBSCRIPTION_ID=f0514094-5bb5-4925-9323-de8fc229bb63
pip install -r requirements.txt
python3 startup.py