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
          var ref, ref1;
          if ((ref = this.user_name) === '' || ref === (void 0)) {
            throw new Error("请输入用户名");
          }
          if ((ref1 = this.password) === '' || ref1 === (void 0)) {
            throw new Error("请输入用密码");
          }
        },
        post: function(type) {
          var parm;
          if (type === 'login') {
            parm = JSON.stringify({
              user_name: this.user_name,
              password: this.password,
              type: type,
              geetest_challenge: $('.geetest_challenge').val(),
              geetest_validate: $('.geetest_validate').val(),
              geetest_seccode: $('.geetest_seccode').val()
            });
          } else if (type === 'signup') {
            parm = JSON.stringify({
              user_name: this.user_name,
              user_type: this.user_type,
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
          var ref;
          this.check();
          if (this.password !== this.repassword) {
            this.error_info = '两次密码不一致';
            return;
          }
          if ((ref = this.email) === '' || ref === (void 0)) {
            this.error_info = '请输入邮箱';
            return;
          }
          if (this.user_type === '') {
            throw new Error("请选择用户类型");
          }
          return this.post('signup');
        },
        forget: function() {
          var parm, ref;
          if ((ref = this.email) === '' || ref === (void 0)) {
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
          var parm;
          if (this.password_set !== this.repassword_set) {
            throw new Error("两次输入的密码不一致");
          }
          this.loading = true;
          parm = JSON.stringify({
            token: hash[1],
            password: this.password_set,
            type: 'setPassword'
          });
          return $.post('/login', parm, (function(_this) {
            return function(result, done) {
              _this.loading = false;
              if (result.error !== '0') {
                throw new Error(result.error);
              } else {
                return window.bz.showSuccess5('设置成功，请重新登录');
              }
            };
          })(this));
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
