$(document).ready(function () {
//heads = 'a2d745d-ebc2-4940-b8e2-567c1ac7732b'
heads = []
	var table = $('#example').DataTable({
	    "ajax": {
        "url": "api/swarminfo",
        "dataSrc": "objects",
        "headers": "Content-Type: application/json"
         },
		"columns": [
			{"data": "SWARM_NAME"},
			{
				"data": "SWARM_STATUS",
				targets: 1,
				render: function (data, type, row) {
					console.log(data);

					return '<span class="label label-success" style="font-size: 13px!important;color: #fff;position:relative;left:24px"' + (data[1] == 'active' ? 'danger' : 'success') + '">' + (data[1] == 'inactive' ? 'inactive' : 'active') + '</span>'
				}
			},
			{
				"data": "MANAGERDISKSIZE"
			},
			{
				"data": "CLUSTERSIZE"
			},
			{
				"data": "WORKERDISKTYPE"
			},
			{
				"data": "CREATION_DATE"
			},

			{
				"defaultContent": "<a href='' id='editButton' class='btn btn-default btn-warning Swarminfo'><i class='fa fa-eye-slash'>View</i></a><button class='btn btn-default btn-danger' data-toggle='modal' data-target='#myModal' id='deleteButton'><i class='fa fa-trash-o'></i></button>"

			},

		]
	});



$('#example').on('click', 'tbody .Swarminfo',function (e) {
e.preventDefault();
var data = table.row($(this).parents('tr')).data();
heads.push(data.SWARM_ID);
console.log(heads);
window.location = '/swarminfo/' + heads;
});



	$('#example').on('click', 'button', function (e) {
	e.preventDefault();

		var data = table.row($(this).parents('tr')).data();
		//alert(data.SWARM_NAME);
		console.log(data.SWARM_NAME);
		heads.push(data.SWARM_ID);
		console.log(heads);

		$.ajax({
			url: '/deletedockerswarm',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify(data.SWARM_ID),
			success: function () {
			   deleteswarm();
			}
		})
	});


    function deleteswarm () {
    $('#deleteswarm').click(function () {

    toastr.success("Swarm delete Successfully!",{"timeout":"0","extendedTImeout": "0","showCloseButton": "true"});
    });
};


});