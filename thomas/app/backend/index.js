const express = require('express');
const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors')
app.use(cors());

async function getObject(){
    //To implement -> Must return Promise of {'title': 'blablabla', 'url':'blablabla'}
    return new Promise((resolve, reject) => {
        JSON.stringify({'title': 'My awesome timer', 'url': 'https://www.giantfreakinrobot.com/wp-content/uploads/2022/08/rick-astley.jpg'})
            }).then((state) => {
                console.log("yeeeees");
            })
            .catch((error) => {
                console.log("aie");
            });
    //return new Promise(() => { JSON.stringify({'title': 'My awesome timer', 'url': 'https://www.giantfreakinrobot.com/wp-content/uploads/2022/08/rick-astley.jpg'})})
}

//Obj must be {'title': 'blablabla', 'url':'blablabla'}
async function setObject(obj){
    //To implement
    return 200;
}

app.get('/', (req, res) => {
    /*getObject().then(o => {
        console.log(o)
        res.status(200).send(o)
    });*/
    res.status(200).json({'title': 'My awesome timer', 'url': 'https://www.giantfreakinrobot.com/wp-content/uploads/2022/08/rick-astley.jpg'});
});


app.post('/', (req, res) => {
    setObject(req.body).then(o => res.sendStatus(o));
});

app.listen(port);

/////////////////////////// TEMPLATE BLOB STORAGE ////////////////////////////////////

// TODO -> set la variable d'environement
const AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING;

if(!AZURE_STORAGE_CONNECTION_STRING) {
    throw Error("Azure Storage Connection string not found");
}

// Create the BlobServiceClient object which will be used to create a container client
const blobServiceClient = BlobServiceClient.fromConnectionString(
    AZURE_STORAGE_CONNECTION_STRING
);
  
// Create a unique name for the container
const containerName = "quickstart" + uuidv1();
  
console.log("\nCreating container...");
console.log("\t", containerName);
  
/*// Get a reference to a container
const containerClient = blobServiceClient.getContainerClient(containerName);
// Create the container
const createContainerResponse = await containerClient.create();
console.log(`Container was created successfully.\n\trequestId:${createContainerResponse.requestId}\n\tURL: ${containerClient.url}`);

// Create a unique name for the blob
const blobName = "quickstart" + uuidv1() + ".txt";

// Get a block blob client
const blockBlobClient = containerClient.getBlockBlobClient(blobName);

// Display blob name and url
console.log(`\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`);

// Upload data to the blob
const data = "Hello, World!";
const uploadBlobResponse = await blockBlobClient.upload(data, data.length);
console.log(`Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`);

console.log("\nListing blobs...");

// List the blob(s) in the container.
for await (const blob of containerClient.listBlobsFlat()) {

    // Get Blob Client from name, to get the URL
    const tempBlockBlobClient = containerClient.getBlockBlobClient(blob.name);

    // Display blob name and URL
    console.log(`\n\tname: ${blob.name}\n\tURL: ${tempBlockBlobClient.url}\n`);
}

// Get blob content from position 0 to the end
// In Node.js, get downloaded data by accessing downloadBlockBlobResponse.readableStreamBody
// In browsers, get downloaded data by accessing downloadBlockBlobResponse.blobBody
const downloadBlockBlobResponse = await blockBlobClient.download(0);
console.log("\nDownloaded blob content...");
console.log("\t", await streamToText(downloadBlockBlobResponse.readableStreamBody));

// Convert stream to text
async function streamToText(readable) {
    readable.setEncoding('utf8');
    let data = '';
    for await (const chunk of readable) {
        data += chunk;
    }
    return data;
}

// Delete container
console.log("\nDeleting container...");

const deleteContainerResponse = await containerClient.delete();
console.log("Container was deleted successfully. requestId: ", deleteContainerResponse.requestId);*/