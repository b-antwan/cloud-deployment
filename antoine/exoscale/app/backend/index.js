const express = require('express');


const app = express();
const axios = require('axios');

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = 3000;

var cors = require('cors')
app.use(cors());


const host = "https://sos-ch-gva-2.exo.io"

const obj = "myobj"

const secret = "q3q1jXLfmuHGkNfxbP3LFcvwJaqWuCjsc18Jhzox2nM";
//get request using s3 bucket api
async function getObject() {
    const url = host + "/" + obj;
    const response = await axios(url, {
        method: "GET",
        authorization: secret
    });
    const data = await response.json();
    return data;
}

console.log(getObject());

//Uses exoscale's SOS s3 bucket api
async function setObject(obj) {

}

app.get('/', (req, res) => {
    /*getObject().then(o => {
        console.log(o)
        res.status(200).send(o)
    });*/
    res.status(200).json({ 'title': 'My awesome timer', 'url': 'https://www.giantfreakinrobot.com/wp-content/uploads/2022/08/rick-astley.jpg' });
});


app.post('/', (req, res) => {
    setObject(req.body).then(o => res.sendStatus(o));
});

app.listen(port);

