$(document).ready(function() {
    var _url = "api/viewregistry";
    var table = $('#registry').DataTable({
        "ajax": {
            "url": _url,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [
            { "title": "REGISTRY_ID", "data": "REGISTRY_ID", },
            { "title": "REGISTRY_URL", "data": "REGISTRY_URL", },
            { "title": "REGISTRY_USERNAME", "data": "REGISTRY_USERNAME" },
            { "title": "Action", "defaultContent": "<button class='btn btn-xs btn-danger' data-toggle='modal' data-target='#myModal' id='deleteButton'>Delete</button>" },
        ]

    });

$('#registry').on('click', 'button', function(e) {
        e.preventDefault();

        var data = table.row($(this).parents('tr')).data();
        console.log(data);
        //alert(data.SWARM_NAME);

        $.ajax({
            url: '/deleteregistry',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data.REGISTRY_ID),
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
        $('#deleteregistry').click(function() {
            toastr.success("Registry deleted Successfully!", {
                timeOut: 6000
            });
            reload();
        });
    };

    function reload() {
        window.location = '/registry';
    }

});


