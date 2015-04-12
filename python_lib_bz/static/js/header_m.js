(function() {
  $(function() {
    var v_header_m;
    return v_header_m = new Vue({
      el: '#v_header_m',
      data: {
        loading: false
      },
      methods: {
        clickLink: function() {
          return this.$data.loading = true;
        }
      }
    });
  });

}).call(this);
