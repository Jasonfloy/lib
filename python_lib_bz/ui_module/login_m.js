var data, login;

Vue.config.delimiters = ['(%', '%)'];

Vue.directive("show-bz", {
  bind: function(value) {
    if (value && value.length !== 0) {
      return $(this.el).removeClass('hide_bz');
    } else {
      return $(this.el).addClass('hide_bz');
    }
  },
  update: function(value) {
    if (value && value.length !== 0) {
      return $(this.el).removeClass('hide_bz');
    } else {
      return $(this.el).addClass('hide_bz');
    }
  }
});

data = {};

data.uploading = false;

data.error_info = false;

data.button_name = '登录';

login = new Vue({
  el: '#v_login',
  data: function() {
    return data;
  },
  methods: {
    submit: function(e) {
      data.error_info = false;
      if (this.$data.user_name === '' || this.$data.user_name === void 0) {
        this.$data.error_info = '请输入用户名';
        return;
      }
      if (this.$data.password === '' || this.$data.password === void 0) {
        this.$data.error_info = '请输入用密码';
        return;
      }
      return $.post('{{action_url}}', JSON.stringify({
        user_name: data.user_name,
        password: data.password
      }), function(result, done) {
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
      return data.error_info = false;
    }
  }
});
