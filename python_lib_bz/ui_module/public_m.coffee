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
  parms = this.expression.split(".")
  table_name = parms[0]
  column_name = parms[1]
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
      startDate: '1950-01-01'
      orientation: "top left"
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
    href = $(this.el).find("a").attr('href')
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

#2015-06-02 23:05 - modify by ZhangRui
#正则表达式的指令
Vue.directive('regexp',(value)->
  if not window.regexp
    window.regexp = {}
  if value
    reg = new RegExp(@arg)
    r = reg.test(value)
    if r
      $(@el).css('border-color','#d2d6de')
      window.regexp[@expression] = r
    else
      $(@el).css('border-color','#ff0000')
  else
    window.regexp[@expression] = false
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
  mobilecheck: ->
    check = false
    ((a) ->
      if /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a) or /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))
        check = true
      return
    ) navigator.userAgent or navigator.vendor or window.opera
    check
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
