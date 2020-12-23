/**
 * Theme: Metrica - Responsive Bootstrap 4 Admin Dashboard
 * Author: Mannatthemes
 * Dashboard Js
 */


  //colunm-1
  
  var options = {
    chart: {
        height: 295,
        type: 'bar',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            endingShape: 'rounded',
            columnWidth: '30%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    colors: ["rgba(42, 118, 244, .18)", '#2a76f4'],
    series: [{
        name: 'New Visitors',
        data: [68, 44, 55, 57, 56, 61, 58, 63, 60, 66]
    }, {
        name: 'Unique Visitors',
        data: [51, 76, 85, 101, 98, 87, 105, 91, 114, 94]
    },],
    xaxis: {
        categories: ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
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
      offsetY: 6,
    },
    yaxis: {
        title: {
            text: 'Visitors',
        },
    },
    fill: {
        opacity: 1
  
    },
    // legend: {
    //     floating: true
    // },
    grid: {
        row: {
            colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.2,           
        },
        strokeDashArray: 4,
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return "" + val + "k"
            }
        }
    }
  }
  
  var chart = new ApexCharts(
    document.querySelector("#ana_dash_1"),
    options
  );
  
  chart.render();
  
  
  // traffice chart

  var options = {
    chart: {
        height: 250,
        type: 'area',
        stacked: true,
        toolbar: {
          show: false,
          autoSelected: 'zoom'
        },
    },
    colors: ['#2a77f4', '#1ccab8'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: [2, 2],
        dashArray: [0, 2]
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
        name: 'Organic Search',
        data: [0,60,20,90,45,110,55,130,44,110,75,200]
    }, {
        name: 'Social Media',
        data: [0,45,10,75,35,94,40,115,30,105,65,190]
    }],
  
    
  
    xaxis: {
        type: 'time',
        categories: ["00:00", "01:30", "02:30", "03:30", "04:30", "05:30", "06:30", "07:30", "08:30", "09:30", "10:30", "11:30"],  
        axisBorder: {
          show: true,
          color: '#45404a2e',
        },  
        axisTicks: {
          show: true,
          color: '#45404a2e',
        },                  
    },
  
    tooltip: {
        x: {
            format: 'HH:mm'
        },
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right'
    },
  }
  
  var chart = new ApexCharts(
    document.querySelector("#liveVisits"),
    options
  );
  
  chart.render();
  
  
  //Device-widget
  
  
  var options = {
    chart: {
        height: 200,
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
        show: false,
        position: 'bottom',
        horizontalAlign: 'center',
        verticalAlign: 'middle',
        floating: false,
        fontSize: '14px',
        offsetX: 0,
        offsetY: 5
    },
    labels: [ "Tablet", "Desktop", "Mobile"],
    colors: ["#fda354", "#506ee4", "#41cbd8"],
   
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
    document.querySelector("#ana_device"),
    options
  );
  
  chart.render();


  // map

$('#usa').vectorMap({
  map: 'us_aea_en',
  backgroundColor: 'transparent',
  borderColor: '#818181',
  regionStyle: {
    initial: {
      fill: '#506ee424',
    }
  },
  series: {
    regions: [{
        values: {
            "US-VA": '#506ee452',
            "US-PA": '#506ee452',
            "US-TN": '#506ee452',
            "US-WY": '#506ee452',
            "US-WA": '#506ee452',
            "US-TX": '#506ee452',
        },
        attribute: 'fill',
    }]
  },
});