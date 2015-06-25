(function() {
  $(function() {
    var input, myCustomTemplates, selectFile;
    input = '<input id="image-file" type="file" />';
    myCustomTemplates = {
      image: function(context) {
        var locale, options;
        locale = context.locale;
        options = context.options;
        return '<li> <span id="file-span" class="file-input btn btn-default btn-file glyphicon glyphicon-picture"> <input id="image-file" type="file" /> </span> </li>';
      }
    };
    $('#wysiwyg').html('Some text dynamically set.');
    selectFile = function(e) {
      var f, fd, files, i, new_file;
      files = e.target.files;
      for (i in files) {
        if (!isNaN(i)) {
          f = files[i];
          fd = new FormData;
          fd.append('file_' + i, f);
          new_file = {
            'file_type': 'file',
            'file_name': f.name,
            'remove': false,
            'suffix': null,
            'fd': fd
          };
        }
      }
      return $.ajax({
        url: '/file_upload',
        type: 'POST',
        data: new_file.fd,
        processData: false,
        contentType: false
      }).done((function(_this) {
        return function(d) {
          var editor, error, file_name, file_path;
          if (d.error === '0') {
            editor = $('#wysiwyg').data("wysihtml5").editor;
            file_path = d.results[0].file_path;
            file_name = d.results[0].file_name;
            log(d.results[0]);
            try {
              editor.composer.commands.exec("insertImage", {
                src: file_path,
                title: file_name,
                alt: file_name
              });
              window.bz.showSuccess5('文件上传成功');
            } catch (_error) {
              error = _error;
              log(error);
              window.bz.showError5('请在编辑器中点击要插入图片的位置');
            }
          } else {
            window.bz.showError5('文件上传时发生错误:' + d.error);
          }
          $(_this).remove();
          $('#image-file').change(selectFile);
          $(input).change(selectFile).appendTo($('#file-span'));
        };
      })(this));
    };
    return window.bz.initWysiwyg = function(bind) {
      var editor;
      if (bind == null) {
        bind = null;
      }
      $('#wysiwyg').wysihtml5({
        locale: 'zh-CN',
        customTemplates: myCustomTemplates
      });
      editor = $('#wysiwyg').data("wysihtml5").editor;
      editor.on("change", function() {
        log(bind.record.content);
        return bind.record.content = $('#wysiwyg').val();
      });
      return $('#image-file').change(selectFile);
    };
  });

}).call(this);
