$(->
  v_login = new Vue
    el:'#v_login'
    data:
      error_info:false
      loading:false
    methods:
      check:->
        if @user_name == '' or @user_name == undefined
          throw new Error("请输入用户名")
        if @password == '' or @password == undefined
          throw new Error("请输入用密码")
      #通用的post,传入type
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
        if @email == '' or @email == undefined
          @error_info = '请输入邮箱'
          return
        @post('signup')
      forget:->
        if @email == '' or @email == undefined
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
