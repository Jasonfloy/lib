$ ->
    Vue.directive('model-checkbox',
        twoWay: true
        bind:(value) ->
            @checkboxChange = (->
                if @el.checked
                    dataKeys = @raw.split(".")
                    dataContainer = @vm.$data
                    i = 0
                    for dataKey in dataKeys
                        if !dataContainer[dataKey] && (i + 1) != dataKeys.length
                            dataContainer[dataKey] = {}
                        if (i + 1) != dataKeys.length
                            dataContainer = dataContainer[dataKey]
                        i++
                    if dataContainer[dataKeys[dataKeys.length - 1]]
                        dataContainer[dataKeys[dataKeys.length - 1]] = dataContainer[dataKeys[dataKeys.length - 1]] + "," + @el.value
                    else
                        dataContainer[dataKeys[dataKeys.length - 1]] = @el.value
                else
                    dataKeys = @raw.split(".")
                    dataContainer = @vm.$data
                    i = 0
                    for dataKey in dataKeys
                        if (i + 1) != dataKeys.length
                            dataContainer = dataContainer[dataKey]
                        i++
                    _valuesStr = dataContainer[dataKeys[dataKeys.length - 1]]
                    if !_valuesStr
                        return
                    _values = _valuesStr.split(",")
                    _newValuesStr = ""
                    for _value in _values
                        if _value != @el.value
                            if _newValuesStr == ""
                                _newValuesStr = _value
                            else
                                _newValuesStr = _newValuesStr + "," + _value
                    dataContainer[dataKeys[dataKeys.length - 1]] = _newValuesStr
            ).bind(@)
            @el.addEventListener('change', @checkboxChange)
            @checkboxChange()
        update:(value) ->
            _checkedValues = @vm.$data.record.sex
            if _checkedValues && _checkedValues.indexOf(@el.value) != -1
                @el.checked = true
        unbind:() ->
            @el.removeEventListener('change', @checkboxChange)
    )
    
    v_crud = new Vue
        el: '#v_crud'
        data:
            editable: true
            record:{}
            loading:false
            oper:''
            table_desc:''
            files:[]
        watch:
            'record':->
                $('#wysiwyg').html(@record.content)
                window.bz.initWysiwyg(@)
        methods:
            toggleEdit:->
                if @$data.editable
                    @$data.editable = false
                else
                    @$data.editable = true
            getTableName:->
                parm = window.bz.getUrlParm()
                return parm[2]
            jump2List:->
                path = '/crud_list/' + @getTableName()
                location.pathname = path
            save:->
                data = @$data
                data.loading=true
                table_name = @getTableName()
                $.post('/crud_api',
                  JSON.stringify {table_name:table_name, record:data.record}
                ).done((result)->
                    if result.error!='0'
                        window.bz.showError5(result.error)
                        log result.error
                    else if result.error == undefined
                        data.error_info = '未知错误'
                    else if data.files.length > 0
                        uploadFile(data.files)
                    else
                        AllDone(result)
                )

    AllDone = (d)->
        v_crud.$set("loading", false)
        if d.error == "0"
            #delay 1500, -> v_crud.jump2List()
            window.bz.showSuccess5('提交成功...正在返回列表')
        else
            window.bz.showError5(d)

    uploadFile = (files)->
        files.forEach (file)->
            if file.temp.fd
                $.ajax
                    url: "/file_upload",
                    type:"POST",
                    data: file.temp.fd,
                    processData: false,
                    contentType: false
                .done (d)->
                    createFileRef(file, d)
            else
                $.post "/file_ref",
                    JSON.stringify 
                        "remove_files": file.temp.remove_files
                .done (d)->
                    createFileRef(file)

    createFileRef = (file, data)->
        if not file
            AllDone()
            return
        else if not data
            params =
                "remove_files": file.temp.remove_files
        else
            params =
                "column": file.column
                "append_files": data.results
                "remove_files": file.temp.remove_files
                "table_name": table_name
                "record_id": id
        $.post "/file_ref",
            JSON.stringify(params)
        .done(AllDone)

    table_name = v_crud.getTableName()
    parm = window.bz.getHashParms()
    id = parm[0].replace('#','')
    parm = {table_name:table_name}
    if id!=''
        v_crud.$data.oper='编辑'
        parm.id = id
    else
        v_crud.$data.oper='新增'

    $.post('/crud',
      JSON.stringify parm
    ).done((result)->
        if result.error!='0'
            window.bz.showError5(result.error)
        else
            v_crud.$data.table_desc = result.table_desc
            if result.data.length>0
                record = result.data[0]
                for field of record
                    if record[field] != null and typeof record[field] == "object"
                        record[field] = JSON.stringify(record[field])
                v_crud.$data.record = result.data[0]
                v_crud.$data.record.id = id
            else if id!=''
                window.bz.showError5('未找到这条数据!')
            # 生成数据交换属性, 并且打包到files中
            if result.all_files
                if result.all_files.length > 0
                    for f in result.all_files
                        v_crud.$set(f.column, {"fd": null, "all_files": f.files, "remove_files": []})
                        v_crud.$data.files.push({"column": f.column, "temp": v_crud.$data[f.column]})
    )

