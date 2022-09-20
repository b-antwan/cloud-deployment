const express = require('express');


const app = express();

const port = 3000;



async function getObject(){
    //To implement -> Must return Promise of {'title': 'blablabla', 'url':'blablabla'}
    return new Promise({'title': 'My awesome timer', 'url': 'https://www.giantfreakinrobot.com/wp-content/uploads/2022/08/rick-astley.jpg'})
}

//Obj must be {'title': 'blablabla', 'url':'blablabla'}
async function setObject(obj){
    //To implement
    return 200;
}

app.get('/', (req, res) => {
    getObject.then(o => res.send(o));
});


app.post('/', (req, res) => {
    setObject(obj).then(o => res.send(o));
});

app.listen(port);