function updateDataTableSelectAllCtrl(table) {
  var $table = table.table().node();
  var $chkbox_all = $('tbody input[type="checkbox"]', $table);
  var $chkbox_checked = $('tbody input[type="checkbox"]:checked', $table);
  var chkbox_select_all = $('thead input[name="select_all"]', $table).get(0);

  // If none of the checkboxes are checked
  if ($chkbox_checked.length === 0) {
    chkbox_select_all.checked = false;
    if ('indeterminate' in chkbox_select_all) {
      chkbox_select_all.indeterminate = false;
    }

    // If all of the checkboxes are checked
  } else if ($chkbox_checked.length === $chkbox_all.length) {
    chkbox_select_all.checked = true;
    if ('indeterminate' in chkbox_select_all) {
      chkbox_select_all.indeterminate = false;
    }

    // If some of the checkboxes are checked
  } else {
    chkbox_select_all.checked = true;
    if ('indeterminate' in chkbox_select_all) {
      chkbox_select_all.indeterminate = true;
    }
  }
}


$(document).ready(function () {
  var rows_selected = [];

  var dbdata = {{dbdata | tojson | safe}};
  console.log(dbdata);
  var dbcolumns = {{dbcolumns | tojson | safe}};
  var table = $('#swarm').DataTable({
    "bDestroy": true,
    "deferRender": true,
    data: dbdata,
    columns: dbcolumns,
    'columnDefs': [{
      'targets': 1,
      'searchable': false,
      'orderable': false,
      'className': 'dt-body-center'

    }],


    select: {
      style: 'single',
      selector: 'td:first-child',

    },

    'order': [1, 'asc'],
    'rowCallback': function (row, data, dataIndex) {
      // Get row ID
      var rowId = data[0];

      // If row ID is in the list of selected row IDs
      if ($.inArray(rowId, rows_selected) !== -1) {
        $(row).find('input[type="checkbox"]').prop('checked', true);
        $(row).addClass('selected');
      }
    }
  });


  // Handle click on checkbox
  $('#swarm tbody').on('click', 'input[type="checkbox"]', function (e) {
    var $row = $(this).closest('tr');

    // Get row data
    var data = table.row($row).data();

    // Get row ID
    var rowId = data[0];

    // Determine whether row ID is in the list of selected row IDs
    var index = $.inArray(rowId, rows_selected);

    // If checkbox is checked and row ID is not in list of selected row IDs
    if (this.checked && index === -1) {
      rows_selected.push(rowId);

      // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
    } else if (!this.checked && index !== -1) {
      rows_selected.splice(index, 1);
    }

    if (this.checked) {
      $row.addClass('selected');
    } else {
      $row.removeClass('selected');
    }

    // Update state of "Select all" control
    updateDataTableSelectAllCtrl(table);

    // Prevent click event from propagating to parent
    e.stopPropagation();
  });

  // Handle click on table cells with checkboxes
  $('#swarm').on('click', 'tbody td, thead th:first-child', function (e) {
    $(this).parent().find('input[type="checkbox"]').trigger('click');
  });

  // Handle click on "Select all" control
  $('thead input[name="select_all"]', table.table().container()).on('click', function (e) {
    if (this.checked) {
      $('#example tbody input[type="checkbox"]:not(:checked)').trigger('click');
    } else {
      $('#example tbody input[type="checkbox"]:checked').trigger('click');
    }

    // Prevent click event from propagating to parent
    e.stopPropagation();
  });


  var array = [];
  $("#swarm tbody tr").click(function (e) {
    if ($(this).hasClass('row_selected')) {
      $(this).removeClass('row_selected');
    } else {
      table.$('tr.row_selected') //.removeClass('row_selected');
      $(this).addClass('row_selected');
    }

    $('#openSwal').click(function (e) {
      var ids = $.map(table.rows('.selected').data(), function (item) {
        return item[2]
      });
      console.log(ids)

      //console.log(alert(table.rows('.selected').data()));

      var anSelected = fnGetSelected(table);
      $(anSelected).remove();
      var id = $(e.currentTarget).attr("id");
      save(id)
      SwalDelete(ids);
      e.preventDefault();

    });
  });

  function fnGetSelected(tableLocal) {
    return tableLocal.$('tr.row_selected');
  }

  function SwalDelete(ids) {
    swal({
      title: 'Are you sure?',
      text: "It will be deleted permanently!",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!',
      showLoaderOnConfirm: true,

      preConfirm: function () {
        return new Promise(function (resolve) {

          $.ajax({
            url: '/deletedockerswarm',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(ids),
          })
          type: 'success',
            swal('Deleted', 'Successfully');


        });
      },
      allowOutsideClick: false
    });

  }


  function save(id) {
    console.log(id);
  }

  $('#swarm tbody').on('click', 'button', function () {
    var heads = [];
    var data = table.row($(this).parents('tr')).data();
    heads.push(data[3]);
    //alert(heads);
    console.log(heads);
    $.ajax({
        url: "/swarminfo/" + heads,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(heads),
      })
      .done(function (data) {
        reload(heads);
      })
      .fail(function () {
        reload(heads);
      });

  });

  function reload(heads) {
    //$("#swarmtemp").load("/swarminfo/" + heads)
    {
      window.location = '/swarminfo/' + heads;
    }
  };
});
