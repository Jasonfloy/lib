Vue.config.delimiters = ['(%', '%)']
window.log = (parm)-> console.log parm
#按钮上的 loading
Vue.directive('btn-loading', (value)->
    el = $(@el)
    if !!value
        el.children().hide()
        el.prepend("<i class='fa fa-spin fa-spinner'></i>")
    else
        el.children(".fa.fa-spin.fa-spinner").remove()
        el.children().show()
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

$().toastmessage(
  sticky: false
  position: 'top-right'
  stayTime: 5000
)

window.bz =
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
  #显示一个消息提示5s
  #依赖 https://github.com/akquinet/jquery-toastmessage-plugin
  showSuccess5:(message)->
    successToast = $().toastmessage('showSuccessToast', message)
  showNotice5:(message)->
    myToast =  $().toastmessage('showNoticeToast', message)
  showWarning5:(message)->
    warningToast = $().toastmessage('showNoticeToast', message)
  showError5:(message)->
    errorToast = $().toastmessage('showErrorToast', message)
  preZero:(num, len)->
    numStr = num.toString()
    if len < numStr.length
      return numStr
    else
      a = new Array(len + 1).join("0") + numStr
      return a.substr(a.length - len, a.length - 1)

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
