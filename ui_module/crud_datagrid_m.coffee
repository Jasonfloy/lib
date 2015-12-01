$(->
    Vue.directive("datagrid-file-list", (value)->
        params = this.arg.split(".")
        if(params.length < 2)
            throw "file-list 指令中的参数不足，请检查是否指定表名与字段名."
        if(!$)
            throw "JQuery没有正确引用."
        table_name = params[0]
        column = params[1]
        parms_str = [table_name, column, value].join("/")
        ((_this, str)->
            $.get('/file_upload/' + str).done (d) ->
                html = ''
                if d.results.length == 0
                    return
                for i of d.results
                    f = d.results[i]
                    html += '<div><a href=\'' + f.file_path + '\'\' target=\'_blank\'>下载</a></div>'
                # 拼装字符串，注入到list中
                $(_this.el).html html
                return
        ) this, parms_str
    )

    vues = $(".safe-datagrid")
    for i in vues
        table_name = i.id
        #有user_id时候,是查看其他人的
        user_id = window.bz.getHashPram("user_id")
        user_id_edit = null
        if user_id
            ids = user_id.split("_")
            if ids.length > 1
                 user_id_edit = ids[0]
            else
                 user_id = ids[0]
        new Vue
            el: '#'+table_name
            data:
                list: []
                record:{}
                stat: "normal" # or look(查看) or check(审查)
                select: 'null' #选中的个数
                loading:true
                loading_target:"#"+table_name
                checked_list:{} #当前选中的list
                file_columns: []
            created:->
                @table_name = table_name
                @user_id = user_id
                @user_id_edit = user_id_edit
                @initStat()

                @loadListData()
                @getRecordDetail()  # 初始化的时候需要设置 file_columns 的参数
            watch:
                "record.id": ->
                    _this = @
                    _this.file_columns.forEach((column)->
                        _this.$[column.name + "_c"].getExistFiles()
                    )
            methods:
                look:(r)->
                    if @stat == 'normal'
                        @stat= "look"
                    $('#modal-' + @table_name).modal()
                    @getRecordDetail(r.id)
                #初始化 stat
                initStat:->
                    @select='null'
                    if @user_id and not user_id_edit
                        @stat = "check"
                    else
                        @stat = "normal"
                loadListData:->
                    _this = @
                    @initStat()
                    url = '/crud_list_api/' + @table_name
                    if @user_id and not user_id_edit
                        url += '?user_id=' + @user_id
                    else if @user_id_edit
                        url += '?user_id=' + @user_id_edit
                    else
                        url = url
                    $.post(url)
                    .done((d1)->
                        if d1.error != "0"
                            window.bz.showError5(d1.error)
                            return
                        _this.$set("list", d1.array)
                        _this.loading=false
                    )
                checkBox:->
                    @checked_list = _.where(@list, {"checked": true})
                    if @checked_list.length == 0
                        @select='null'
                    else if @checked_list.length == 1
                        @select='select_one'
                    else if @checked_list.length > 1
                        @select='select_more'
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
                            _this.$set("file_columns", result.file_columns)
                            if result.data.length > 0
                                record = result.data[0]
                                for field of record
                                    if record[field] != null and typeof record[field] == "object"
                                        record[field] = JSON.stringify(record[field])
                                _this.record = result.data[0]
                                _this.record.id = id
                            else if id != '' and typeof id != "undefined"
                                window.bz.showError5('未找到这条数据!')
                    )
                edit:(row) ->
                    @stat = "normal"
                    $('#modal-' + @table_name).modal()
                    @getRecordDetail(row.id)
                new:->
                    @stat = "normal"
                    new_record = {}
                    for key of @record
                        if key == 'id' then continue
                        new_record[key] = null
                    @$set("record", new_record)
                    $('#modal-' + @table_name).modal()

                confirm:(id) ->
                    $('#confirm-' + @table_name).modal()
                    @record.id = id

                del: ->
                    _this = @
                    $.ajax
                        url: '/crud_list_api/' + @table_name
                        type: 'DELETE'
                        data: @record.id.toString()
                    .done((data)->
                        if data.error == "0"
                            window.bz.showSuccess5("删除成功")
                            _this.initStat()
                            _this.loadListData()
                        else
                            window.bz.showError5(data.error)
                    )
                    return
                save:->
                    _this = @
                    @loading=true
                    if window.bz.isEmpty @record
                        window.bz.showError5('没有填写任何值!')
                        _this.loading=false
                        $('#modal-' + _this.table_name).modal('hide')
                        return
                    if _this.user_id_edit
                        _this.$set("record.user_id", _this.user_id_edit)
                    
                    $.post('/crud_api',
                        JSON.stringify {table_name:@table_name, record:@record}
                    ).done((result)->
                        _this.loading=false
                        $('#modal-' + _this.table_name).modal('hide')
                        if result.error!='0'
                            window.bz.showError5(result.error)
                        else if result.error == undefined
                            window.bz.showError5('未知错误')
                        else
                            _this.$set("record.id", result.id)
                            _this.file_columns.forEach((column)->
                                _this.$[column.name + "_c"].createFileRef(result.id)
                                _this.$[column.name + "_c"].clear()
                            )
                            window.bz.showSuccess5("操作成功")
                            _this.loadListData()
                    )
)
