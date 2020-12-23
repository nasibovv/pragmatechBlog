/**
 * Theme: Metrica - Responsive Bootstrap 4 Admin Dashboard
 * Author: Mannatthemes
 * Opportunities Js
 */

 //Apex-radialbar4

var options = {
  chart: {
    height: 170,
    type: 'radialBar',
    toolbar: {
      show: false
    }
  },
  plotOptions: {
    radialBar: {
      hollow: {
        margin: 0,
        size: "70%",
        background: 'transparent',
      },
     
      dataLabels: {
        name: {
          offsetY: -5,
          color: "#fff",
          fontSize: "13px",
        },
        value: {
          offsetY: 5,
          color: "#ff7d51",
          fontSize: "20px",
          show: true
        }
      }
    }
  },
  colors:['#7680ff'],
  series: [75],
  stroke: {
    lineCap: 'round'
  },
  labels: ['Leads Won'],

}

var chart = new ApexCharts(
  document.querySelector("#apex_radialbar4"),
  options
);

chart.render();