$(->
    v_crud_check = new Vue
        el: '#v_crud_check'
        data:
            editable: false
            record: {}
            loading: false
            table_desc: ''
            test: 'test'

        created: ->
            @loadData()
        
        methods:
            getTableName:->
                parm = window.bz.getUrlParm()
                return parm[2]

            jump2List: ->
                path = '/crud_list/' + @getTableName()
                location.pathname = path
            
            save: ->
                data = @$data
                data.loading=true
                table_name = @getTableName()
                $.post('/crud_api',
                  JSON.stringify {table_name:table_name, record:data.record}
                ).done((result)->
                    if result.error!='0'
                        window.bz.showError5(result.error)
                    else if result.error == undefined
                        data.error_info = '未知错误'
                    else
                        window.bz.showSuccess5('审核成功...正在返回列表')
                )

            loadData: ->
                table_name = @getTableName()
                parm = window.bz.getHashParms()
                id = parm[0].replace('#','')
                parm = {table_name:table_name}
                if id!=''
                    parm.id = id

                $.post('/crud_check',
                  JSON.stringify parm
                ).done((result)->
                    if result.error!='0'
                        window.bz.showError5(result.error)
                    else
                        if result.data.length>0
                            record = result.data[0]
                            for field of record
                                if record[field] != null and typeof record[field] == "object"
                                    record[field] = JSON.stringify(record[field])
                            v_crud_check.$data.record = result.data[0]
                            v_crud_check.$data.record.id = id
                            console.log "record: ", v_crud_check.$data.record
                        else if id!=''
                            window.bz.showError5('未找到这条数据!')
                )
)
