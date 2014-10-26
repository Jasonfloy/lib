var data, login;

data = {};

data.uploading = false;

data.error_info = false;

data.button_name = '登录';

Vue.config({
  delimiters: ["[", "]"]
});

login = new Vue({
  el: '#login',
  data: data,
  methods: {
    submit: function(e) {
      data.error_info = false;
      if (data.user_name === '') {
        data.error_info = '请输入用户名';
        return;
      }
      if (data.password === '') {
        data.error_info = '请输入用密码';
        return;
      }
      data.disabled = 'disabled';
      data.button_name = '登录中...';
      return window.superagent.post('/login', {
        user_name: data.user_name,
        password: data.password
      }, function(error, res) {
        var result;
        data.disabled = '';
        data.uploading = false;
        data.button_name = '登录';
        result = JSON.parse(res.text);
        if (result.error !== '0') {
          return data.error_info = result.error;
        } else {
          return location.pathname = '/';
        }
      });
    }
  }
});
