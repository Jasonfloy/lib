Vue.config.delimiters = ['(%', '%)']
window.log = (parm)-> console.log parm
#用来做延迟运行,例子: delay 1500, -> v_crud.jump2List()
window.delay = (ms, func) -> setTimeout func, ms

# 闭包方法添加 watch
setWatch = (vm, arg, table_name, column_name, el)->
  vm.$watch(arg, (new_value)->
    if $(el).is("select")
      getOptions(table_name, column_name, new_value, (options)->
        hide = $(el).hasClass("hide")
        if options
          $(el).removeClass("hide")
          str = "<option value='' disabled='true' selected>--请选择--</option>"
          i = 0
          while i < options.length
            str += "<option value='" + options[i].value + "'>" + options[i].text + "</option>"
            i++
          $(el).html(str)
        else if hide
          $(el).addClass("hide")
      )
    else
      getValue(table_name, column_name, new_value, (data)->
        $(el).val(data[0].value)
      )
  , false, false)

# ajax获取options
getOptions = (table_name, column_name, key, callback)->
  if not key
    return
  str = [table_name, column_name, key].join("/")
  $.get("/cascade/options/" + str, (data)->
    if not data.error == "0"
      window.bz.showError5("获取数据失败，请刷新重试。")
    else
      callback(data.options)
  )

# ajax获取关联的value
getValue = (table_name, column_name, key, callback)->
  if not key
    return
  str = [table_name, column_name, key].join("/")
  $.get("/cascade/value/" + str, (data)->
    if not data.error == "0"
      window.bz.showError5("获取数据失败，请刷新重试。")
    else
      callback(data.options)
  )

# 创建级联关系
# 使用方法
# <select class="hide" v-cascade="watch_parm : table_name.column_name">
# </select>

Vue.directive("cascade",->
  # 拆解参数
  parms = this.expression.split(".");
  table_name = parms[0];
  column_name = parms[1];
  setWatch(this.vm, this.arg, table_name, column_name, this.el)
)

# 日期格式化
Vue.directive('dateformat', (value)->
  if value
    el = $(@el)
    mask = @arg
    date_str = window.bz.dateFormat(value, mask)
    el.html(date_str)
)

# 字符串显示省略
Vue.directive('ellipsis', (str)->
  if str
    el = $(@el)
    len = @arg
    if len < str.length
      el.html(str.substring(0, len) + "...")
    else
      el.html(str)
)

# 按钮上的 loading
Vue.directive('btn-loading', (value)->
  el = $(@el)
  if !!value
    el.children().hide()
    el.prepend("<i class='fa fa-spin fa-spinner'></i>")
  else
    el.children(".fa.fa-spin.fa-spinner").remove()
    el.children().show()
)

Vue.directive('datepicker',
  bind: (value)->
    _this = @
    datepicker = $(@el)
    datepicker.datepicker
      format: "yyyy-mm-dd"
      language: "zh-CN"
      autoclose: true
      forceParse: true
      clearBtn: true
    .on("changeDate", (e)->
      levels = _this.raw.split(".")
      d_str = ""
      if e.date
        d_str = e.date.valueOf()
      temp_obj = _this.vm[levels[0]]
      index  = 1
      while index <= levels.length - 1
        level = levels[index]
        if typeof temp_obj[level] == "undefined" and index < levels.length - 1
          temp_obj.$add(levels[index], {})
          temp_obj = temp_obj[level]
        else if index == levels.length - 1
          temp_obj[level] = d_str
        index += 1
    ).siblings(".input-group-addon")
      .on("click", ->
        datepicker.datepicker("show")
      )
  update: (value)->
    if isNaN(value)
      $(@el).datepicker('update', value)
    else if value
      $(@el).datepicker('update', new Date(parseInt(value)))
    else
      $(@el).datepicker('update', '')
)
#进程的图标
Vue.directive "process-icon",
  update: (value) ->
    if value
      src = ""
      if /^QQ/.test(value)
        src = "qq.png"
      else if /^Google Chrome/.test(value)
        #src = "www.google.com/chrome/browser/desktop/index.html"
        src = "chrome.png"
      else if /^WeChat/.test(value)
        src = "weixin.png"
      else if /^iTerm/.test(value)
        src = "iterm2.png"
      else if /^node/.test(value)
        src = "nodejs.png"
      else if /python/.test(value) or /Python/.test(value)
        src = "python.png"
      else if /^nginx/.test(value)
        src = "nginx.png"
      else if /postgres/.test(value)
        src = "postgresql.png"
      else if /apache2/.test(value)
        src = "apache.png"
      else if /mysqld/.test(value)
        src = "mysql.png"
      else if /^java/.test(value)
        src = "java.png"
      else
        src="default.png"
      #img = '<img src="http://www.google.com/s2/favicons?domain='+src+'" height="16" width="16">'
      img = '<img src="/static/favicons/ico/'+src+'" height="16" style="margin-right: 4px;" width="16">'

      path = ""
      if /dropbox/.test(value)
        path = "dropbox.ico"
      if path != ""
        img = '<img src="/static/favicons/'+path+'" height="16" style="margin-right: 4px;" width="16">'

      if value.length > 80
        value = value.substr(0,80) + "+"
      $(@el).html(img+value)

#根据 a 的是否是当前 url 的一部分来判断是否设置 active
Vue.directive 'a-active',
  bind:  ->
    href = $(this.el).attr('href')
    href = encodeURI(href)
    path = window.location.pathname
    if path.search(href) != -1
      $(this.el).addClass("active")

#操作系统发行版本的图标
Vue.directive "release-icon",
  update: (value) ->
    file_name='hold.svg'
    if value
      # windows 未收录版本默认图标
      if value.search("Windows") != -1
        file_name = "windows8.svg"
      if value.search('Fedora') != -1
        file_name = "fedora.svg"
      if value.search('Ubuntu') != -1
        file_name = "ubuntu.svg"
      if value.search("CentOS") != -1
        file_name = "centos.svg"
      if value.search('Windows XP') != -1
        file_name = "windows.svg"
      if value.search('Windows 7') != -1
        file_name = "windows.svg"
      if value.search('Windows 8.1') != -1
        file_name = "windows8.svg"
      if value.search('Darwin') != -1
        file_name = "osx.svg"
      @el.src = "/static/images/system_icon/" + file_name

Vue.directive('disable', (value)->
  this.el.disabled = !!value
)

Vue.directive('active', (value)->
  if !!value
    $(this.el).addClass("active")
  else
    $(this.el).removeClass("active")
)

if $().toastmessage
  $().toastmessage(
    sticky: false
    position: 'top-right'
    stayTime: 5000
    closeText: '<i class="fa fa-times"></i>'
    successText: '<i class="fa fa-check"></i>'
    warningText: '<i class="fa fa-exclamation-triangle"></i>',
    noticeText: '<i class="fa fa-exclamation"></i>',
    errorText: '<i class="fa fa-exclamation-circle"></i>'
  )
window.bz =
  setOnErrorVm:(vm)->
    window.onerror = (errorMsg, url, lineNumber)->
      error = errorMsg.replace('Uncaught Error: ', '')
      vm.$set('error_info', error)
      window.bz.showError5(error)
  #是不是空对象
  isEmpty : (obj) ->
    # null and undefined are "empty"
    if obj == null
      return true
    # Assume if it has a length property with a non-zero value
    # that that property is correct.
    if obj.length > 0
      return false
    if obj.length == 0
      return true
    # Otherwise, does it have any properties of its own?
    # Note that this doesn't handle
    # toString and valueOf enumeration bugs in IE < 9
    for key of obj
      if Object::hasOwnProperty.call(obj, key)
        return false
    true

  #计算距今的时间间隔
  timeLen : (that_time)->
    second = 1000
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    month = day * 30
    year = month * 12

    now = Date.now()
    interval = now - that_time
  
    if interval < minute
      desc  = parseInt(interval / second) + "秒前"
    else if interval < hour
      desc = parseInt(interval / minute) + "分钟前"
    else if interval < day
      desc = parseInt(interval / hour) + "小时前"
    else if interval < month
      desc = parseInt(interval / day) + "天前"
    else if interval < year
      desc = parseInt(interval / month) + "个月前"
    else
      desc = parseInt(interval / year)+"年前"
    return desc
  #取最后的参数
  getLastParm:->
    parms = window.location.pathname.split( '/' )
    return parms[parms.length-1]
  getUrlParm:->
    parms = window.location.pathname.split( '/' )
    return parms
  #获取hash参数，返回数组
  getHashParms:->
    parms = window.location.hash.split('/')
    return parms
  #显示一个消息提示5s
  #依赖 https://github.com/akquinet/jquery-toastmessage-plugin
  showSuccess5:(message)->
    if $().toastmessage
      successToast = $().toastmessage('showSuccessToast', message)
    else
      console.log "require jquery-toastmessage-plugin"
  showNotice5:(message)->
    if $().toastmessage
      myToast =  $().toastmessage('showNoticeToast', message)
    else
      console.log "require jquery-toastmessage-plugin"
  showWarning5:(message)->
    if $().toastmessage
      warningToast = $().toastmessage('showNoticeToast', message)
    else
      console.log "require jquery-toastmessage-plugin"
  showError5:(message)->
    if $().toastmessage
      errorToast = $().toastmessage('showErrorToast', message)
    else
      console.log "require jquery-toastmessage-plugin"
  preZero:(num, len)->
    numStr = num.toString()
    if len < numStr.length
      return numStr
    else
      a = new Array(len + 1).join("0") + numStr
      return a.substr(a.length - len, a.length - 1)
  # 清除html标签
  HTMLEncode:(value)->
    return $("<div/>").html(value).text()
  HTMLDecode:(value)->
    return $("<div/>").text(value).html()

  #时间格式化工具 timestramp -> string
  #支持 y - 年,M - 月,d - 日,h - 小时,m - 分钟,s - 秒 根据mask中对应字符的数量自动补0
  dateFormat:(timestramp, mask)->
    date = new Date(timestramp)
    _this = @
    o = {
      "y+": (len)->
        return _this.preZero(date.getFullYear(), len)
      "M+": (len)->
        return _this.preZero(date.getMonth() + 1, len)
      "d+": (len)->
        return _this.preZero(date.getDate(), len)
      "h+": (len)->
        return _this.preZero(date.getHours(), len)
      "m+": (len)->
        return _this.preZero(date.getMinutes(), len)
      "s+": (len)->
        return _this.preZero(date.getSeconds(), len)
    }
    for regStr of o
      matched_array = mask.match(new RegExp(regStr))
      if matched_array
        res = o[regStr](matched_array[0].length)
        mask = mask.replace(matched_array[0], res)
    return mask
  #转换单位
  #传入kb
  #超过1024kb为m
  #超过1024m的按照g显示
  #超过1024g的按照T显示
  formatUnit:(value)->
    value = parseFloat(value)
    m = 1024
    g = m*1024
    t = g*1024
    if value>t
      desc = (value/t).toFixed(2) + 'TB'
    else if value>g
      desc = (value/g).toFixed(2) + 'GB'
    else if value>m
      desc = (value/m).toFixed(2) + 'MB'
    else
      desc = value + 'KB'
    return desc
    
  # 获取hash参数的值
  getHashPram: (key) ->
    _hashStr = window.location.hash.replace('#','')
    if(!_hashStr || _hashStr == "")
      return undefined
    _hashs = _hashStr.split(";")
    for _hashItem in _hashs
      _hash = _hashItem.split("=")
      if(key == _hash[0])
        return _hash[1]
    return undefined
        
  # 设置hash参数,格式如: aa=bb;cc=dd;  
  setHashPram: (key,value) ->
    _hashStr = window.location.hash.replace('#','')
    if(!window.bz.getHashPram(key) && value)
      window.location.hash = _hashStr + key + "=" + value + ";"
    else
      _hashs = _hashStr.split(";")
      _newHashStr = ""
      for _hashItem in _hashs
        if (!_hashItem || _hashItem == "")
             continue
          _hash = _hashItem.split("=")
          if(key == _hash[0])
            if(value != "")
              _newHashStr = _newHashStr + key + "=" + value + ";"
          else
            _newHashStr = _newHashStr + _hash[0] + "=" + _hash[1] + ";"
      window.location.hash = _newHashStr
  isInclude : (key,words)->
    if words.toLocaleLowerCase().indexOf(key.toLocaleLowerCase()) > -1
        return true
    else
        return false
  resolve: (obj, path, value) ->
    r=path.split(".")
    if r.length > 1
      key = r.shift()
      if not obj[key]
        obj[key]={}
      return window.bz.resolve(obj[key], r.join("."), value)
    else
      obj[path] = value or {}
    @
