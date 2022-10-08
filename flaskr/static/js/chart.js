/* ChartJS
* -------
* Data and config for chartjs
*/
'use strict';

var backgroundColors = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]

var borderColors = [
    'rgba(255, 255, 255, 1)'
]


function pieChart(labelsList, counts, id){
    var options = {
        responsive: true,
        animation: {
            animateScale: true,
            animateRotate: true
        }
    };

    var chartTypesData = {
        datasets: [{
        data: counts,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: labelsList
    };
    if ($("#"+id).length) {
        var pieChartCanvas = $("#"+id).get(0).getContext("2d");
        var pieChart = new Chart(pieChartCanvas, {
        type: 'pie',
        data: chartTypesData,
        options: options
        });
    }
}

function doughnutChart(labelsList, counts, id){
    var options = {
        responsive: true,
        animation: {
            animateScale: true,
            animateRotate: true
        }
    };

    var chartTypesData = {
        datasets: [{
        data: counts,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: labelsList
    };

    if ($("#"+id).length) {
        var doughnutChartCanvas = $("#"+id).get(0).getContext("2d");
        var doughnutChart = new Chart(doughnutChartCanvas, {
          type: 'doughnut',
          data: chartTypesData,
          options: options
        });
    }
}

function buildChart(list, id, type){

    var Labels = Array();
    var Counts = Array();
    for (const device of list ) {
        Labels.push( device[0]  );
        Counts.push( device[1]  );      
    }

    if (type=="pie") {
        pieChart(Labels, Counts, id); 
    }else if (type=="doughnut") {
        doughnutChart(Labels, Counts, id); 
    }
     

}

