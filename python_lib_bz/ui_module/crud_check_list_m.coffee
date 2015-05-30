$(->

    selectPage = (currPage, beginIndex, endIndex, limit) ->
        if !limit
            limit = 10
        if !beginIndex
            beginIndex = 0

        table_name = window.bz.getUrlParm()[2]

        if v_crud_check_list
            v_crud_check_list.table_name = table_name
            audit_state = v_crud_check_list.audit_state

        $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex + '&audit_state=' + audit_state).done((data) ->
                if data.error == "0"
                    v_crud_check_list.records = data.records
                    v_crud_check_list.pagination.resultCount = data.count
                else
                    window.bz.showError5(data.error)
            )
            
   
    v_crud_check_list = new Vue
            el: '#v_crud_check_list'
            data:
                records: []
                table_name: ''
                audit_state: 'submit'
                audit_state_text: '待审核'
                options: [
                    {text: '待确认', value: 'submit'},
                    {text: '已确认', value: 'pass'}
                ]
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
                detail:(user_id, id) ->
                    #window.location.href = "/crud_check/" + @table_name + "#" + record_id
                    if @table_name == "agency_info"
                        window.location.href = "/" + @table_name + "#user_id=" + user_id
                    else
                        #window.location.href = "/" + @table_name + "_detail#id=" + id + "&user_id=" + user_id
                        window.location.href = "/" + @table_name + "_detail/" + id + "#user_id=" + user_id
                        
                checkedSelect:(e) ->
                    @audit_state_text = option.text for option in @options when option.value == @audit_state
                    selectPage()


)
