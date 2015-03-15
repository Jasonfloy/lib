$(->
    v_crud = new Vue
        el: '#v_crud'
        data:
            editable: true
            record:{}
            loading:false
            oper:''
            table_desc:''
            files:[]
        methods:
            toggleEdit:->
                if @$data.editable
                    @$data.editable = false
                else
                    @$data.editable = true
            getTableName:->
                parm = window.bz.getUrlParm()
                return parm[2]
            jump2List:->
                path = '/crud_list/' + @getTableName()
                location.pathname = path
            save:->
                data = @$data
                data.loading=true
                log data

                table_name = @getTableName()

                $.post('/crud_api',
                  JSON.stringify {table_name:table_name, record:data.record}
                ).done((result)->
                    data.loading=false
                    if result.error!='0'
                        window.bz.showError5(result.error)
                        log result.error
                    else if result.error == undefined
                        data.error_info = '未知错误'
                    else
                        for file in data.files
                            $.ajax
                                url: "/file_upload",
                                type:"POST",
                                data: file.temp.fd,
                                processData: false,
                                contentType: false
                            .done (d)->
                                for file_id of d.results
                                    $.post "/file_ref",
                                        JSON.stringify 
                                            "file_id":file_id,
                                            "table_name":parm.table_name,
                                            "column":file.column,
                                            "record_id": id
                                    .done (d)->
                                        if d.error == 0
                                            #delay 1500, -> v_crud.jump2List()
                                            window.bz.showSuccess5('提交成功...正在返回列表')
                                        else
                                            window.bz.showError5(d)
                )

    table_name = v_crud.getTableName()
    parm = window.bz.getHashParms()
    id = parm[0].replace('#','')
    parm = {table_name:table_name}
    if id!=''
        v_crud.$data.oper='编辑'
        parm.id = id
    else
        v_crud.$data.oper='新增'

    $.post('/crud',
      JSON.stringify parm
    ).done((result)->
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
            # 生成数据交换属性, 并且打包到files中
            if result.all_files.length > 0
                for f in result.all_files
                    v_crud.$set(f.column, {"fd": null, "all_files": f.files})
                    v_crud.$data.files.push({"column": f.column, "temp": v_crud.$data[f.column]})
    )
)
