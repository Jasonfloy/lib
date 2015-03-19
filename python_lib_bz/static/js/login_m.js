(function() {
  $(function() {
    var v_login;
    return v_login = new Vue({
      el: '#v_login',
      data: {
        error_info: false,
        loading: false
      },
      methods: {
        submit: function() {
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
          return $.post('/login', JSON.stringify({
            user_name: data.user_name,
            password: data.password,
            email: data.email,
            type: 'login'
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
        signup: function() {
          var data;
          data = this.$data;
          if (data.password !== data.repassword) {
            data.error_info = '两次密码不一致';
            return;
          }
          return this.submit();
        },
        forget: function() {
          var data;
          data = this.$data;
          if (data.email === '' || data.email === void 0) {
            data.error_info = '请输入邮箱';
            return;
          }
          data.loading = true;
          $.post('/login', JSON.stringify({
            email: data.email,
            type: 'forget'
          }), function(result, done) {
            data.loading = false;
            return console.log(result);
          });
        },
        cleanError: function() {
          return this.$data.error_info = false;
        }
      }
    });
  });

}).call(this);
