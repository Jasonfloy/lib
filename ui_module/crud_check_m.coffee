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
                return parm[2]

            jump2List: ->
                path = '/crud_check_list/' + @getTableName()
                location.pathname = path
            
            save:(checked) ->
                _this = @
                @loading = true
                table_name = @getTableName()
                record = {'id': @record.id, 'checked': checked}
                console.log "record: ", record
                $.post('/crud_api', JSON.stringify {table_name: table_name, record: record}).done((data)->
                    if data.error == '0'
                        window.bz.showSuccess5('审核成功...正在返回列表')
                        _this.loading = false
                        delay 2000, -> _this.jump2List()
                    else
                        window.bz.showError5(data.error)
                )

            loadData: ->
                _this = @
                table_name = @getTableName()
                parm = window.bz.getHashParms()
                id = parm[0].replace('#','')

                $.post('/crud_check', JSON.stringify({'table_name': table_name, 'id': id})).done((result)->
                    if result.error != '0'
                        window.bz.showError5(result.error)
                    else
                        if result.data.length > 0
                            record = result.data[0]
                            record.id = id
                            for field of record
                                if record[field] != null and typeof record[field] == "object"
                                    record[field] = JSON.stringify(record[field])
                            _this.record = record

                        else if id != ''
                            window.bz.showError5('未找到这条数据!')
                )
)
