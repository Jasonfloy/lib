(function() {
  $(function() {
    var v_signup;
    return v_signup = new Vue({
      el: '#v_signup',
      data: {
        error_info: false,
        loading: false
      },
      methods: {
        submit: function(e) {
          var data;
          data = this.$data;
          data.error_info = false;
          if (data.user_name === '' || data.user_name === void 0) {
            data.error_info = '请输入用户名';
            return;
          }
          if (data.password === '' || data.password === void 0) {
            data.error_info = '请输入用密码';
            return;
          }
          data.loading = true;
          return $.post('{{action_url}}', JSON.stringify({
            user_name: data.user_name,
            password: data.password
          }), function(result, done) {
            data.loading = false;
            if (result.error !== '0') {
              return data.error_info = result.error;
            } else if (result.error === void 0) {
              return data.error_info = '未知错误';
            } else {
              return location.pathname = '/';
            }
          });
        },
        cleanError: function() {
          return this.$data.error_info = false;
        }
      }
    });
  });

}).call(this);
