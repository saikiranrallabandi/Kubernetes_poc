$(document).ready(function() {
     var dbdata = {{dbdata|tojson|safe }};
     console.log(dbdata);
     var dbcolumns = {{dbcolumns|tojson|safe }};
     var table = $('#awsconfig').DataTable( {
        data: dbdata,
        columns:dbcolumns,
});
});
