$(->
  v_login = new Vue
    el:'#v_login'
    data:
      error_info:false
      loading:false
    methods:
      submit:->
        data = @$data
  
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
      check:->
        if @user_name == '' or @user_name == undefined
          throw new Error("请输入用户名")
        if @password == '' or @password == undefined
          throw new Error("请输入用密码")
      post:(type)->
        if type == 'login'
          parm = JSON.stringify
            user_name:@user_name
            password:@password
            type:type
        else if type == 'signup'
          parm = JSON.stringify
            user_name:@user_name
            password:@password
            email:@email
            type:type
            type:'signup'
        @loading=true
        $.post '/login', parm ,(result, done)=>
          @loading=false
          if result.error != '0'
            #后台说这个用户没有时,提示用户创建
            if result.error == 'user not exist' and type =='login'
              $('#confirm-ask-create').modal()
              return
            @error_info = result.error
          else if result.error == undefined
            @error_info = '未知错误'
          else
            location.pathname = '/'
      createUserByModal:->
        $('#go_signup').tab('show')
      login:->
        @error_info = false
        @check()
        @post('login')
      signup:->
        @check()
        if @password != @repassword
          @error_info = '两次密码不一致'
          return
        if @email == '' or @email == undefined
          @error_info = '请输入邮箱'
          return
        @post('signup')

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
            data.loading = false
            if result.error != '' && result.error != undefined
              if result.error == 0
                data.error_info = '您输入的邮箱不存在，请重试'
              else
                data.error_info = '系统错误，请联系管理员'
            else
              data.error_info = '确认邮件已发送到您的邮箱中，请查收并设置新密码'

        return

      setPassword:->
        data = @$data
        if data.password_set != data.repassword_set
          data.error_info = '两次输入的密码不一致'
          return
        data.loading = true
        $.post '/login',
          JSON.stringify
            token:hash[1]
            password:data.password_set
            type:'setPassword'
        ,(result, done)->
          data.loading = false
          if result.error != '' && result.error != undefined
            data.error_info = '您的链接已失效，请重新获取邮件'
          else
            data.error_info = '设置成功，请重新登录'


      cleanError:->
        @$data.error_info = false

  window.bz.setOnErrorVm(v_login)


  hash = window.bz.getHashParms()
  if hash[0] == "#token"
    $ '#tab a'
      .tab('show')
)
