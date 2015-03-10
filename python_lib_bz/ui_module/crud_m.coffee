$(->
    v_crud = new Vue
        el: '#v_crud'
        data:
            editable: true
            record:{}
            loading:false
            oper:''
            table_desc:''
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
    parm = {table_name:table_name}
    if id!=''
        v_crud.$data.oper='编辑'
        parm.id = id
    else
        v_crud.$data.oper='新增'

    $.post '/crud',
      JSON.stringify parm
    ,(result, done)->
        if result.error!='0'
            window.bz.showError5(result.error)
        else
            v_crud.$data.table_desc = result.table_desc
            if result.data.length>0
                record = result.data[0]
                for field of record
                    if record[field] != null and typeof record[field] == "object"
                        record[field] = JSON.stringify(record[field])
                v_crud.$data.record = result.data[0]
                v_crud.$data.record.id = id
            else if id!=''
                window.bz.showError5('未找到这条数据!')

)
