$(document).ready(function() {
    var table = $('#myTable').DataTable();

    $('#myTable tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        var data = table.row( this ).data();

//        alert( 'You clicked on '+data[0]+'\'s row' );

    } );

    $('#button').click( function () {
        alert( table.rows('.selected').data().length +' row(s) selected' );
    } );
} );


$('[data-toggle="tooltip"]').tooltip();

