/**
 * Theme: Metrica - Responsive Bootstrap 4 Admin Dashboard
 * Author: Mannatthemes
 * Hospital Dashboard Js
 */

var options = {
  chart: {
      height: 320,
      type: 'area',
      stacked: true,
      toolbar: {
        show: false,
        autoSelected: 'zoom'
      },
  },
  colors: ['#2a77f4', '#a5c2f1'],
  dataLabels: {
      enabled: false
  },
  stroke: {
      curve: 'smooth',
      width: [1.5, 1.5],
      dashArray: [0, 4],
      lineCap: 'round'
  },
  grid: {
    borderColor: "#45404a2e",
    padding: {
      left: 0,
      right: 0
    },
    strokeDashArray: 4,
  },
  markers: {
    size: 0,
    hover: {
      size: 0
    }
  },
  series: [{
      name: 'New Visits',
      data: [0,60,20,90,45,110,55,130,44,110,75,120]
  }, {
      name: 'Unique Visits',
      data: [0,45,10,75,35,94,40,115,30,105,65,110]
  }],

  xaxis: {
      type: 'month',
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      axisBorder: {
        show: true,
        color: '#45404a2e',
      },  
      axisTicks: {
        show: true,
        color: '#45404a2e',
      },                  
  },
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.4,
      opacityTo: 0.3,
      stops: [0, 90, 100]
    }
  },
  
  tooltip: {
      x: {
          format: 'dd/MM/yy HH:mm'
      },
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right'
  },
}

var chart = new ApexCharts(
  document.querySelector("#hospital_survey"),
  options
);

chart.render();



 //colunm-1
  
  var options = {
    chart: {
        height: 200,
        type: 'bar',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            endingShape: 'rounded',
            columnWidth: '25%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 1,
        colors: ['transparent']
    },
    colors: ["#7367f0", "#dfdeec"],
    series: [{
        name: 'Male',
        data: [68, 44, 55, 57, 56, 61, 58]
    }, {
        name: 'Female',
        data: [51, 76, 85, 101, 98, 87, 105]
    },],
    xaxis: {
        categories: ['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Set'],
        axisBorder: {
          show: true,
          color: '#bec7e0',
        },  
        axisTicks: {
          show: true,
          color: '#bec7e0',
        },    
    },
    legend: {
      show: false,
      position: 'top',
      horizontalAlign: 'right',
    },
   
    fill: {
        opacity: 1
  
    },
    grid: {
        row: {
            colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.2
        },
        borderColor: '#f1f3fa',
        strokeDashArray: 4,
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return "" + val 
            }
        }
    }
  }
  
  var chart = new ApexCharts(
    document.querySelector("#patient_dash_report"),
    options
  );
  
  chart.render();


  

//Medicine-widget


var options = {
  chart: {
      height: 225,
      type: 'donut',
  }, 
  plotOptions: {
    pie: {
      donut: {
        size: '80%'
      }
    }
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
 
  series: [10, 65, 25,],
  legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      verticalAlign: 'middle',
      floating: false,
      fontSize: '14px',
      offsetX: 0,
      offsetY: 5
  },
  labels: [ "Syrup", "Tablets", "Injections"],
  colors: ['#fdbaad', '#2a77f4', '#58ded0'],
 
  responsive: [{
      breakpoint: 600,
      options: {
        plotOptions: {
            donut: {
              customScale: 0.2
            }
          },        
          chart: {
              height: 240
          },
          legend: {
              show: false
          },
      }
  }],

  tooltip: {
    y: {
        formatter: function (val) {
            return   val + " %"
        }
    }
  }
  
}

var chart = new ApexCharts(
  document.querySelector("#dash_medicine"),
  options
);

chart.render();

// Datepicker



// Datatable
$('#datatable').DataTable();