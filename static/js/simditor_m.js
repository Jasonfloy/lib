(function() {
  $(function() {
    var editor, mobileToolbar, toolbar;
    toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent', 'alignment'];
    mobileToolbar = ['bold', 'underline', 'strikethrough', 'color', 'ul', 'ol'];
    if (bz.mobilecheck()) {
      toolbar = mobileToolbar;
    }
    return window.editor = new Simditor({
      textarea: $('#editor'),
      placeholder: '这里输入文字...',
      toolbar: toolbar,
      pasteImage: true,
      defaultImage: 'assets/images/image.png',
      upload: {
        url: '/upload_file',
        params: null,
        fileKey: 'upload_file',
        connectionCount: 3,
        leaveConfirm: '正在上传文件，如果离开上传会自动取消'
      }
    });
  });

}).call(this);
