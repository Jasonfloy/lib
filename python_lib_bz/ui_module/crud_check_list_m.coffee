$(->

    selectPage = (currPage, beginIndex, endIndex, limit) ->
        if !limit
            limit = 10
        if !beginIndex
            beginIndex = 0

        table_name = window.bz.getUrlParm()[2]
        if v_crud_check_list
            v_crud_check_list.table_name = table_name

        $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex).done((data) ->
                if data.error == "0"
                    v_crud_check_list.records = data.records
                    v_crud_check_list.pagination.resultCount = data.count
                else
                    window.bz.showError5(d1.error)
            )
            
   
    v_crud_check_list = new Vue
            el: '#v_crud_check_list'
            data:
                records: []
                table_name: ''
                pagination:
                    showFL: true #是否显示第一页,最后一页
                    showFN: true #是否显示上一页,下一页
                    resultCount: 10 #总记录数,必须
                    pageCount: 20 #每页几行
                    currPage: 1 #当前第几页
                    showPageNum: 7 #显示几个页面按钮
                    gotoPageFun: selectPage
                    onInitedLoadCurrPageData: false

            methods:
                detail: (record_id)->
                    window.location.href = "/crud_check/" + @table_name + "#" + record_id

)
