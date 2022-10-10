const express = require('express');
const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors')
app.use(cors());

const { BlobServiceClient } = require('@azure/storage-blob');
const { v1: uuidv1} = require('uuid');
require('dotenv').config();

var containerClient;
var blockBlobClient;

async function getObject(){
    const downloadBlockBlobResponse = await blockBlobClient.download(0);
    console.log("\nDownloaded blob content...");
    content = await streamToText(downloadBlockBlobResponse.readableStreamBody);
    console.log("\t", content);

    async function streamToText(readable) {
        readable.setEncoding('utf8');
        let data = '';
        for await (const chunk of readable) {
            data += chunk;
        }
        return data;
    }

    return content;
}

async function setObject(obj){
    const blobName = "item_" + uuidv1();
    blockBlobClient = containerClient.getBlockBlobClient(blobName);
    console.log(`\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`);

    const data = JSON.stringify(obj);
    const uploadBlobResponse = await blockBlobClient.upload(data, data.length);
    console.log(`Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`);

    return 200;
}

app.get('/', (req, res) => {
    getObject().then(o => {
        console.log(o)
        res.status(200).send(o)
    });
});


app.post('/', (req, res) => {
    setObject(req.body).then(o => res.sendStatus(o));
});

async function create_azure_storage() {
    console.log('Azure Blob storage v12 - JavaScript quickstart sample');

    const AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING;
    
    if(!AZURE_STORAGE_CONNECTION_STRING) {
        throw Error("Azure Storage Connection string not found");
    }

    const blobServiceClient = BlobServiceClient.fromConnectionString(
        AZURE_STORAGE_CONNECTION_STRING
    );
  
    const containerName = "app" + uuidv1();
        
    console.log("\nCreating container...");
    console.log("\t", containerName);
        
    containerClient = blobServiceClient.getContainerClient(containerName);
    const createContainerResponse = await containerClient.create();
    console.log(`Container was created successfully.\n\trequestId:${createContainerResponse.requestId}\n\tURL: ${containerClient.url}`);
}

create_azure_storage();
app.listen(port);

process.on('SIGINT', async function () { 
    console.log("lol1");
    const deleteContainerResponse = await containerClient.delete();
    console.log("Container was deleted successfully. requestId: ", deleteContainerResponse.requestId);
    process.exit(0);
});

process.on('SIGTERM', async function () { 
    console.log("lol2");
    const deleteContainerResponse = await containerClient.delete();
    console.log("Container was deleted successfully. requestId: ", deleteContainerResponse.requestId);
    process.exit(0);
});