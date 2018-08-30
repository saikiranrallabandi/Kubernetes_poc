$(document).ready(function () {
  funswarminfo();
  funmanagerinfo();
  funmanagerdetailsinfo();
  funworkerinfo();
  funwokerdetailsinfo();

});

function funswarminfo() {
  var swarmdata = {
    {
      swarmdata | tojson | safe
    }
  };
  var swarmcolumns = {
    {
      swarmcolumns | tojson | safe
    }
  };
  var table = $('#swarmdata').DataTable({
    data: swarmdata,
    columns: swarmcolumns,
  });

}

function funmanagerinfo() {
  var managerdata = {
    {
      managerdata | tojson | safe
    }
  };
  var managercolumns = {
    {
      managercolumns | tojson | safe
    }
  };
  var table = $('#managerdata').DataTable({
    data: managerdata,
    columns: managercolumns,
  });
}

function funmanagerdetailsinfo() {
  var managerdetailsdata = {
    {
      managerdetailsdata | tojson | safe
    }
  };
  var managerdetailcolumns = {
    {
      managerdetailcolumns | tojson | safe
    }
  };
  var table = $('#managerdetailsdata').DataTable({
    data: managerdetailsdata,
    columns: managerdetailcolumns,
  });
  $("#managerdetailsdata td:contains('active')").replaceWith('<td><button class="btn btn-warning btn-xs">active</button></td>');

}

function funworkerinfo() {
  var workerdata = {
    {
      workerdata | tojson | safe
    }
  };
  var workercolumns = {
    {
      workercolumns | tojson | safe
    }
  };
  var table = $('#workerdata').DataTable({
    data: workerdata,
    columns: workercolumns,
  });
}

function funwokerdetailsinfo() {
  var workerdetailsdata = {
    {
      workerdetailsdata | tojson | safe
    }
  };
  var workerdetailcolumns = {
    {
      workerdetailcolumns | tojson | safe
    }
  };
  var table = $('#workerdetailsdata').DataTable({
    data: workerdetailsdata,
    columns: workerdetailcolumns,
  });
  $("#workerdetailsdata td:contains('active')").replaceWith('<td><button class="btn btn-warning btn-xs">active</button></td>');
}