let arr = [['Region',   'Votes']]

let arr_imp = []

function loadArray(callback) {
    let year = document.getElementById('year').value
    let parti = document.getElementById('parti').value
    let url = `http://localhost:4042/result-per-year-region?year=${year}&parti=${parti}`
    fetch(url)
    .then(res => res.json())
    .then(res => {
        if(res) {
            arr_imp = []    
            arr_imp.push(['Region',   'Votes'])
            for(let i = 0; i < res.length; i++) {
                arr_imp.push([res[i].region, res[i].evolution])
            }
            console.log(arr_imp)
            callback()
        }
    })
}

function loadArrayQ2(callback) {
    let year = document.getElementById('year1').value
    let url = `http://localhost:4042/result-per-year?year=${year}`
    fetch(url)
    .then(res => res.json())
    .then(res => {
        if(res) {
            arr_imp = []
            arr_imp.push(['Region',   'Participation'])
            for(let i = 0; i < res.length; i++) {
                arr_imp.push([res[i].region, res[i].taux_paticip])
            }
            callback()
        }
    })
}

function loadMap() {
    google.charts.load('current', {
        'packages':['geochart'],
        'mapsApiKey': 'AIzaSyCqnJzg7vdeP17AviEQkWBIzwJVCf1I-Qo'
      });
      google.charts.setOnLoadCallback(drawRegionsMap);
    
    function drawRegionsMap() {
      var data = google.visualization.arrayToDataTable(arr_imp); 
    
        var options = {
            region: 'FR',
            displayMode: 'markers',
            colorAxis: {colors: ['red', 'blue']}
        };
    
        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
    
        chart.draw(data, options);
    }
    
}

function reloadDataQ4() {
    loadArray(() => {
        loadMap()
    })
}

function reloadDataQ2() {
    loadArrayQ2(() => {
        loadMap()
    })
}

