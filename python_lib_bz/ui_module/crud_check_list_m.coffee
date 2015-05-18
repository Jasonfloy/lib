$(->

    selectPage = (currPage, beginIndex, endIndex, limit) ->
        if !limit
            limit = 10
        if !beginIndex
            beginIndex = 0

        table_name = window.bz.getUrlParm()[2]
        checked = 'submit'
        if v_crud_check_list
            v_crud_check_list.table_name = table_name
            checked = v_crud_check_list.checked

        $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex + '&checked=' + checked).done((data) ->
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
                checked: 'submit'
                checked_text: '待审核'
                options: [
                    {text: '待审核', value: 'submit'},
                    {text: '未通过', value: 'nopass'},
                    {text: '已通过', value: 'pass'}
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
                        window.location.href = "/" + @table_name + "_detail#id=" + id + "&user_id=" + user_id
                        
                checkedSelect:(e) ->
                    #@checked_text = $(e.target).find("option:selected").text()
                    @checked_text = option.text for option in @options when option.value == @checked
                    selectPage()


)
