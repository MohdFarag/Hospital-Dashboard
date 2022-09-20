/* ChartJS
    * -------
    * Data and config for chartjs
    */
'use strict';


function piechart(labelsList, counts, id){
    
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
        backgroundColor: [
            'rgba(92, 212, 40, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(212, 40, 195, 1)'
        ],
        borderColor: [
            'rgba(255, 255, 255, 1)'
        ],
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

function buildChart(list, id){

    var Labels = Array();
    var Counts = Array();
    for (const device of list ) {
        Labels.push( device[0]  );
        Counts.push( device[1]  );      
    }
    piechart(Labels, Counts, id);  

}

