$(->
  v_login = new Vue
    el:'#v_login'
    data:
      error_info:false
      loading:false
    methods:
      submit:(e)->
        data = @$data
        data.error_info = false
        if data.user_name == '' or data.user_name == undefined
          data.error_info = '请输入用户名'
          return
        if data.password == '' or data.password == undefined
          data.error_info = '请输入用密码'
          return
  
        data.loading=true
        $.post '/login',
          JSON.stringify
            user_name:data.user_name
            password:data.password
        ,(result, done)->
            data.loading=false
            if result.error!='0'
              data.error_info = result.error
            else if result.error == undefined
              data.error_info = '未知错误'
            else
              location.pathname = '/'
      cleanError:->
        @$data.error_info = false
)
