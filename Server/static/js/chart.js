$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';
  
  var options = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true
    }
  };

  var equipmentTypesData = {
    datasets: [{
      data: [40, 20, 30],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'Pink',
      'Blue',
      'Yellow',
    ]
  };
  if ($("#equipmentTypes").length) {
    var pieChartCanvas = $("#equipmentTypes").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: equipmentTypesData,
      options: options
    });
  }

  var technicalStatusData = {
    datasets: [{
      data: [15, 20, 10,2],
      backgroundColor: [
        'rgba(80, 200, 120, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(150, 0, 24, 0.5)',
        'rgba(54, 162, 235, 0.5)'
      ],
      borderColor: [
        'rgba(80, 200, 120, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(150, 0, 24, 1)',
        'rgba(54, 162, 235, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'FF',
      'PF',
      'NF',
      'Not Updated',
    ]
  };
  if ($("#technicalStatus").length) {
    var pieChartCanvas = $("#technicalStatus").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: technicalStatusData,
      options: options
    });
  }

  var contractType  = {
    datasets: [{
      data: [20, 10, 35],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'Local',
      'Service',
      'Warranty',
    ]
  };
  if ($("#contractType").length) {
    var pieChartCanvas = $("#contractType").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: contractType,
      options: options
    });
  }

  var inspectionData = {
    datasets: [{
      data: [15, 10, 10],
      backgroundColor: [
        'rgba(80, 200, 120, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(150, 0, 24, 0.5)',
        'rgba(54, 162, 235, 0.5)'
      ],
      borderColor: [
        'rgba(80, 200, 120, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(150, 0, 24, 1)',
        'rgba(54, 162, 235, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'On time',
      'Late',
      'Not Inspected',
    ]
  };
  if ($("#inspection").length) {
    var pieChartCanvas = $("#inspection").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: inspectionData,
      options: options
    });
  }

  var ppmData = {
    datasets: [{
      data: [10, 20, 10],
      backgroundColor: [
        'rgba(80, 200, 120, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(150, 0, 24, 0.5)',
        'rgba(54, 162, 235, 0.5)'
      ],
      borderColor: [
        'rgba(80, 200, 120, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(150, 0, 24, 1)',
        'rgba(54, 162, 235, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'On time',
      'Late',
      'Not Checked',
    ]
  };
  if ($("#ppm").length) {
    var pieChartCanvas = $("#ppm").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: ppmData,
      options: options
    });
  }

  var calibrationData = {
    datasets: [{
      data: [15, 25, 5],
      backgroundColor: [
        'rgba(80, 200, 120, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(150, 0, 24, 0.5)',
        'rgba(54, 162, 235, 0.5)'
      ],
      borderColor: [
        'rgba(80, 200, 120, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(150, 0, 24, 1)',
        'rgba(54, 162, 235, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'On time',
      'Late',
      'Not Calibrated',
    ]
  };
  if ($("#calibration").length) {
    var pieChartCanvas = $("#calibration").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: calibrationData,
      options: options
    });
  }

});