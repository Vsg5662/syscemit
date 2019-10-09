jQuery.each(["put", "delete"], function(i, method) {
  jQuery[method] = function(url, data, callback, type) {
    if (jQuery.isFunction(data)) {
      type = type || callback;
      callback = data;
      data = undefined;
    }

    return jQuery.ajax({
      url: url,
      type: method,
      dataType: type,
      data: data,
      success: callback
    });
  };
});

$(document).ready(function() {
  // Init bootstrap-material-design
  $('body').bootstrapMaterialDesign();

  // Cancel button returns to previous page
  $('.cancel').on('click', function() {
    window.history.back();
  });

  // Delete a entity and reload the page
  $('.delete').on('click', function() {
    var url = $(this).data('action');
    $('.modal-delete').modal('toggle');
    $('.modal-delete').on('shown.bs.modal', function() {
      $('.btn-yes').on('click', function() {
        $.delete(url)
          .done(function(resp) {
            window.location.href = window.location.origin + window.location.pathname;
          });
      });
    });
  });

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  // Loop over them and prevent submission
  $('.needs-validation').each(function() {
    var form = $(this)[0],
      url = $(this).attr('action') || window.location.pathname;
      method = $(this).data('method');
    $(this).on('submit', function(event) {
      event.preventDefault();
      if (form.checkValidity() === false) {
        event.stopPropagation();
      } else {
        var data = $(this).serialize();
        $[method](url, data, function(response) {
          if (response.redirect) {
            window.location.href = response.redirect;
          }
        });
      }
      $(this).addClass('was-validated');
    });
  });
});
