$(document).ready(function (){
  var dbdata = {{dbdata | tojson | safe}};
  var dbcolumns = {{dbcolumns | tojson | safe}};
  var table = $('#image').DataTable({
    "bDestroy": true,
    "deferRender": true,
    data: dbdata,
    columns: dbcolumns,
  });
});