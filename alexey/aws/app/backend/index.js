const express = require('express');


const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors')
app.use(cors());

const REGION = "us-east-1";

const bucketParams = {
  Bucket: "lavabucket4",
  Key: "test.json",
};

const { S3Client, GetObjectCommand, PutObjectCommand } = require('@aws-sdk/client-s3');
const client = new S3Client({region: REGION});

const streamToString = (stream) => new Promise((resolve, reject) => {
  const chunks = [];
  stream.on('data', (chunk) => chunks.push(chunk));
  stream.on('error', reject);
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
});

const readObject = async (bucket, key) => {
  const params = {
    Bucket: bucket,
    Key: key,
  };
  const command = new GetObjectCommand(params);
  const response = await client.send(command);
  const { Body } = response; 
  return streamToString(Body);
};

const writeObject = async (bucket,key,body) => {
  const uploadparams = {
    Bucket: bucket,
    Key: key,
    Body: body
  };
  const command = new PutObjectCommand(uploadparams);
  const response = await client.send(command);
  return response
};


async function getObject(){
  return readObject(bucketParams.Bucket,bucketParams.Key)   
}

//Obj must be {'title': 'blablabla', 'url':'blablabla'}
async function setObject(obj){
    return writeObject(bucketParams.Bucket,bucketParams.Key,JSON.stringify(obj)).then( o => {
      console.log("write OK")
      console.log(o)
      return 200;
    }
    );

}



app.get('/', (req, res) => {
    getObject().then(o => {
        console.log(o)
        res.status(200).send(o)
    });

});


app.post('/', (req, res) => {
  
    setObject(req.body).then(o => {
      res.sendStatus(o)
      console.log("write")
 });
        
});


app.listen(port);