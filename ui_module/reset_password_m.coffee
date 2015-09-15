$ ->
  v_reset_password = new Vue
    el:'#v_reset_password'
    created:->
      bz.setOnErrorVm(@)
      @token = bz.getLastParm()
    data:
      error_info:false
      loading:false

      password:''
      repassword:''
    methods:
      resetPassword:->
        if @password != @repassword
          throw new Error("两次输入的密码不一致")
        @loading = true
        parm = JSON.stringify
          token:@token
          password:@repassword
        $.ajax
          url: '/reset_password'
          type: 'POST'
          data : parm
          success: (data, status, response) =>
            @loading=false
            if data.error != '0'
              throw new Error(data.error)
            else
              bz.showSuccess5('重置密码成功, 请重新登录')
              bz.delay 5000, -> location.pathname = '/login'
          error: ->
      cleanError:->
        @$data.error_info = false

