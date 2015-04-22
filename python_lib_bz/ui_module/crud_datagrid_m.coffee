$(->
    vues = $(".safe-datagrid")
    for i in vues
        table_name = i.id
        new Vue
            el: '#'+table_name
            data:
                list: []
                record:{}
                module: "normal"
                loading:true
                loading_target:"#"+table_name
            created:->
                _this = @
                @table_name = table_name
                $.post('/crud_list_api/' + @table_name)
                    .done((d1)->
                        if d1.error != "0"
                            window.bz.showError5(d1.error)
                            return
                        _this.$set("list", d1.array)
                        _this.loading=false
                    )
            methods:
                checkBox:->
                    checked_list = _.where(@list, {"checked": true})
                    if checked_list.length == 0
                        @module='normal'
                    else if checked_list.length == 1
                        @module='select_one'
                    else if checked_list.length > 1
                        @module='select_more'
                #查出表单内容,用于编辑
                getRecordDetail:(id)->
                    parm = {table_name:@table_name}
                    _this = @
                    if id!=''
                        parm.id = id
                    $.post('/crud',
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
                                _this.record = result.data[0]
                                _this.record.id = id
                            else if id!=''
                                window.bz.showError5('未找到这条数据!')
                    )

                edit:->
                    $('#modal-' + @table_name).modal()
                    id = _.where(@list, {"checked": true})[0].id
                    @getRecordDetail(id)
                new:->
                    @record={}
                    $('#modal-' + @table_name).modal()
                del: ->
                    del_array = _.pluck(_.where(@list, {"checked": true}), "id")
                    log del_array
                    log del_array.join(",")
                    #$.ajax
                    #    url: '/crud_list_api/' + table_name
                    #    type: 'DELETE'
                    #    data:  del_array.join(",")
                    #.done((data)->
                    #    if data.error = "0"
                    #        window.bz.showSuccess5("删除成功。")
                    #        load()
                    #    else
                    #        window.bz.showError5(data.error)
                    #)
                    #return

                moduleToggle: ->
                    if @module == 'edit'
                        @$set('module', 'normal')
                    else if @module == 'normal'
                        @$set('module', 'edit')
)
