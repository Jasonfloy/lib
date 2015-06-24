(function() {
  $(function() {
    var editor, input, myCustomTemplates, selectFile, the_wysiwyg;
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
    the_wysiwyg = $('#wysiwyg').wysihtml5({
      locale: 'zh-CN',
      customTemplates: myCustomTemplates
    });
    editor = the_wysiwyg.data("wysihtml5").editor;
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
          var error, file_path;
          if (d.error === '0') {
            log(editor);
            log($('#wysiwyg').data("wysihtml5"));
            file_path = d.results[0].file_path;
            try {
              editor.composer.commands.exec("insertImage", {
                src: file_path,
                alt: "this is an image"
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
    return $('#image-file').change(selectFile);
  });

}).call(this);
