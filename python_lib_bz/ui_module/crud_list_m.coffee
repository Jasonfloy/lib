$(->
    table_name = window.bz.getUrlParm()[2]
    load = ->
        $.get('/crud_list_api/' + table_name)
            .done((d1)->
                if d1.error != "0"
                    window.bz.showError5(d1.error)
                    return
                d1.array.forEach((n)->
                    n.checked = false
                )
                v_crud_list.$set("list", d1.array)
            )

    v_crud_list = new Vue
        el: '#v_crud_list'
        data:
            list: []
            module: "normal"
        created:->
            load()
        methods:
            detail: (event, index)->
                if index == "new"
                    window.location.href = "#detail/new"
                    @$set("current_record", null)
                    return
                record = @list[index]
                if @module == 'normal'
                    window.location.href = "#detail/" + record.id
                    @$set("current_record", record)
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
                    url: '/crud_list_api/' + table_name
                    type: 'DELETE'
                    data:  del_array.join(",")
                .done((data)->
                    if data.error = "0"
                        load()
                    else
                        window.bz.showError5(data.error)
                )
                return
)