(function() {
  Vue.directive('btn-loading', function(value) {
    var el;
    el = $(this.el);
    if (!!value) {
      el.children().hide();
      return el.prepend("<i class='fa fa-spin fa-spinner'></i>");
    } else {
      el.children(".fa.fa-spin.fa-spinner").remove();
      return el.children().show();
    }
  });

}).call(this);
