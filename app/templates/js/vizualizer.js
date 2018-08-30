$(document).ready(function () {
  var delay;
  var temp = {{SwarmDict | tojson | safe}};
  //console.log(temp);
  // EXTRACT JSON DATA.
  $.each(temp, function (key, value) {
    // APPEND OR INSERT DATA TO SELECT ELEMENT.
    $('#down').append('<option value="' + value + '">' + key + '</option>');
  });


  $('#down').change(function () {
    Swarlalert();
    console.log(this.options[this.selectedIndex].value);
    file_src = this.options[this.selectedIndex].value;
    $('<iframe>')
      .attr('src', file_src)
      .appendTo('#iframe_div');
  });


  $('.btn').on('click', function () {
    var $this = $(this);
    $this.button('loading');
    setTimeout(function () {
      $this.button('reset');
    }, 1000);
  });


});

function Swarlalert() {
  swal({
    position: 'top-end',
    type: 'success',
    title: 'Swarm vizualizer is creating',
    showConfirmButton: false,
    timer: 1000
  })
}