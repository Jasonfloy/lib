$(->
    table_name = window.bz.getUrlParm()[2]
    v_crud_list = {}
    count=0
    search_parms=[]
    _pageCount = 10 #每页显示10条记录
    _currPageNo = 1
    _onbeforeunloadCleanStorage = true
    
    window.onbeforeunload = (event) ->
        if _onbeforeunloadCleanStorage
            window.sessionStorage.clear()
            
    
    # 从sessionStorage中获取搜索条件并写入hash
    if window.sessionStorage
        storageData = window.sessionStorage.getItem("search_curd_list_" + table_name)
        if(storageData)
            window.location.hash = ""
            searchPams = storageData.split(";")
            if(searchPams[0] != "")
                for searchPam in searchPams
                    if(searchPam == "")
                        continue
                    searchKeyValue = searchPam.split("=")
                    if(searchKeyValue[0] == "" || searchKeyValue[1] == "")
                        continue
                    window.bz.setHashPram(searchKeyValue[0], searchKeyValue[1])
        
    # 从hash中获取搜索参数并写入到搜索框,并构建search_parms    
    _hashStrTemp = window.location.hash.replace('#','')
    if(_hashStrTemp)
        search_parms=[]
        _hashsTemp = _hashStrTemp.split(";")
        for _hashItemTemp in _hashsTemp
            if(_hashItemTemp == "")
                continue
            _hashTemp = _hashItemTemp.split("=")
            if(_hashTemp[0] == "" || _hashTemp[1] == "" || _hashTemp[0].indexOf("search_") == -1)
                continue
            if($("#" + _hashTemp[0]))
                $("#" + _hashTemp[0]).val(_hashTemp[1])
                objTemp = {"name": _hashTemp[0].replace("search_", ""), "value": _hashTemp[1]}
                search_parms.push(objTemp)

    # 判断hash中是否有当前页参数,如果没有则设为1
    if(!window.bz.getHashPram("p") || isNaN(window.bz.getHashPram("p")))
        window.bz.setHashPram("p","1")
    # 从hash中获取当前页
    _currPageNo = parseInt(window.bz.getHashPram("p"))
                     
    
    load = (currPage, beginIndex, endIndex, limit) ->
        #window.location.hash = currPage
        window.bz.setHashPram("p",currPage)
        if window.sessionStorage
            window.sessionStorage.setItem("search_curd_list_" + table_name, window.location.hash.replace("#","")) # window.location.hash.replace(/#p=\d*;/g,"")
        if v_crud_list.$data
            v_crud_list.$data.loading=true
        if(!limit)
            limit = 10
        if(!beginIndex)
            beginIndex = 1
        $.post('/crud_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex+'&find=true',
                JSON.stringify {table_name:table_name, search_parms:search_parms}
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
            
            
    Vue.directive('on-search',
        twoWay: true
        bind:(value) ->
            eventAndFun = @raw.split(":")
            @["search_fn_" + eventAndFun[0] + eventAndFun[1]] = (->
                @vm[eventAndFun[1]]()
            ).bind(@)
            if eventAndFun[0] == "enter"
                eventName = "onkeypress"
                _vue_this = @
                @el[eventName] = (event)->
                    if event && event.keyCode == 13
                        _vue_this["search_fn_" + eventAndFun[0] + eventAndFun[1]]()
            else
                eventName = "on" + eventAndFun[0]
                @el[eventName] = @["search_fn_" + eventAndFun[0] + eventAndFun[1]]
        update:(value) ->
        unbind:() ->
            eventNameKey = @raw.split(":")[0]
            eventName = "on" + eventNameKey
            @el[eventName] = undefined
    )
            
    
    v_crud_list = new Vue
            el: '#v_crud_list'
            data:
                list: []
                record:{}
                module: "normal"
                loading:true
                loading_target:"#v_crud_list"
                pagination: 
                    resultCount: 1
                    showFL: true
                    showFN: true
                    pageCount: _pageCount
                    currPage: _currPageNo
                    showPageNum: 7
                    gotoPageFun: load
                    onInitedLoadCurrPageData: false
            methods:
                detail: (event, record)->
                    console.log record
                    if record == "new"
                        window.location.href = "/crud/" + table_name
                        _onbeforeunloadCleanStorage = false
                        return
                    if @module == 'normal'
                        window.location.href = "/crud/" + table_name + "#" + record.id
                        _onbeforeunloadCleanStorage = false
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
                searchToggle: ->
                    $('.moreSearch').toggle()
                    $('#gridSearch').toggle()
                find:->
                    search_parms=[]        
                    i=0
                    searchs=$(".form-search")           
                    for s in searchs
                        if s.value
                            a={"name":s.name,"value": s.value}
                            window.bz.setHashPram("search_" + s.name, s.value)
                            search_parms[i]=a
                            i=i+1
                        else
                            window.bz.setHashPram("search_" + s.name, "")
                    $.post('/crud_list_api/'+table_name+ '?queryCount=true&find=true',
                           JSON.stringify {table_name:table_name, search_parms:search_parms}
                    ).done((data)->
                        v_crud_list.$data.pagination.resultCount = data.count
                    )
                       
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
                    
    $.post('/crud_list_api/' + table_name + '?queryCount=true&find=true',
        JSON.stringify {table_name:table_name, search_parms:search_parms}
    ).done((data) ->
        #if(window.location.hash == '' || isNaN(window.location.hash.replace('#','')))
        #    window.location.hash = '1'
        _resultCount = data.count
        _endPage = parseInt(_resultCount/_pageCount)
        if(_resultCount%_pageCount > 0)
            _endPage = _endPage + 1
        if(_currPageNo > _endPage)
            #window.location.hash = '1'
            window.bz.setHashPram("p","1")
            _currPageNo = 1
            v_crud_list.$data.pagination.currPage = _currPageNo
            
        v_crud_list.$data.pagination.resultCount = _resultCount
        

    )
)
