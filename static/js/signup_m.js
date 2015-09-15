(function() {
  $(function() {
    var v_signup;
    return v_signup = new Vue({
      el: '#v_signup',
      created: function() {
        return bz.setOnErrorVm(this);
      },
      data: {
        error_info: false,
        loading: false,
        user_name: '',
        email: '',
        password: '',
        repassword: ''
      },
      methods: {
        signup: function() {
          var key, parm, value;
          if (!this.user_name) {
            throw new Error("请输入用户名");
          }
          if (!this.password) {
            throw new Error("请输入用密码");
          }
          if (this.password !== this.repassword) {
            throw new Error("两次密码不一致");
          }
          if (!this.email) {
            throw new Error("请输入邮箱");
          }
          for (key in regexp) {
            value = regexp[key];
            if (value === false) {
              throw new Error("您的邮箱无法验证, 请填写正确的邮箱");
            }
          }
          parm = JSON.stringify({
            user_name: this.user_name,
            user_type: this.user_type,
            password: this.password,
            email: this.email
          });
          this.loading = true;
          return $.ajax({
            url: '/signup',
            type: 'POST',
            data: parm,
            success: (function(_this) {
              return function(data, status, response) {
                if (data.error !== '0') {
                  throw new Error(data.error);
                } else {
                  bz.showSuccess5('注册成功, 正在自动登录');
                  bz.delay(1500, function() {
                    return location.pathname = '/';
                  });
                }
                return _this.loading = false;
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
