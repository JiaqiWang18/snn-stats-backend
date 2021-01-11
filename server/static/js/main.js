function main(){
    $.get("/getData", function(data, status){
        console.log(data)
        let raw = []
        let labels = []
        let rawNum = []
        for(key in data){
            labels.push(key)
            arr = []
            numarr = []
            for (sub in data[key]){
                arr.push(data[key][sub].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","))
                numarr.push(data[key][sub])
            }
            rawNum.push(numarr)
            raw.push(arr)
        }

        $("#USTT").text(raw[0][0])
        $("#USR").text(raw[1][0])
        $("#USD").text(raw[2][0])
        $("#CATT").text(raw[3][0])
        $("#CAD").text(raw[4][0])
        $("#LATT").text(raw[5][0])
        $("#LAD").text(raw[6][0])
        $("#OCTT").text(raw[7][0])
        $("#OCD").text(raw[8][0])
        $("#OCR").text(raw[9][0])
        console.log( rawNum)
        const rate = rawNum[7][1]/rawNum[9][1]
        let percentage= Math.round((rate + Number.EPSILON) * 100) / 100* 100
        if(percentage.toString().length>3){
          percentage = percentage.toString().slice(0,3)
        }
        $("#ocpositiverate").text(`${percentage}%`)
        if(rawNum[9][1]==0){
          $("#ocpositiverate").hide()
          $("#hideLabel").hide()
        }else{
          $("#ocpositiverate").show()
          $("#hideLabel").show()
        }
       
        const ids = ["#USTTIncre","#USRIncre","#USDIncre","#CATTIncre","#CADIncre","#LATTIncre","#LADIncre","#OCTTIncre","#OCDIncre","#OCRIncre"]
        for (var i = 0; i < ids.length; i++){
          $(ids[i]).text("+"+raw[i][1])
          if(rawNum[i][1]==0){
            $(ids[i]).hide()
          }else{
            $(ids[i]).show()
          }
        }
        raw=raw.slice(11)
        labels=labels.slice(11)
        console.log(raw)
        console.log(labels)
        
        for (var i = 0; i < raw.length; i++){
            var tr = document.createElement("tr")
            var thTitle = document.createElement("th")
            var thNum = document.createElement("th")
            thTitle.appendChild(document.createTextNode(labels[i]))
            if(raw[i][1] == 0){
                thNum.appendChild(document.createTextNode(raw[i][0]))
            }else{
                if(raw[i][1] < 0){
                  thNum.appendChild(document.createTextNode(raw[i][0] + "  " + raw[i][1]))
                  console.log("yep")
                }
                else{thNum.appendChild(document.createTextNode(raw[i][0] + "  +" + raw[i][1]))}
            }
            tr.appendChild(thTitle)
            tr.appendChild(thNum)
            if (i % 2 == 0){
                tr.setAttribute("class","occitytrR")
            }else{
                tr.setAttribute("class","occitytrY")
            }
            thTitle.setAttribute("class","occityth")
            thNum.setAttribute("class","occityth")
            document.getElementById("OCCity").appendChild(tr)
        }
    });
}


function makeChart(range, initial = false){
    dataAxis = []
    USData = []
    USIncre = []
    LAData = []
    LAIncre = []
    OCData = []
    OCIncre = []
    CAData = []
    CAIncre = []

    var server = new XMLHttpRequest();
    server.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            console.log(data)
            if(initial){
                document.getElementById("sliderDivId").innerHTML = "<table><tr><th><p class = 'title'>Data Range: </p></th><th><input type='range' min='3' max=" + (Object.keys(data).length-1) + " value=" + (Object.keys(data).length-1) + " class='slider' id='graphRange'></th></tr></table>"
                var slider = document.getElementById("graphRange");
                slider.onchange  = function() {
                    let val = this.value;
                    console.log(val)
                    makeChart(val);
            }
            }
            for (date in data){
                console.log(date)
                var day = date.split(".")[1]
                if(day.length == 1){
                    day+="0"
                }
                formatted = date.split(".")[0]+"/"+day
                dataAxis.push(formatted)
                list = data[date]
                USData.push(list[0])
                LAData.push(list[2])
                OCData.push(list[3])
                CAData.push(list[1])               
            }
        
            console.log(USData)
            console.log(LAData)
            for(var i = 0; i < USData.length-1; i ++){
                USIncre.push(USData[i+1]-USData[i])
                CAIncre.push(CAData[i+1]-CAData[i])
                LAIncre.push(LAData[i+1]-LAData[i])
                OCIncre.push(OCData[i+1]-OCData[i])
            }
            document.getElementById("chartTb").innerHTML = `
            <tr>
						<th class = "chartth"> 
							<canvas class = "chartstyle" id = "USC1">Chart1</canvas>
						</th>
						<th class = "chartth">
							<canvas class = "chartstyle" id = "USC2">Chart2</canvas>
						</th>

					</tr>
					<tr>
						<th class = "chartth">
							<canvas class = "chartstyle" id = "CA1">Chart1</canvas>
						</th>
						<th class = "chartth"> 
							<canvas class = "chartstyle" id = "CA2">Chart2</canvas>
						</th>
					</tr>
					<tr>
						<th class = "chartth"><canvas class = "chartstyle" id = "LAC1">LA Chart 1</canvas></th>
					
						<th class = "chartth"><canvas class = "chartstyle" id = "LAC2">LA Chart 2</canvas></th>
					</tr>
					<tr>
						<th class = "chartth"><canvas class = "chartstyle" id = "OCC1">OC Chart 1</canvas></th>
					
						<th class = "chartth"><canvas class = "chartstyle" id = "OCC2">OC Chart 2</canvas></th>
					</tr>
            `;
            
            
    
            renderChart("US Total \u5168\u56fd\u611f\u67d3",USData,dataAxis, "USC1", "rgb(65,192,192)")
            renderChart("LA Total \u6d1b\u6749\u77f6\u53bf\u611f\u67d3",LAData,dataAxis, "LAC1", "rgb(76,235,52)")
            renderChart("CA Total \u52a0\u5dde\u611f\u67d3",CAData,dataAxis, "CA1", "rgb(235,52,52)")
            renderChart("OC Total \u6a59\u53bf\u611f\u67d3",OCData,dataAxis, "OCC1", "rgb(201,52,235)")
            dataAxis.shift()
            renderChart("US Daily Increase \u5168\u56fd\u65b0\u589e", USIncre, dataAxis,"USC2", "rgb(65,192,192)")
            renderChart("OC Daily Increase \u6a59\u53bf\u65b0\u589e", OCIncre, dataAxis,"OCC2", "rgb(201,52,235)")
            renderChart("LA Daily Increase \u6d1b\u6749\u77f6\u53bf\u65b0\u589e",LAIncre,dataAxis, "LAC2", "rgb(76,235,52)")
            renderChart("CA Daily Increase \u52a0\u5dde\u65b0\u589e", CAIncre,dataAxis, "CA2", "rgb(235,52,52)")
        }
    };
    server.open("GET", "/graphData?range="+range, true);
    server.send();

    
}


function renderChart(label, data, xaxis, eleId, color) {
    try {
      var ctx = document.getElementById(eleId)
    } catch (err) {
      return
    }
    var type = 'line'
    if (eleId.includes("2")) {
      type = "bar"
      min = 0
    } else {
      min = Math.round(Math.min(...data) - 0.05 * Math.min(...data))
    }
    var ctx = document.getElementById(eleId)
    //ctx.style.backgroundColor = 'rgb(255,255,255)';
    //ctx.style.padding = '5px';

    //ctx.style.width = "100%"
    //ctx.style.height = "100%"
    var myChart = new Chart(ctx, {
      type: type,
      data: {
        labels: xaxis,
        datasets: [{
          label: null,
          fontColor: "white",

          data: data,
          borderColor: color,
          backgroundColor: color,
          fill: false,

        }]
      },
      options: {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: label,
            fontColor: "white",

      },
        scales: {
          yAxes: [{
            display: true,
            ticks: {
              fontColor: "white",
              min: min,             
            },
            gridLines: {
                display: true ,
                color: "#FFFFFF"
              }
          }],
          xAxes:[{
              ticks: {
                fontColor: "white"
              },
              gridLines: {
                display: true ,
                color: "#FFFFFF"
              },
          }]
        },
        responsive:true,
        //maintainAspectRatio:false
      }
    });
}

$( document ).ready(function() {
  console.log = function() {}

  var modal = document.getElementById("myModal");
  var btn = document.getElementById("myBtn");
  var span = document.getElementsByClassName("close")[0];

  btn.onclick = function() {
    modal.style.display = "block";
  }

  span.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
    main()
    makeChart(Number.MAX_SAFE_INTEGER, true)

});
