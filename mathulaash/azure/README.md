# Cloud - Lab 1 : Azure

Made by Thomas Dagier for Cloud course at HES-SO Master

## Manual deployment

### Frontend

- modify script.js with backend's ip address (script.js l.2)
- python3 -m http.server

### Backend

- apt update -y
- apt install nodejs npm -y
- export AZURE_STORAGE_CONNECTION_STRING=...
- npm install
- node index.js

### SSH connection (both frontend - backend)

- ssh -i <KEY.PEM> azureuser@<IP_ADDRESS>

### Test

- go to <FRONTEND_IP_ADDRESS>:8000
- test...

## Automatic deployment

### Requirements

First, you'll need to have 2 images of instances you deployed manually and their corresponding security groups
For security group, you'll need to add those rules :
FRONT => inbound source any:* dst any:8000
BACK  => inbound source any:* dst any:3000

### Commands

- python3 -m venv .venv
- source .venv/bin/activate
- export AZURE_SUBSCRIPTION_ID=...
- export AZURE_STORAGE_CONNECTION_STRING=...
- pip install -r requirements.txt
- python3 startup.py

## Notes

- [blob storage doc](https://learn.microsoft.com/fr-fr/azure/storage/blobs/storage-quickstart-blobs-nodejs?tabs=environment-variable-linux)
- [blob storage infos](https://cloudblogs.microsoft.com/opensource/2017/11/09/s3cmd-amazon-s3-compatible-apps-azure-storage/)
- [moodle course](https://moodle.msengineering.ch/mod/page/view.php?id=148665)
- [doc for deployment](https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-virtual-machines?tabs=cmd)
