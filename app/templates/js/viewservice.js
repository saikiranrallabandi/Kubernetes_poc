$(document).ready(function() {
    service_id = []
    var table = $('#service').DataTable({
        "ajax": {
            "url": "api/serviceinfo",
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [
           {
                "title": "SERVICE_NAME",
                "data": "SERVICE_NAME"
            },
            {
                "title": "SERVICE_ID",
                "data": "SERVICE_ID",
            },
            {
                "title": "IMAGE_ID",
                "data": "IMAGE_ID"
            },
            {
                "title": "REPLICAS",
                "data": "REPLICAS"
            },
            {
                "title": "HOSTPORT",
                "data": "HOSTPORT"
            },
            {
                "title": "CREATION_DATE",
                "data": "CREATION_DATE"
            },

            {
                "title": "Action",
                "defaultContent": "<a href='' id='editButton' class='btn btn-xs btn-info Serviceinfo'>View</a><button class='btn btn-xs btn-danger' data-toggle='modal' data-target='#myModal' id='deleteButton'>Delete</button>"

            },

        ]
    });

    $('#service').on('draw.dt', function(e) {
        $("#service td:contains('Creation in Progress')").replaceWith('<td><span class="label label-danger" style="font-size: 10px!important;color: #fff;position:relative;left:7px" danger="">Creation in Progress</span></td>');
        $("#service td:contains('active')").replaceWith('<td><span class="label label-success" style="font-size: 10px!important;color: #fff;position:relative;left:24px" danger="">active</span></td>');
    });



    $('#service').on('click', 'tbody .Serviceinfo', function(e) {
        e.preventDefault();
        var data = table.row($(this).parents('tr')).data();
        service_id.push(data.SERVICE_ID);
        console.log(service_id);
        window.location = '/serviceinfo/' + service_id;
    });



    $('#service').on('click', 'button', function(e) {
        e.preventDefault();

        var data = table.row($(this).parents('tr')).data();
        console.log(data);

        $.ajax({
            url: '/deleteservice',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data.SERVICE_ID),
            success: function(response) {
                deleteservice();
                console.log("SUCCESS: ", response);
            },
            error: function(error) {
                console.log("ERROR: ", error);
            }
        })
    });


    function deleteservice() {
        $('#deleteservice').click(function() {
            toastr.success("Service delete Successfully!", {
                timeOut: 6000
            });
            reload();
        });
    };

    function reload() {
        window.location = '/viewservice';
    }

});