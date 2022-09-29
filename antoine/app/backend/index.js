const express = require('express');


const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors')
app.use(cors());

async function getObject(){
    //Use the command "s3cmd get --force s3://cloudbuck/data.json"
    //then read data.json
}

async function setObject(obj){
    //Write objs to data.json
    //And use the command:
    //"s3cmd put s3://cloudbuck/data.json"
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