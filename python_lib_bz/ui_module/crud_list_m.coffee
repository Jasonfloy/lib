$(->
    find_parms=""
    table_name = window.bz.getUrlParm()[2]
    v_crud_list = {}
    count=0
    window.loadData =(value) ->
        find_parms=""
        if(value)
	        searchs=$(".form-search")	        
	        for s in searchs 
	        	if s.value
	        	    find_parms+=" and ("+s.name+")::text like '"+ s.value+"%' ";
	        	    
        $.post('/crud_list_api/' + table_name + '?queryCount=true',find_parms).done((data) ->
	        v_crud_list.$data.pagination.resultCount = data.count
        )
	    
        

                    
    load = (currPage, beginIndex, endIndex, limit) ->
        window.location.hash = currPage
        if v_crud_list.$data
            v_crud_list.$data.loading=true
        if(!limit)
            limit = 10
        if(!beginIndex)
            beginIndex = 1
        $.post('/crud_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex,
        		find_parms
        		).done((d1)->
                if d1.error != "0"
                    window.bz.showError5(d1.error)
                    return
                d1.array.forEach((n)->
                    n.checked = false
                )
                v_crud_list.$set("list", d1.array)
                v_crud_list.$data.loading=false
            )
            
    $.post('/crud_list_api/' + table_name + '?queryCount=true',find_parms).done((data) ->
        if(window.location.hash == '' || isNaN(window.location.hash.replace('#','')))
            window.location.hash = '1'
        _pageCount = 10 #每页显示10条记录
        _resultCount = data.count
        _currPageNo = parseInt(window.location.hash.replace('#',''))
        
        
        _endPage = parseInt(_resultCount/_pageCount)
        if(_resultCount%_pageCount > 0)
            _endPage = _endPage + 1
        if(_currPageNo > _endPage)
            window.location.hash = '1'
            _currPageNo = 1
        
                    
        
        v_crud_list = new Vue
            el: '#v_crud_list'
            data:
                list: []
                module: "normal"
                loading:true
                loading_target:"#v_crud_list"
                pagination: 
                    resultCount: _resultCount
                    showFL: true
                    showFN: true
                    pageCount: _pageCount
                    currPage: _currPageNo
                    showPageNum: 7
                    gotoPageFun: load
                    onInitedLoadCurrPageData: true
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
    )
    

)    

