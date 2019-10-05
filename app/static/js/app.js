$(document).ready(function() {
  // Init bootstrap-material-design
  $('body').bootstrapMaterialDesign();

  // Delete a entity and reload the page
  $('.delete').on('click', function() {
    var url = $(this).data('action');
    $('.modal-delete').modal('toggle');
    $('.modal-delete').on('shown.bs.modal', function() {
      $('.btn-yes').on('click', function() {
        $.post(url)
          .done(function(resp) {
            window.location.href = window.location.origin + window.location.pathname;
          });
      });
    });
  });

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  // Loop over them and prevent submission
  $('.needs-validation').each(function() {
    var form = $(this)[0];
    $(this).on('submit', function(event) {
      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }
      $(this).addClass('was-validated');
    });
  });
});
