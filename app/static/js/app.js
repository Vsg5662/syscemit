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
	// init bootstrap-material-design
	$('body').bootstrapMaterialDesign();

	// delete entity
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
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
      	console.log(event);
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
	});
});