function mainPageHeader(){
    var server = new XMLHttpRequest();
    server.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        data = JSON.parse(this.responseText)
        var counter = 0
        var i = 1
        for (title in data){
            if(counter == 0 || counter == 3 || counter == 5 || counter == 7){
                var tr = document.createElement("tr")
                var labelth = document.createElement("th")
                var numth = document.createElement("th")
                var increaseth = document.createElement("th")
                var label = document.createTextNode(title)
                var num = document.createTextNode(data[title][0])
                var increase = document.createTextNode(`+ ${data[title][1]}`)
                labelth.appendChild(label)
                numth.appendChild(num)
                increaseth.appendChild(increase)
                tr.appendChild(labelth)
                tr.appendChild(numth)
                tr.appendChild(increaseth)
                tr.addEventListener('click', function () {
                    window.location.href = 'http://snnnewsus.com/corona-virus/'
                });
                if(i%2==0){
                    tr.setAttribute("class","white")
                }
                else{
                tr.setAttribute("class","grey")
                }
                document.getElementById("headerStats").appendChild(tr);
                console.log(counter)
                i++;
            }
            counter++;
            
        }    
    }
    };
    server.open("GET", "https://snnstatsapi.herokuapp.com/getData", true);
    server.send();
}

mainPageHeader()