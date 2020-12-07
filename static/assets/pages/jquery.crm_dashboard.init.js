/**
 * Theme: Metrica - Responsive Bootstrap 4 Admin Dashboard
 * Author: Mannatthemes
 * CRM Dashboard Js
 */

var options = {
  chart: {
      height: 350,
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
  document.querySelector("#liveVisits"),
  options
);

chart.render();


var options = {
  chart: {
      height: 270,
      type: 'radialBar',
  },
  plotOptions: {
      radialBar: {
          startAngle: -135,
          endAngle: 135,
          hollow: {
            margin: 0,
            size: "55%",
          },
          track: {
            background: '#b9c1d4',
            opacity: 0.3, 
            strokeWidth: '90%',           
          },
          dataLabels: {
              name: {
                  fontSize: '15px',
                  color: '#8997bd',                 
                  offsetY: 95, 
                  fontFamily: 'Roboto, sans-serif',                 
              },
              value: {
                  offsetY: 50,
                  fontSize: '22px',
                  color: '#8997bd',
                  formatter: function (val) {
                      return val + "%";
                  }
              }
          }
      }
  },
  fill: {
      gradient: {
          enabled: true,
          shade: 'dark',
          shadeIntensity: 0.15,
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 50, 65, 91]
      },
  },
  stroke: {
      dashArray: 4,
  },
  colors: ["#727cf5"],
  series: [67],
  labels: ['New Leads Target'],
  responsive: [{
      breakpoint: 380,
      options: {
        chart: {
          height: 280
        }
      }
  }]
}

var chart = new ApexCharts(
  document.querySelector("#apex_radialbar3"),
  options
);

chart.render();

