const express = require('express');
const { exec } = require("child_process");

const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors');
const fs = require('fs');
app.use(cors());


var fileData = {};

async function getObject() {
    //Use the command "s3cmd get --force s3://cloudbuck/data.json"
    //then read data.json
    exec("s3cmd get --force s3://cloudbuck/data.json", (error, stdout, stderr) => {
        if (error) {
            console.log(" error : " + error.message);
        }
        if (stderr) {
            console.log(" stderr : " + stderr);
        }
        console.log("GET DONE :");
        console.log(" stdout : " + stdout);
    });
    //read data.json and return its contents
    fileData = JSON.parse(fs.readFileSync('data.json'));
}

async function setObject(obj) {
    //write obj to data.json
    fs.writeFileSync('data.json', JSON.stringify(obj));

    console.log("data.json written");
    console.log(JSON.parse(fs.readFileSync("data.json")));
    
    console.log("Starting put");
    exec("s3cmd put data.json s3://cloudbuck/data.json", (error, stdout, stderr) => {
        if (error) {
            console.log(" error : " + error.message);
        }
        if (stderr) {
            console.log(" stderr : " + stderr);
        }
        console.log("SET DONE :");

        console.log(" stdout : " + stdout);
    });
    return 200;
}

setObject({ title: "test", url: "testqoqeoq" }).then(() => {
    getObject().then(() => {
        console.log(" hehe ");
        console.log(fileData);
    });
});

app.get('/', (req, res) => {
    getObject().then(() => {
        console.log(fileData);
        res.send(fileData);
    });
});


app.post('/', (req, res) => {
    setObject(req.body).then(o => res.sendStatus(o));
});

app.listen(port);