# Start the HTML and Javascript code
print '''
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["treemap"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
'''

print CountBugs('path/to/repo')

# Finish the HTML and Javascript
print '''
        ]);

        // Create and draw the visualization.
        var tree = new google.visualization.TreeMap(document.getElementById('chart_div'));
        tree.draw(data, {
          maxDepth: 2,
          minColor: 'YellowGreen',
          midColor: 'LightGoldenRodYellow',
          maxColor: 'Red',
          headerHeight: 15,
          fontColor: 'black',
          showScale: true});
        }
    </script>
  </head>

  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
'''
