
const myHeader = new Headers({
    'Access-Control-Allow-Origin': 'http://localhost:8080',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
});

async function get() {
    await fetch('//localhost:3000/',
    {
        headers : myHeader,
        method: 'GET'
    })
    .then(async function(response) {
        if(response.status === 200){
            console.log("Error while getting data");
        } else{
            output = await response.json();
            
            var title = document.getElementById('title_out');    
            var img = document.getElementById('image');
            img.style.display = "block";

            title.value = output.title;
            img.src = output.url; //"https://i.ibb.co/4MVtB6F/unknown.png";
        }
    });
}

async function post() {
    await fetch('//localhost:3000/',
    {
        headers : myHeader,
        method: 'POST',
        body : JSON.stringify(
            {'title': document.getElementById('title_in').value, 
            'url': document.getElementById('url_in').value})
    })
    .then(async function(response) {
        if(response.status === 200){
            console.log("Error while posting data from");
        } else{
            document.getElementById('title_in').value = "";
            document.getElementById('url_in').value = "";
        }
    });

}