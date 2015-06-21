$(->
  v_login = new Vue
    el:'#v_login'
    data:
      error_info:false
      loading:false
    methods:
      check:->
        if @user_name in ['', undefined]
          throw new Error("请输入用户名")
        if @password in ['', undefined]
          throw new Error("请输入用密码")
      #通用的post,传入type
      post:(type)->
        if type == 'login'
          parm = JSON.stringify
            user_name:@user_name
            password:@password
            type:type
            #尝试取验证的数据
            geetest_challenge : $('.geetest_challenge').val()
            geetest_validate : $('.geetest_validate').val()
            geetest_seccode : $('.geetest_seccode').val()
            validate: $('#validate').val()
        else if type == 'signup'
          console.log window.regexp
          for key of window.regexp
            value = window.regexp[key]
            console.log value
            if value == false
              throw new Error("您的邮箱无法验证，请填写正确的邮箱。")
          parm = JSON.stringify
            user_name:@user_name
            user_type:@user_type
            password:@password
            email:@email
            type:type
        else if type == 'forget'
          parm = JSON.stringify
            email:@email
            type:type
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
        if @email in ['', undefined]
          @error_info = '请输入邮箱'
          return
        if @user_type is ''
          throw new Error("请选择用户类型")
        @post('signup')
      forget:->
        if @email in ['', undefined]
          @error_info = '请输入邮箱'
          return
        parm = JSON.stringify
          email:@email
          type:'forget'
        @loading=true
        $.post '/login', parm, (result, done)=>
          @loading=false
          if result.error != '0'
            @error_info = result.error
          else if result.error == undefined
            @error_info = '未知错误'
          else
            window.bz.showSuccess5('邮件已经发送,请查看你的邮箱来修改密码!')

      setPassword:->
        if @password_set != @repassword_set
          throw new Error("两次输入的密码不一致")
        @loading = true
        parm = JSON.stringify
          token:hash[1]
          password:@password_set
          type:'setPassword'
        $.post '/login', parm, (result, done)=>
          @loading = false
          if result.error != '0'
            throw new Error(result.error)
          else
            window.bz.showSuccess5('设置成功，请重新登录')

      cleanError:->
        @$data.error_info = false

  window.bz.setOnErrorVm(v_login)

  hash = window.bz.getHashParms()
  if hash[0] == "#token"
    $ '#tab a'
      .tab('show')
  url = window.bz.getUrlParm()
  if url[1] == "profile"
    $ '#tab a'
      .tab('show')
)
