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
                @table_name=table_name
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
                moduleToggle: ->
                    if @module == 'edit'
                        @$set('module', 'normal')
                    else if @module == 'normal'
                        @$set('module', 'edit')
                searchToggle: ->
                    $('.moreSearch').toggle()
                    $('#gridSearch').toggle()
                del: ->
                    del_array = _.pluck(_.where(@list, {"checked": true}), "id")
                    log del_array
                    $.ajax
                        url: '/crud_list_api/' + table_name
                        type: 'DELETE'
                        data:  del_array.join(",")
                    .done((data)->
                        if data.error = "0"
                            window.bz.showSuccess5("删除成功。")
                            load()
                        else
                            window.bz.showError5(data.error)
                    )
                    return

)
