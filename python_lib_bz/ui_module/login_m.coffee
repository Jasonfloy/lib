$(->
  v_login = new Vue
    el:'#v_login'
    data:
      error_info:false
      loading:false
    methods:
      submit:->
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
            email:data.email
            type:'login'
        ,(result, done)->
            data.loading=false
            if result.error!='0'
              data.error_info = result.error
            else if result.error == undefined
              data.error_info = '未知错误'
            else
              location.pathname = '/'
      signup:->
        data = @$data
        if data.password != data.repassword
          data.error_info = '两次密码不一致'
          return
        @submit()

      forget:->
        data = @$data
        if data.email == '' or data.email == undefined
          data.error_info = '请输入邮箱'
          return

        data.loading=true
        $.post '/login',
          JSON.stringify
            email:data.email
            type:'forget'
        ,(result, done)->
            data.loading=false
            console.log(result)

        return

      cleanError:->
        @$data.error_info = false
)
