# Cloud - Lab 1 : Azure

Made by Thomas Dagier for Cloud course at HES-SO Master

## Manual deployment

### Frontend

- modify script.js with backend's ip address
- python3 -m http.server

### Backend

- apt update -y
- apt instal node -y
- apt install npm -y
- export AZURE_STORAGE_CONNECTION_STRING=...
- npm install
- node index.js

### Test

- go to FRONTEND_IP_ADDRESS:8000
- test...

### Automatic deployment

- export AZURE_SUBSCRIPTION_ID=...
- pip install -r requirements.txt
- python3 startup.py

## Notes

- connect -> ssh -i thomas-aids.pem azureuser@FRONT_IP/BACK_IP
- security groups -> FRONT = inbound source any:* dst any:8000
                  -> BACK  = inbound source any:* dst any:3000

[blob storage doc](https://learn.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-nodejs?tabs=environment-variable-linux)

[moodle course](https://moodle.msengineering.ch/mod/page/view.php?id=148665)

[blob storage infos](https://cloudblogs.microsoft.com/opensource/2017/11/09/s3cmd-amazon-s3-compatible-apps-azure-storage/)
