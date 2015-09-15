(function() {
  $(function() {
    var v_forget;
    return v_forget = new Vue({
      el: '#v_forget',
      created: function() {
        return bz.setOnErrorVm(this);
      },
      data: {
        error_info: false,
        loading: false,
        email: ''
      },
      methods: {
        forget: function() {
          var key, parm, value;
          if (!this.email) {
            throw new Error("请输入邮箱");
          }
          this.loading = true;
          for (key in regexp) {
            value = regexp[key];
            if (value === false) {
              throw new Error("您的邮箱无法验证, 请填写正确的邮箱");
            }
          }
          parm = JSON.stringify({
            email: this.email
          });
          return $.ajax({
            url: '/forget',
            type: 'POST',
            data: parm,
            success: (function(_this) {
              return function(data, status, response) {
                _this.loading = false;
                if (data.error !== '0') {
                  throw new Error(data.error);
                } else {
                  bz.showSuccess5('找回密码成功,请登录你的邮箱继续修改密码');
                  return _this.email = '';
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
