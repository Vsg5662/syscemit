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

var app = {
  methods: {
    cancel: function() {
      window.history.back();
    },

    mask: function() {
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
        'inputFormat': 'dd/mm/yyyy HH:MM',
        'jitMasking': true
      });

      $('.number').inputmask({'regex': "\\d*"});
    },

    remove: function(button) {
      var url = $(button).data('action');
      $('.modal-delete').modal('toggle');
      $('.modal-delete').on('shown.bs.modal', function() {
        $('.btn-yes').on('click', function() {
          $.delete(url)
            .done(function(resp) {
              window.location.href = window.location.origin + window.location.pathname;
            });
        });
      });
    },

    search: function() {
      $('#search input, #search select').on('change', function() {
        var $form = $(this).parents('form'),
          field = $(this).attr('name'),
          value = $(this).val(),
          url = new URL(window.location.origin + window.location.pathname),
          params = new URLSearchParams($form.serialize());

        if (value.length) {
          params.set(field, value);
        }
        params.set('grid', 1);
        url.search = params.toString();
        $('#results').load(url.toString().concat(' #results tr'));
      });
    },

    selectors: function() {
      $('.address').selectize({
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
          },
        },
        load: function(query, callback) {
          if (!query.length || query.length < 2) return callback();
          $.get('/enderecos/?filters-street=' + query)
            .done(function(data) {
              callback(data.result);
            }).fail(function() {
              callback();
            });
        }
      });

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

      $('.doctor').selectize({
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
          $.get('/medicos?filters-name=' + query)
            .done(function(data) {
              callback(data.result);
            }).fail(function() {
              callback();
            });
        }
      });

      $('.filiation').selectize({
        delimiter: ',',
        persist: false,
        create: function(input) {
          return {
            value: input,
            text: input
          };
        },
        onFocus: function() {
          $(this.$input[0]).trigger('blur');
        },
        render: {
          option_create: function(item, escape) {
            console.log(item);
            return '<div>Adicionar ' + escape(item.input) + '</div>';
          }
        }
      });

      $('.grave').selectize({
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
          },
        },
        load: function(query, callback) {
          if (!query.length) return callback();
          $.get('/tumulos?filters-street=' + query)
            .done(function(data) {
              callback(data.result);
            }).fail(function() {
              callback();
            });
        }
      });

      $('.registry').selectize({
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
          },
        },
        load: function(query, callback) {
          if (!query.length || query.length < 2) return callback();
          $.get('/cartorios?filters-name=' + query)
            .done(function(data) {
              callback(data.result);
            }).fail(function() {
              callback();
            });
        }
      });

      $('.zone').selectize({
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
          $.get('/regioes?filters-description=' + query)
            .done(function(data) {
              callback(data.result);
            }).fail(function() {
              callback();
            });
        }
      });
    },

    submit: function() {
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
    }
  },

  init: function() {
    // Init bootstrap-material-design
    $('body').bootstrapMaterialDesign();
    $('input[autofocus]').focus();
    this.methods.search();
    this.methods.selectors();
    this.methods.mask();
    this.methods.submit();
  }
};

$(document).ready(function() {
  app.init();
});
