$(->
    v_crud = new Vue
        el: '#v_crud'
        data:
            editable: true
            record:{}
            loading:false
        methods:
            toggleEdit:->
                if @$data.editable
                    @$data.editable = false
                else
                    @$data.editable = true
            getTableName:->
                parm = window.bz.getUrlParm()
                return parm[2]
            save:->
                data = @$data
                data.loading=true

                table_name = @getTableName()

                $.post '/crud',
                  JSON.stringify {table_name:table_name, record:data.record}
                ,(result, done)->
                    data.loading=false
                    if result.error!='0'
                      data.error_info = result.error
                    else if result.error == undefined
                      data.error_info = '未知错误'
                    else
                        window.bz.showSuccess5('成功提交')

                    #  location.pathname = '/'
)
