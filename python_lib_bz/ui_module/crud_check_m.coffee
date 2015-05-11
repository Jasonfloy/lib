$(->
    v_crud_check = new Vue
        el: '#v_crud_check'
        data:
            editable: false
            record: {}
            loading: false

        created: ->
            @loadData()
        
        methods:
            getTableName:->
                parm = window.bz.getUrlParm()
                console.log "parm: ", parm
                return parm[2]

            jump2List: ->
                path = '/crud_check_list/' + @getTableName()
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
                _this = @
                table_name = @getTableName()
                parm = window.bz.getHashParms()
                id = parm[0].replace('#','')

                $.post('/crud_check', JSON.stringify({'table_name': table_name, 'id': id})).done((result)->
                    console.log result
                    if result.error != '0'
                        window.bz.showError5(result.error)
                    else
                        if result.data.length > 0
                            record = result.data[0]
                            for field of record
                                if record[field] != null and typeof record[field] == "object"
                                    record[field] = JSON.stringify(record[field])
                            _this.record = record

                        else if id != ''
                            window.bz.showError5('未找到这条数据!')
                    console.log "record:", _this.record
                )
)
