var options = {
                  series: [
                  {
                    name: 'Mandalay Temperature',
                    data: {{ previous_lis|safe }}   
                     }
                ],
                  chart: {
                  height: 350,
                  width: '100%',
                  type: 'rangeArea',
                  offsetY: 30,
                  
                },
                stroke: {
                  curve: 'smooth'
                },
                title: {
                  text: 'Mandalay Temperature (Previous 30 days)'
                },
                markers: {
                  hover: {
                    sizeOffset: 5
                  }
                },
                dataLabels: {
                  enabled: false,
                  textAnchor: 'end',
                },
                xaxis: {
                    type: 'datetime',
                
                },
                yaxis: {
                    min:20,
                  labels: {
                    formatter: (val) => {
                      return Math.round( val ) + '°C'
                    }
                  }
                }
                };
            
var chart = new ApexCharts(document.querySelector("#chart1"), options);
chart.render();
var options = {
                  series: [
                  {
                    name: 'Mandalay Temperature',
                    data: {{ future_lis|safe }}   
                     }
                ],
                  chart: {
                  height: 350,
                  width: '100%',
                  type: 'rangeArea',
                  offsetY: 30,
                  
                },
                stroke: {
                  curve: 'smooth'
                },
                title: {
                  text: 'Mandalay Temperature (5 days prediction)'
                },
                markers: {
                  hover: {
                    sizeOffset: 5
                  }
                },
                dataLabels: {
                  enabled: false,
                  textAnchor: 'end',
                },
                xaxis: {
                    type: 'datetime',
                
                },
                yaxis: {
                    min:20,
                  labels: {
                    formatter: (val) => {
                      return Math.round( val ) + '°C'
                    }
                  }
                }
                };
            
var chart = new ApexCharts(document.querySelector("#chart2"), options);
chart.render();