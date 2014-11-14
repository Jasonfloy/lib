Vue.config.delimiters = ['(%', '%)']
Vue.directive "show-bz",
  bind: (value) ->
    if value and value.length != 0
      $(@el).removeClass('hide_bz')
    else
      $(@el).addClass('hide_bz')
  update: (value) ->
    if value and value.length != 0
      $(@el).removeClass('hide_bz')
    else
      $(@el).addClass('hide_bz')

data = {}
data.uploading = false
data.error_info = false
data.button_name = '登录'

login = new Vue
  el:'#v_login'
  data:->
    data
  methods:
    submit:(e)->
      data.error_info = false
      if @$data.user_name == '' or @$data.user_name == undefined
        @$data.error_info = '请输入用户名'
        return
      if @$data.password == '' or @$data.password == undefined
        @$data.error_info = '请输入用密码'
        return

      $.post '/login',
        JSON.stringify
          user_name:data.user_name
          password:data.password
      ,(result, done)->
          if result.error!='0'
            data.error_info = result.error
          else if result.error == undefined
            data.error_info = '未知错误'
          else
            location.pathname = '/'
    cleanError:->
      data.error_info = false
