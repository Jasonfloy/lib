(function() {
  Vue.config.delimiters = ['(%', '%)'];

  window.log = function(parm) {
    return console.log(parm);
  };

  Vue.directive('ellipsis', function(str) {
    var el, len;
    if (str) {
      el = $(this.el);
      len = this.arg;
      if (len < str.length) {
        return el.html(str.substring(0, len) + "...");
      } else {
        return el.html(str);
      }
    }
  });

  Vue.directive('btn-loading', function(value) {
    var el;
    el = $(this.el);
    if (!!value) {
      el.children().hide();
      return el.prepend("<i class='fa fa-spin fa-spinner'></i>");
    } else {
      el.children(".fa.fa-spin.fa-spinner").remove();
      return el.children().show();
    }
  });

  Vue.directive("process-icon", {
    update: function(value) {
      var img, path, src;
      if (value) {
        src = "";
        if (/^QQ/.test(value)) {
          src = "qq.png";
        } else if (/^Google Chrome/.test(value)) {
          src = "chrome.png";
        } else if (/^WeChat/.test(value)) {
          src = "weixin.png";
        } else if (/^iTerm/.test(value)) {
          src = "iterm2.png";
        } else if (/^node/.test(value)) {
          src = "nodejs.png";
        } else if (/python/.test(value) || /Python/.test(value)) {
          src = "python.png";
        } else if (/^nginx/.test(value)) {
          src = "nginx.png";
        } else if (/postgres/.test(value)) {
          src = "postgresql.png";
        } else if (/apache2/.test(value)) {
          src = "apache.png";
        } else if (/mysqld/.test(value)) {
          src = "mysql.png";
        } else if (/^java/.test(value)) {
          src = "java.png";
        } else {
          src = "default.png";
        }
        img = '<img src="/static/favicons/ico/' + src + '" height="16" style="margin-right: 4px;" width="16">';
        path = "";
        if (/dropbox/.test(value)) {
          path = "dropbox.ico";
        }
        if (path !== "") {
          img = '<img src="/static/favicons/' + path + '" height="16" style="margin-right: 4px;" width="16">';
        }
        if (value.length > 80) {
          value = value.substr(0, 80) + "+";
        }
        return $(this.el).html(img + value);
      }
    }
  });

  Vue.directive('a-active', {
    bind: function() {
      var href, path;
      href = $(this.el).attr('href');
      href = encodeURI(href);
      path = window.location.pathname;
      if (path.search(href) !== -1) {
        return $(this.el).addClass("active");
      }
    }
  });

  Vue.directive("release-icon", {
    update: function(value) {
      var file_name;
      file_name = 'hold.svg';
      if (value) {
        if (value.search("Windows") !== -1) {
          file_name = "windows8.svg";
        }
        if (value.search('Fedora') !== -1) {
          file_name = "fedora.svg";
        }
        if (value.search('Ubuntu') !== -1) {
          file_name = "ubuntu.svg";
        }
        if (value.search("CentOS") !== -1) {
          file_name = "centos.svg";
        }
        if (value.search('Windows XP') !== -1) {
          file_name = "windows.svg";
        }
        if (value.search('Windows 7') !== -1) {
          file_name = "windows.svg";
        }
        if (value.search('Windows 8.1') !== -1) {
          file_name = "windows8.svg";
        }
        if (value.search('Darwin') !== -1) {
          file_name = "osx.svg";
        }
        return this.el.src = "/static/images/system_icon/" + file_name;
      }
    }
  });

  Vue.directive('disable', function(value) {
    return this.el.disabled = !!value;
  });

  Vue.directive('active', function(value) {
    if (!!value) {
      return $(this.el).addClass("active");
    } else {
      return $(this.el).removeClass("active");
    }
  });

  $().toastmessage({
    sticky: false,
    position: 'top-right',
    stayTime: 5000
  });

  window.bz = {
    timeLen: function(that_time) {
      var day, desc, hour, interval, minute, month, now, second, year;
      second = 1000;
      minute = second * 60;
      hour = minute * 60;
      day = hour * 24;
      month = day * 30;
      year = month * 12;
      now = Date.now();
      interval = now - that_time;
      if (interval < minute) {
        desc = parseInt(interval / second) + "秒前";
      } else if (interval < hour) {
        desc = parseInt(interval / minute) + "分钟前";
      } else if (interval < day) {
        desc = parseInt(interval / hour) + "小时前";
      } else if (interval < month) {
        desc = parseInt(interval / day) + "天前";
      } else if (interval < year) {
        desc = parseInt(interval / month) + "个月前";
      } else {
        desc = parseInt(interval / year) + "年前";
      }
      return desc;
    },
    getLastParm: function() {
      var parms;
      parms = window.location.pathname.split('/');
      return parms[parms.length - 1];
    },
    getHashParms: function() {
      var parms;
      parms = window.location.hash.split('/');
      return parms;
    },
    showSuccess5: function(message) {
      var successToast;
      return successToast = $().toastmessage('showSuccessToast', message);
    },
    showNotice5: function(message) {
      var myToast;
      return myToast = $().toastmessage('showNoticeToast', message);
    },
    showWarning5: function(message) {
      var warningToast;
      return warningToast = $().toastmessage('showNoticeToast', message);
    },
    showError5: function(message) {
      var errorToast;
      return errorToast = $().toastmessage('showErrorToast', message);
    },
    preZero: function(num, len) {
      var a, numStr;
      numStr = num.toString();
      if (len < numStr.length) {
        return numStr;
      } else {
        a = new Array(len + 1).join("0") + numStr;
        return a.substr(a.length - len, a.length - 1);
      }
    },
    HTMLEncode: function(value) {
      return $("<div/>").html(value).text();
    },
    HTMLDecode: function(value) {
      return $("<div/>").text(value).html();
    },
    dateFormat: function(timestramp, mask) {
      var date, matched_array, o, regStr, res, _this;
      date = new Date(timestramp);
      _this = this;
      o = {
        "y+": function(len) {
          return _this.preZero(date.getFullYear(), len);
        },
        "M+": function(len) {
          return _this.preZero(date.getMonth() + 1, len);
        },
        "d+": function(len) {
          return _this.preZero(date.getDate(), len);
        },
        "h+": function(len) {
          return _this.preZero(date.getHours(), len);
        },
        "m+": function(len) {
          return _this.preZero(date.getMinutes(), len);
        },
        "s+": function(len) {
          return _this.preZero(date.getSeconds(), len);
        }
      };
      for (regStr in o) {
        matched_array = mask.match(new RegExp(regStr));
        if (matched_array) {
          res = o[regStr](matched_array[0].length);
          mask = mask.replace(matched_array[0], res);
        }
      }
      return mask;
    },
    formatUnit: function(value) {
      var desc, g, m, t;
      value = parseFloat(value);
      m = 1024;
      g = m * 1024;
      t = g * 1024;
      if (value > t) {
        desc = (value / t).toFixed(2) + 'TB';
      } else if (value > g) {
        desc = (value / g).toFixed(2) + 'GB';
      } else if (value > m) {
        desc = (value / m).toFixed(2) + 'MB';
      } else {
        desc = value + 'KB';
      }
      return desc;
    }
  };

}).call(this);
