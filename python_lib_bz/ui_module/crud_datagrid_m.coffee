$(->
    vues = $(".safe-datagrid")
    for i in vues
        table_name = i.id
        new Vue
            el: '#'+i.id
            data:
                list: []
                module: "normal"
            created:->
                _this = @
                @table_name=table_name
                $.post('/crud_list_api/' + @table_name)
                    .done((d1)->
                        if d1.error != "0"
                            window.bz.showError5(d1.error)
                            return
                        d1.array.forEach((n)->
                            n.checked = false
                        )
                        _this.$set("list", d1.array)
                    )
            methods:
                detail: (event, index)->
                    if index == "new"
                        #window.location.href = "/crud/" + table_name
                        $('#modal-'+@table_name).modal()
                        return
                    record = @list[index]
                    if @module == 'normal'
                        window.location.href = "/crud/" + @table_name + "#" + record.id
                        return
                    else if record.checked
                        record.checked = false
                        $(event.target).siblings(".check-column").find("input[type=checkbox]").prop('checked', false)
                    else
                        record.checked = true
                        $(event.target).siblings(".check-column").find("input[type=checkbox]").prop('checked', true)
                moduleToggle: ->
                    if @module == 'edit'
                        @$set('module', 'normal')
                    else if @module == 'normal'
                        @$set('module', 'edit')
                del: ->
                    del_array = _.pluck(_.where(@list, {"checked": true}), "id")
                    $.ajax
                        url: '/crud_list_api/' + @table_name
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
