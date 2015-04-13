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
          return this.loading = true;
        },
        submit: function(e) {
          var host, url;
          e.preventDefault();
          host = window.location.hostname;
          url = "https://www.google.com/search?q=site:" + host + " " + this.search + "&gws_rd=ssl";
          return window.open(url);
        }
      }
    });
  });

}).call(this);
