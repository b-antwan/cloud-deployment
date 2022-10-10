const backaddr = "http://86.119.32.139";

const myHeader = new Headers({
    'Access-Control-Allow-Origin': backaddr+':3000',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
});

async function get() {
    await fetch( backaddr+':3000/',
    {
        headers : myHeader,
        method: 'GET'
    })
    .then(async function(response) {
        if(response.status !== 200){
            console.log("Error while getting data");
        } else{
            output = await response.json();
            console.log(output);
            document.getElementById('title_out').innerHTML = output.title;
            document.getElementById('image').src = output.url;
            document.getElementById('image').style.display = "block";
        }
    });
}

async function post() {
    await fetch(backaddr+':3000/',
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
