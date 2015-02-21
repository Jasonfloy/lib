v_login = new Vue
  el:'#v_login'
  data:
    error_info:false
  methods:
    submit:(e)->
      log 'bigzhu'
      data.error_info = false
      if @$data.user_name == '' or @$data.user_name == undefined
        @$data.error_info = '请输入用户名'
        return
      if @$data.password == '' or @$data.password == undefined
        @$data.error_info = '请输入用密码'
        return

      $.post '{{action_url}}',
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
