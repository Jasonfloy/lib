$ ->
  toolbar = [
    'title'
    'bold'
    'italic'
    'underline'
    'strikethrough'
    'color'
    '|'
    'ol'
    'ul'
    'blockquote'
    'code'
    'table'
    '|'
    'link'
    'image'
    'hr'
    '|'
    'indent'
    'outdent'
    'alignment'
  ]
  mobileToolbar = [
    'bold'
    'underline'
    'strikethrough'
    'color'
    'ul'
    'ol'
  ]
  if bz.mobilecheck()
    toolbar = mobileToolbar
  editor = new Simditor(
    textarea: $('#editor')
    placeholder: '这里输入文字...'
    toolbar: toolbar
    pasteImage: true
    defaultImage: 'assets/images/image.png'
    upload:
      upurl: '/upload_file'
      upparams: null
      upfileKey: 'upload_file'
      upconnectionCount: 3
      upleaveConfirm: '正在上传文件，如果离开上传会自动取消'
  )

