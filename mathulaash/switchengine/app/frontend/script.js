let back_addr = "localhost";

const myHeader = new Headers({
    'Access-Control-Allow-Origin': 'http://' + back_addr + ':3000',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
});

async function get() {
    await fetch('//' + back_addr + ':3000/',
    {
        headers : myHeader,
        method: 'GET'
    })
    .then(async function(response) {
        if(response.status !== 200){
            console.log("Error while getting data");
        } else{
            output = await response.json();
            document.getElementById('title_out').innerHTML = output.title;
            document.getElementById('image').src = output.url;
            document.getElementById('image').style.display = "block";
        }
    });
}

async function post() {
    await fetch('//' + back_addr + ':3000/',
    {
        headers : myHeader,
        method: 'POST',
        body : JSON.stringify(
            {title: document.getElementById('title_in').value, 
             url: document.getElementById('url_in').value})
    })
    .then(async function(response) {
        if(response.status !== 200){
            console.log("Error while posting data");
        } else{
            document.getElementById('title_in').value = "";
            document.getElementById('url_in').value = "";
        }
    });
}