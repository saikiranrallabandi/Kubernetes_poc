$(document).ready(function() {
    awsconfig_id = []
    var _url = "api/aws";
    var table = $('#aws').DataTable({
        "ajax": {
            "url": _url,
            "dataSrc": "objects",
            "headers": "Content-Type: application/json",
        },
        "columns": [
            { "title": "AWSCONFIG_ID", "data": "AWSCONFIG_ID", },
            { "title": "AWS_ACCESS_KEY_ID", "data": "AWS_ACCESS_KEY_ID", },
            { "title": "AWS_REGION_NAME", "data": "AWS_REGION_NAME" },
            { "title": "AWS_ACCOUNT_ID", "data": "AWS_ACCOUNT_ID" },
            { "title": "CREATION_DATE", "data": "CREATION_DATE" },
            { "title": "Action", "defaultContent": "<a href='' id='editButton' class='btn btn-xs btn-info Awsinfo'>View</a><button class='btn btn-xs btn-danger' data-toggle='modal' data-target='#myModal' id='deleteButton'>Delete</button>" },
        ]
    });

    $('#aws').on('draw.dt', function(e) {
        $("#aws td:contains('Creation in Progress')").replaceWith('<td><span class="label label-danger" style="font-size: 10px!important;color: #fff;position:relative;left:7px" danger="">Creation in Progress</span></td>');
        $("#aws td:contains('active')").replaceWith('<td><span class="label label-success" style="font-size: 10px!important;color: #fff;position:relative;left:24px" danger="">active</span></td>');
    });



    $('#aws').on('click', 'tbody .Awsinfo', function(e) {
        e.preventDefault();
        var data = table.row($(this).parents('tr')).data();
        awsconfig_id.push(data.AWSCONFIG_ID);
        window.location = '/awsinfo/' + awsconfig_id;
    });

    $('#aws').on('click', 'button', function(e) {
        e.preventDefault();

        var data = table.row($(this).parents('tr')).data();
        console.log(data);

        $.ajax({
            url: '/deleteaws',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data.AWSCONFIG_ID),
            success: function(response) {
                deleteaws();
                console.log("SUCCESS: ", response);
            },
            error: function(error) {
                console.log("ERROR: ", error);
            }
        })
    });


    function deleteaws() {
        $('#deleteaws').click(function() {
            toastr.success("Aws delete Successfully!", {
                timeOut: 6000
            });
            reload();
        });
    };

    function reload() {
        window.location = '/aws';
    }

});