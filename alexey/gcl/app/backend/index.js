const express = require('express');


const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;


var cors = require('cors');
app.use(cors());
const path = require('path');
const {Storage} = require('@google-cloud/storage');


async function downloadFromCloud() {

    const serviceKey = path.join(__dirname, './keys.json')
    const storageConf = {keyFilename:serviceKey}
    const storage = new Storage(storageConf)
    const downlaodOptions = {
        destination: __dirname+'/test.txt'
        };

        try {
        let res =await storage
        .bucket('labo1bucket')
        .file('test.txt')
        .download(downlaodOptions)
    }
    catch(err){
        console.log(err)
    }
}


async function uploadToCloud() {
    const serviceKey = path.join(__dirname, './keys.json')
    const storageConf = {keyFilename:serviceKey}
    const storage = new Storage(storageConf)

    try {
        let res = await storage
        .bucket('labo1bucket')
        .upload("test.txt")
    }
        catch(err){
            console.log(err)
        }
}




async function getObject(){
    await downloadFromCloud()
    //read from file test.txt
    const fs = require('fs');
    const data = fs.readFileSync('test.txt', 'utf8');
    console.log(data)
    return data
}

async function setObject(obj){
    //write to file test.txt
    console.log(obj)
    const fs = require('fs');
    fs.writeFileSync('test.txt', JSON.stringify(obj), 'utf8');
    await uploadToCloud()
    return 200
}

app.get('/', (req, res) => {
    getObject().then(o => {
        console.log(o)
        res.status(200).send(o)
    });
});


app.post('/', (req, res) => {
    console.log(req.body)
    setObject(req.body).then(o => {
      res.sendStatus(o)
      console.log("write done")
 });
        
});


app.listen(port);