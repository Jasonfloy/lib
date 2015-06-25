
$ ->
    input = '<input id="image-file" type="file" />'
    myCustomTemplates = image: (context) ->
      locale = context.locale
      options = context.options
      '
        <li>
            <span id="file-span" class="file-input btn btn-default btn-file glyphicon glyphicon-picture">
                <input id="image-file" type="file" />
            </span>
        </li>
      '
    $('#wysiwyg').html('Some text dynamically set.')



    selectFile = (e)->
        files = e.target.files
        for i of files
            if !isNaN(i)
                f = files[i]
                fd = new FormData
                fd.append 'file_' + i, f
                # 把文件放入到 all_files列表和 fd上传队列中
                new_file =
                    'file_type': 'file'
                    'file_name': f.name
                    'remove': false
                    'suffix': null
                    'fd': fd
        $.ajax(
            url: '/file_upload'
            type: 'POST'
            data: new_file.fd
            processData: false
            contentType: false).done (d) =>
                if d.error == '0'
                    editor = $('#wysiwyg').data("wysihtml5").editor

                    file_path = d.results[0].file_path
                    file_name = d.results[0].file_name
                    log d.results[0]
                    try
                        editor.composer.commands.exec("insertImage", { src: file_path, title: file_name, alt: file_name })
                        window.bz.showSuccess5 '文件上传成功'
                    catch error
                        log error
                        window.bz.showError5 '请在编辑器中点击要插入图片的位置'
                else
                    window.bz.showError5 '文件上传时发生错误:' + d.error
                $(this).remove()
                $('#image-file').change (selectFile)
                $(input).change(selectFile).appendTo($('#file-span'))
                return
    #window.bz.initWysiwyg()
    window.bz.initWysiwyg = (bind=null)->
        $('#wysiwyg').wysihtml5 (
            locale: 'zh-CN'
            customTemplates: myCustomTemplates
        )

        editor = $('#wysiwyg').data("wysihtml5").editor

        editor.on("change", ->
            log bind.record.content
            bind.record.content = $('#wysiwyg').val()
        )
        $('#image-file').change (selectFile)
