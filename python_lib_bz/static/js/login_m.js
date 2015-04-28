(function() {
  $(function() {
    var hash, v_login;
    v_login = new Vue({
      el: '#v_login',
      data: {
        error_info: false,
        loading: false
      },
      methods: {
        check: function() {
          if (this.user_name === '' || this.user_name === void 0) {
            throw new Error("请输入用户名");
          }
          if (this.password === '' || this.password === void 0) {
            throw new Error("请输入用密码");
          }
        },
        post: function(type) {
          var parm;
          if (type === 'login') {
            parm = JSON.stringify({
              user_name: this.user_name,
              password: this.password,
              type: type
            });
          } else if (type === 'signup') {
            parm = JSON.stringify({
              user_name: this.user_name,
              password: this.password,
              email: this.email,
              type: type
            });
          } else if (type === 'forget') {
            parm = JSON.stringify({
              email: this.email,
              type: type
            });
          }
          this.loading = true;
          return $.post('/login', parm, (function(_this) {
            return function(result, done) {
              _this.loading = false;
              if (result.error !== '0') {
                if (result.error === 'user not exist' && type === 'login') {
                  $('#confirm-ask-create').modal();
                  return;
                }
                return _this.error_info = result.error;
              } else if (result.error === void 0) {
                return _this.error_info = '未知错误';
              } else {
                return location.pathname = '/';
              }
            };
          })(this));
        },
        createUserByModal: function() {
          return $('#go_signup').tab('show');
        },
        login: function() {
          this.error_info = false;
          this.check();
          return this.post('login');
        },
        signup: function() {
          this.check();
          if (this.password !== this.repassword) {
            this.error_info = '两次密码不一致';
            return;
          }
          if (this.email === '' || this.email === void 0) {
            this.error_info = '请输入邮箱';
            return;
          }
          return this.post('signup');
        },
        forget: function() {
          var parm;
          if (this.email === '' || this.email === void 0) {
            this.error_info = '请输入邮箱';
            return;
          }
          parm = JSON.stringify({
            email: this.email,
            type: 'forget'
          });
          this.loading = true;
          return $.post('/login', parm, (function(_this) {
            return function(result, done) {
              _this.loading = false;
              if (result.error !== '0') {
                return _this.error_info = result.error;
              } else if (result.error === void 0) {
                return _this.error_info = '未知错误';
              } else {
                return window.bz.showSuccess5('邮件已经发送,请查看你的邮箱来修改密码!');
              }
            };
          })(this));
        },
        setPassword: function() {
          var data;
          data = this.$data;
          if (data.password_set !== data.repassword_set) {
            data.error_info = '两次输入的密码不一致';
            return;
          }
          data.loading = true;
          return $.post('/login', JSON.stringify({
            token: hash[1],
            password: data.password_set,
            type: 'setPassword'
          }), function(result, done) {
            data.loading = false;
            if (result.error !== '' && result.error !== void 0) {
              return data.error_info = '您的链接已失效，请重新获取邮件';
            } else {
              return data.error_info = '设置成功，请重新登录';
            }
          });
        },
        cleanError: function() {
          return this.$data.error_info = false;
        }
      }
    });
    window.bz.setOnErrorVm(v_login);
    hash = window.bz.getHashParms();
    if (hash[0] === "#token") {
      return $('#tab a').tab('show');
    }
  });

}).call(this);
