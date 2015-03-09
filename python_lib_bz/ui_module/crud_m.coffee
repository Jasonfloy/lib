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

                $.post '/crud_api',
                  JSON.stringify {table_name:table_name, record:data.record}
                ,(result, done)->
                    data.loading=false
                    if result.error!='0'
                        window.bz.showError5(result.error)
                    else if result.error == undefined
                        data.error_info = '未知错误'
                    else
                        window.bz.showSuccess5('成功提交')

                    #  location.pathname = '/'
                   
    table_name = v_crud.getTableName()
    parm = window.bz.getHashParms()
    id = parm[0].replace('#','')
    if id!=''
        id = parseInt(id)

        $.post '/crud',
          JSON.stringify {table_name:table_name, id:id}
        ,(result, done)->
            if result.error!='0'
                window.bz.showError5(result.error)
            else
                log result.data.length
                if result.data.length>0
                    v_crud.$data.record = result.data[0]
                    v_crud.$data.record.id = id
                else
                    window.bz.showError5('未找到这条数据!')
)
