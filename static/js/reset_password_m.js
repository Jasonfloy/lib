(function() {
  $(function() {
    var v_reset_password;
    return v_reset_password = new Vue({
      el: '#v_reset_password',
      created: function() {
        bz.setOnErrorVm(this);
        return this.token = bz.getLastParm();
      },
      data: {
        error_info: false,
        loading: false,
        password: '',
        repassword: ''
      },
      methods: {
        resetPassword: function() {
          var parm;
          if (this.password !== this.repassword) {
            throw new Error("两次输入的密码不一致");
          }
          this.loading = true;
          parm = JSON.stringify({
            token: this.token,
            password: this.repassword
          });
          return $.ajax({
            url: '/reset_password',
            type: 'POST',
            data: parm,
            success: (function(_this) {
              return function(data, status, response) {
                _this.loading = false;
                if (data.error !== '0') {
                  throw new Error(data.error);
                } else {
                  bz.showSuccess5('重置密码成功, 请重新登录');
                  return bz.delay(5000, function() {
                    return location.pathname = '/login';
                  });
                }
              };
            })(this),
            error: function() {}
          });
        },
        cleanError: function() {
          return this.$data.error_info = false;
        }
      }
    });
  });

}).call(this);
