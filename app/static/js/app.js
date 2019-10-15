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

  /*  var selects = $('select > option:first-child');
  if (selects.length > 0) {
    selects.each(function() {
      if ($(this).attr('value') == 0) {
        $(this).attr('disabled', true);
        $(this).attr('selected', true);
      }
    });
  }*/

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

  $('.city').selectize({
    valueField: 'id',
    labelField: 'name',
    searchField: 'name',
    options: [],
    create: false,
    render: {
      item: function(item, escape) {
        if (item.state) {
          return '<div>' + escape(item.name) + ' - ' + escape(item.state) + '</div>';
        } else {
          return '<div>' + escape(item.name) + '</div>';
        }
      },
      option: function(item, escape) {
        if (item.state) {
          return '<div>' + escape(item.name) + ' - ' + escape(item.state) + '</div>';
        } else {
          return '<div>' + escape(item.name) + '</div>';
        }
      }
    },
    load: function(query, callback) {
      if (!query.length) return callback();
      $.getJSON('/cidades/?search=' + query)
        .done(function(data) {
          callback(data.cities);
        }).fail(function() {
          callback();
        });
    },
    /*onChange: function (value) {
      var control = $(this.$wrapper).parent();
      if (control.hasClass('has-error')) {
        control.find('.help-block').hide();
        control.removeClass('has-error');
      }
    }*/
  });

  // Input field masks
  $('.cep').inputmask({
    'mask': '99999-999',
    'clearIncomplete': true
  });

  $('.date').inputmask({
    'alias': 'datetime',
    'clearIncomplete': true,
    'displayFormat': true,
    'inputFormat': 'dd/mm/yyyy',
    'jitMasking': true
  });

  $('.datetime').inputmask({
    'alias': 'datetime',
    'clearIncomplete': true,
    'displayFormat': true,
    'inputFormat': 'dd/mm/yyyy HH:MM[:ss]',
    'jitMasking': true
  });

  $('.number').inputmask({'regex': "\\d*"});

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
