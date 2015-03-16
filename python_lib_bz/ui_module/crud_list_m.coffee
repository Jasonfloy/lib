$(->
    v_crud_list = new Vue
        el: '#v_crud_list'
        data:
            list: []
            module: "normal"
            loading:true
            loading_target:"#v_crud_list",
            pagination:{
                resultCount: 101,
                showFL: true, 
                showFN: true,
                currPage: 1,
                showPageNum: 7,
                gotoPageFun: (currPage) ->
                    console.log(currPage)
                    
            }
        methods:
            detail: (event, record)->
                console.log record
                if record == "new"
                    window.location.href = "/crud/" + table_name
                    return
                if @module == 'normal'
                    window.location.href = "/crud/" + table_name + "#" + record.id
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

    table_name = window.bz.getUrlParm()[2]
    load = ->
        $.get('/crud_list_api/' + table_name)
            .done((d1)->
                v_crud_list.$data.loading=false
                if d1.error != "0"
                    window.bz.showError5(d1.error)
                    return
                d1.array.forEach((n)->
                    n.checked = false
                )
                v_crud_list.$set("list", d1.array)
            )
    load()
)
