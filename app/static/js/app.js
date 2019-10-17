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

  // Init bootstrap-select

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

  var storage = {
    fetch: function(key) {
      return JSON.parse(localStorage.getItem(key)) || false;
    },

    delete: function(key) {
      if (this.fetch(key)) {
        localStorage.removeItem(key);
        return true;
      }
      return false;
    },

    clear: function() {
      localStorage.clear();
    },

    save: function(key, data) {
      localStorage.setItem(key, JSON.stringify(data));
      return true;
    }
  };

  $('.city').selectize({
    valueField: 'id',
    labelField: 'name',
    searchField: 'name',
    options: [],
    create: false,
    render: {
      item: function(item, escape) {
        return '<div>' + escape(item.name) + '</div>';
      },
      option: function(item, escape) {
        return '<div>' + escape(item.name) + '</div>';
      }
    },
    load: function(query, callback) {
      if (!query.length || query.length < 2) return callback();
      $.get('/cidades?search=' + query)
        .done(function(data) {
          callback(data.result);
        }).fail(function() {
          callback();
        });
    }
  });

  $('.address').selectize({
    valueField: 'id',
    labelField: 'name',
    searchField: 'name',
    preload: true,
    options: [],
    create: false,
    render: {
      item: function(item, escape) {
        return '<div>' + escape(item.name) + '</div>';
      },
      option: function(item, escape) {
        return '<div>' + escape(item.name) + '</div>';
      }
    },
    load: function(query, callback) {
      if (!query.length || query.length < 2) return callback();
      $.get('/enderecos?search=' + query)
        .done(function(data) {
          callback(data.result);
        }).fail(function() {
          callback();
        });
    },
    onItemAdd: function(value, $item) {
      // Get current loaded data, fill and disable the field
      var option = this.options[value].address,
        id = this.$input.attr('id').split('_id')[0];
      for (var opt in option) {
        var $field = $('#' + id + '-' + opt),
          val = option[opt];
        // If element is a selectize widget
        if ($field[0].hasOwnProperty('selectize')) {
          var select = $field[0].selectize,
            control = select.$wrapper.parent();
          select.addOption(val);
          select.setValue(val.id);
          select.disable();
          control.find('.invalid-feedback').hide();
        } else {
          $field.val(val)
            .trigger('change')
            .prop('disabled', true);
        }
      }
    },
    onChange: function (value) {
      if (!value) {
        var self = this,
          option = this.options[1].address,
          id = this.$input.attr('id').split('_id')[0];
        for (var opt in option) {
          var $field = $('#' + id + '-' + opt);
          if ($field[0].hasOwnProperty('selectize')) {
            var select = $field[0].selectize;
            select.clear();
            select.clearOptions();
            select.enable();
          } else {
            $field.val('')
              .trigger('change')
              .prop('disabled', false);
          }
        }
      } else {
        var control = $(this.$wrapper).parent();
        if (control.hasClass('has-error')) {
          control.find('.invalid-feedback').hide();
          control.removeClass('has-error');
        }
      }
    }
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
      if (this.checkValidity && !this.checkValidity()) {
        var invalid = $(this).find(':invalid')
          .first()
          .focus()[0]
          .scrollIntoView();
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
