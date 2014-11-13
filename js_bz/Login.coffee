data = {}
data.uploading = false
data.error_info = false
data.button_name = '登录'

Vue.config({ delimiters: ["[", "]"] })
login = new Vue
  el:'#login'
  data:data
  methods:
    submit:(e)->
      data.error_info = false
      if data.user_name == ''
        data.error_info = '请输入用户名'
        return
      if data.password == ''
        data.error_info = '请输入用密码'
        return
      
      data.disabled = 'disabled'#避免重复点击
      data.button_name = '登录中...'

      window.superagent.post '/login', {user_name:data.user_name, password:data.password}, (error, res)->
        data.disabled = ''
        data.uploading = false
        data.button_name = '登录'
        result = JSON.parse(res.text)
        if result.error!='0'
          data.error_info = result.error
        else
          location.pathname = '/'
    cleanError:->
      data.error_info = false
