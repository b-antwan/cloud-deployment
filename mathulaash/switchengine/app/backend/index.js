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