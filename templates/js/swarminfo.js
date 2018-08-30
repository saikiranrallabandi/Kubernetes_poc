$(document).ready(function() {
    //var url = "/api"+document.location.pathname
    var pathArray = document.location.pathname.split( '/' );
    //alert(secondLevelLocation);

    var secondLevelLocation = pathArray[2];
    var swarmurl = "/api/" + 'swarminfo/'+secondLevelLocation;
    var managerurl = "/api/" + 'managerinfo/' + secondLevelLocation;
    var workerurl = "/api/" + 'workerinfo/' + secondLevelLocation;

    var table = $('#swarmdata').DataTable({
        "paging": false,
        "bInfo": false,
        "ajax": {
            "url": swarmurl,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [{
                "title": "SWARM_NAME",
                "data": "SWARM_NAME",
                //"fnCreatedCell": function(nTd, sData, oData, iRow, iCol) {
                 //   $(nTd).html("<a href='/nodes' style='text-decoration: underline;'" + "'>" + oData.SWARM_NAME + "</a>");
                //}

            },
            {
                "title": "SWARM_ID",
                "data": "SWARM_ID",
            },

            {
                "title": "CREATION_DATE",
                "data": "CREATION_DATE"
            },

        ]
    });



    var table = $('#managerdata').DataTable({
        "paging": false,
        "bInfo": false,
        "ajax": {
            "url": managerurl,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [{

                "title": "MANAGER_ID",
                "data": "MANAGER_ID",
                //"fnCreatedCell": function(nTd, sData, oData, iRow, iCol) {
                 //   $(nTd).html("<a href='/nodes' style='text-decoration: underline;'" + "'>" + oData.MANAGER_ID + "</a>");
                //}
            },
            {

                "title": "MANAGER_HOSTNAME",
                "data": "MANAGER_HOSTNAME",

            },
            {
                "title": "AVAILABILITY",
                "data": "AVAILABILITY",
            },

            {
                "title": "MANAGER_STATUS",
                "data": "MANAGER_STATUS",
            },

        ]
    });


    var table = $('#workerdata').DataTable({
        "paging": false,
        "bInfo": false,
        "ajax": {
            "url": workerurl,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [{

                "title": "WORKER_ID",
                "data": "WORKER_ID",
                //"fnCreatedCell": function(nTd, sData, oData, iRow, iCol) {
                 //   $(nTd).html("<a href='/nodes' style='text-decoration: underline;'" + "'>" + oData.WORKER_ID + "</a>");
                //}
            },
            {
                "title": "WORKER_HOSTNAME",
                "data": "WORKER_HOSTNAME"

            },
            {
                "title": "AVAILABILITY",
                "data": "AVAILABILITY",
            },

            {
                "title": "WORKER_STATUS",
                "data": "WORKER_STATUS"
            },

        ]
    });

details();
function details(){
var settings = {
 "async": true,
 "crossDomain": true,
 "url": swarmurl,
 "method": "GET"
}

$.ajax(settings).done(function (response) {
 console.log(response);

 for(var prop in response) {
   var item = response[prop];
   for (var key in item) {
   var $row = $('<h2>'+item[key]["SWARM_NAME"]+'</h2>');
}
$('#swarmname').append($row);

}
});
}


    $("#tempdiv1").one( "click", function(e) {

  //var div = '<div><p>Sai</p></div>'
  var div = '<rd-widget><div class="widget" style="max-width: 1500px;"><rd-widget-header icon="fa-object-group" title="Cluster visualizer"><div class="widget-header"><div class="row"><span ng-class="classes" class="pull-left"><i class="fa fa-object-group" ng-class="icon"></i> Cluster visualizer </span><span ng-class="classes" class="pull-right" ng-transclude=""></span><span ng-class="classes" class="pull-right" ng-transclude=""><div class="pull-right"><button type="button" class="btn btn-sm btn-primary" id="buttonLogin" ng-click="state.ShowInformationPanel = false;" ng-if="state.ShowInformationPanel">Hide</button></div></span></div></div></rd-widget-header><rd-widget-body><div class="widget-body" ng-class="classes"><rd-loading ng-show="loading" class="ng-hide"></rd-loading><div ng-hide="loading" class="widget-content" ng-transclude=""><div class="visualizer_container"><div class="node" ng-repeat="node in visualizerData.nodes track by $index"><div class="node_info"><div><div><b>DEV</b><span class="node_platform"><i class="fa fa-linux" aria-hidden="true" ></i></span></div></div><div>manager</div><div>CPU: 4</div><div>Memory: 2.1 GB</div></div><div class="tasks"><div class="task task_running"><div class="service_name">sigmaxm</div><div>Image: sigmaxm/sigmaxm:latest</div><div>Status: running</div><div>Update: 2018-01-15 09:47:00</div></div></div> </div></div></div></div></rd-widget-body></div></rd-widget>'

  $("#tempdiv").append(div);


 $('#buttonLogin').click(function(){
 $("#tempdiv").hide(1000);
});

$('#tempdiv1').click(function(){
 $("#tempdiv").show(1000);
});

});

});