$(document).ready(function() {
    swarm_id = []
    var _url = "api/viewdockerswarm";
    var table = $('#swarm').DataTable({
        "ajax": {
            "url": _url,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [
            { "title": "SWARM_NAME", "data": "SWARM_NAME", },
            { "title": "SWARM_STATUS", "data": "SWARM_STATUS", },
            { "title": "MANAGERDISKSIZE", "data": "MANAGERDISKSIZE" },
            { "title": "CLUSTERSIZE", "data": "CLUSTERSIZE" },
            { "title": "WORKERDISKTYPE", "data": "WORKERDISKTYPE" },
            { "title": "CREATION_DATE", "data": "CREATION_DATE" },
            { "title": "Action", "defaultContent": "<a href='' id='editButton' class='btn btn-xs btn-info Swarminfo'>View</a><button class='btn btn-xs btn-danger' data-toggle='modal' data-target='#myModal' id='deleteButton'>Delete</button>" },
        ]
    });

    $('#swarm').on('draw.dt', function(e) {
        $("#swarm td:contains('Creation in Progress')").replaceWith('<td><span class="label label-danger" style="font-size: 10px!important;color: #fff;position:relative;left:7px" danger="">Creation in Progress</span></td>');
        $("#swarm td:contains('active')").replaceWith('<td><span class="label label-success" style="font-size: 10px!important;color: #fff;position:relative;left:24px" danger="">active</span></td>');
    });



    $('#swarm').on('click', 'tbody .Swarminfo', function(e) {
        e.preventDefault();
        var data = table.row($(this).parents('tr')).data();
        swarm_id.push(data.SWARM_ID);
        console.log(swarm_id);
        window.location = '/swarminfo/' + swarm_id;
    });



    $('#swarm').on('click', 'button', function(e) {
        e.preventDefault();

        var data = table.row($(this).parents('tr')).data();
        console.log(data);
        //alert(data.SWARM_NAME);

        $.ajax({
            url: '/deletedockerswarm',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data.SWARM_ID),
            success: function(response) {
                deleteswarm();
                console.log("SUCCESS: ", response);
            },
            error: function(error) {
                //deleteswarm();
                console.log("ERROR: ", error);
            }
        })
    });


    function deleteswarm() {
        $('#deleteswarm').click(function() {
            toastr.success("Swarm delete Successfully!", {
                timeOut: 6000
            });
            reload();
        });
    };

    function reload() {
        window.location = '/viewdockerswarm';
    }

});