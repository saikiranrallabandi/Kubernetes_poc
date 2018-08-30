 $(document).ready(function () {
//   $.each(dashboardData, function (key, value) {
//       console.log(dashboardData["awsaccount"]);
//       $("#dashboard").append('<div class="animated flipInY col-lg-3 col-md-3 col-sm-6 col-xs-12"><div class="tile-stats"><div class="icon"><i class="fa fa-sitemap" style="color: #2361ae!important;"></i></div><div class="count" id="fetchvalue" style="color: #337ab7;">' + value + '</div>' + '<h3 id="fetchkey" style="color: #337ab7;">' + key+'</h3>'+'<p></p>'+'</div>'+'</div>');
//       });
//
//
//
//
//      //setInterval('autoRefresh1()', 5000);
//        });

url = 'api/dashboard'
var settings = {
  "async": true,
 "crossDomain": true,
 "url": url,
 "method": "GET"
}

$.ajax(settings).done(function (response) {
console.log(response);

console.log(response.awsaccount);
var $row = $('<div class="count" id="awsaccountvalue" style="color: #337ab7;">'+response.awsaccount+'</div>')
$('#awsaccountvalue').append($row);
var $row = $('<div class="count" id="containersvalue" style="color: #337ab7;">'+response.containers+'</div>')
$('#containersvalue').append($row);
var $row = $('<div class="count" id="dockerswarmsvalue" style="color: #337ab7;">'+response.dockerswarms+'</div>')
$('#dockerswarmsvalue').append($row);
var $row = $('<div class="count" id="servicesvalue" style="color: #337ab7;">'+response.services+'</div>')
$('#servicesvalue').append($row);

            });




  function autoRefresh1()
  {
  	  window.location.reload();
  }
 var dashboard_data = {{swarm_dict| tojson | safe}};
 $.each(dashboard_data, function (key, value) {
    // APPEND OR INSERT DATA TO SELECT ELEMENT.
    $('#down').append('<option value="' + value + '">' + key + '</option>');
  });


  $('#down').change(function () {
    console.log(this.options[this.selectedIndex].value);
    file_src = this.options[this.selectedIndex].value;

    $('<iframe> scrolling="no"')
      .attr('src', file_src)
      .appendTo('#iframe_div');

  });
  });