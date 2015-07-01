(function() {
  var getOptions, getValue, setWatch;

  Vue.config.delimiters = ['(%', '%)'];

  window.log = function(parm) {
    return console.log(parm);
  };

  window.delay = function(ms, func) {
    return setTimeout(func, ms);
  };

  setWatch = function(vm, arg, table_name, column_name, el) {
    return vm.$watch(arg, function(new_value) {
      if ($(el).is("select")) {
        return getOptions(table_name, column_name, new_value, function(options) {
          var hide, i, str;
          hide = $(el).hasClass("hide");
          if (options) {
            $(el).removeClass("hide");
            str = "<option value='' disabled='true' selected>--请选择--</option>";
            i = 0;
            while (i < options.length) {
              str += "<option value='" + options[i].value + "'>" + options[i].text + "</option>";
              i++;
            }
            return $(el).html(str);
          } else if (hide) {
            return $(el).addClass("hide");
          }
        });
      } else {
        return getValue(table_name, column_name, new_value, function(data) {
          return $(el).val(data[0].value);
        });
      }
    }, false, false);
  };

  getOptions = function(table_name, column_name, key, callback) {
    var str;
    if (!key) {
      return;
    }
    str = [table_name, column_name, key].join("/");
    return $.get("/cascade/options/" + str, function(data) {
      if (!data.error === "0") {
        return window.bz.showError5("获取数据失败，请刷新重试。");
      } else {
        return callback(data.options);
      }
    });
  };

  getValue = function(table_name, column_name, key, callback) {
    var str;
    if (!key) {
      return;
    }
    str = [table_name, column_name, key].join("/");
    return $.get("/cascade/value/" + str, function(data) {
      if (!data.error === "0") {
        return window.bz.showError5("获取数据失败，请刷新重试。");
      } else {
        return callback(data.options);
      }
    });
  };

  Vue.directive("cascade", function() {
    var column_name, parms, table_name;
    parms = this.expression.split(".");
    table_name = parms[0];
    column_name = parms[1];
    return setWatch(this.vm, this.arg, table_name, column_name, this.el);
  });

  Vue.directive('dateformat', function(value) {
    var date_str, el, mask;
    if (value) {
      el = $(this.el);
      mask = this.arg;
      date_str = window.bz.dateFormat(value, mask);
      return el.html(date_str);
    }
  });

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

  Vue.directive('datepicker', {
    bind: function(value) {
      var _this, datepicker;
      _this = this;
      datepicker = $(this.el);
      return datepicker.datepicker({
        format: "yyyy-mm-dd",
        language: "zh-CN",
        autoclose: true,
        forceParse: true,
        clearBtn: true,
        startDate: '1980-01-01',
        orientation: "top left"
      }).on("changeDate", function(e) {
        var d_str, index, level, levels, results, temp_obj;
        levels = _this.raw.split(".");
        d_str = "";
        if (e.date) {
          d_str = e.date.valueOf();
        }
        temp_obj = _this.vm[levels[0]];
        index = 1;
        results = [];
        while (index <= levels.length - 1) {
          level = levels[index];
          if (typeof temp_obj[level] === "undefined" && index < levels.length - 1) {
            temp_obj.$add(levels[index], {});
            temp_obj = temp_obj[level];
          } else if (index === levels.length - 1) {
            temp_obj[level] = d_str;
          }
          results.push(index += 1);
        }
        return results;
      }).siblings(".input-group-addon").on("click", function() {
        return datepicker.datepicker("show");
      });
    },
    update: function(value) {
      if (isNaN(value)) {
        return $(this.el).datepicker('update', value);
      } else if (value) {
        return $(this.el).datepicker('update', new Date(parseInt(value)));
      } else {
        return $(this.el).datepicker('update', '');
      }
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
      href = $(this.el).find("a").attr('href');
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

  Vue.directive('regexp', function(value) {
    var r, reg;
    if (!window.regexp) {
      window.regexp = {};
    }
    if (value) {
      reg = new RegExp(this.arg);
      r = reg.test(value);
      if (r) {
        $(this.el).css('border-color', '#d2d6de');
        return window.regexp[this.expression] = r;
      } else {
        return $(this.el).css('border-color', '#ff0000');
      }
    } else {
      return window.regexp[this.expression] = false;
    }
  });

  if ($().toastmessage) {
    $().toastmessage({
      sticky: false,
      position: 'top-right',
      stayTime: 5000,
      closeText: '<i class="fa fa-times"></i>',
      successText: '<i class="fa fa-check"></i>',
      warningText: '<i class="fa fa-exclamation-triangle"></i>',
      noticeText: '<i class="fa fa-exclamation"></i>',
      errorText: '<i class="fa fa-exclamation-circle"></i>'
    });
  }

  window.bz = {
    mobilecheck: function() {
      var check;
      check = false;
      (function(a) {
        if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) {
          check = true;
        }
      })(navigator.userAgent || navigator.vendor || window.opera);
      return check;
    },
    setOnErrorVm: function(vm) {
      return window.onerror = function(errorMsg, url, lineNumber) {
        var error;
        error = errorMsg.replace('Uncaught Error: ', '');
        vm.$set('error_info', error);
        return window.bz.showError5(error);
      };
    },
    isEmpty: function(obj) {
      var key;
      if (obj === null) {
        return true;
      }
      if (obj.length > 0) {
        return false;
      }
      if (obj.length === 0) {
        return true;
      }
      for (key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
          return false;
        }
      }
      return true;
    },
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
    getUrlParm: function() {
      var parms;
      parms = window.location.pathname.split('/');
      return parms;
    },
    getHashParms: function() {
      var parms;
      parms = window.location.hash.split('/');
      return parms;
    },
    showSuccess5: function(message) {
      var successToast;
      if ($().toastmessage) {
        return successToast = $().toastmessage('showSuccessToast', message);
      } else {
        return console.log("require jquery-toastmessage-plugin");
      }
    },
    showNotice5: function(message) {
      var myToast;
      if ($().toastmessage) {
        return myToast = $().toastmessage('showNoticeToast', message);
      } else {
        return console.log("require jquery-toastmessage-plugin");
      }
    },
    showWarning5: function(message) {
      var warningToast;
      if ($().toastmessage) {
        return warningToast = $().toastmessage('showNoticeToast', message);
      } else {
        return console.log("require jquery-toastmessage-plugin");
      }
    },
    showError5: function(message) {
      var errorToast;
      if ($().toastmessage) {
        return errorToast = $().toastmessage('showErrorToast', message);
      } else {
        return console.log("require jquery-toastmessage-plugin");
      }
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
      var _this, date, matched_array, o, regStr, res;
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
    },
    getHashPram: function(key) {
      var _hash, _hashItem, _hashStr, _hashs, j, len1;
      _hashStr = window.location.hash.replace('#', '');
      if (!_hashStr || _hashStr === "") {
        return void 0;
      }
      _hashs = _hashStr.split(";");
      for (j = 0, len1 = _hashs.length; j < len1; j++) {
        _hashItem = _hashs[j];
        _hash = _hashItem.split("=");
        if (key === _hash[0]) {
          return _hash[1];
        }
      }
      return void 0;
    },
    setHashPram: function(key, value) {
      var _hash, _hashItem, _hashStr, _hashs, _newHashStr, j, len1;
      _hashStr = window.location.hash.replace('#', '');
      if (!window.bz.getHashPram(key) && value) {
        return window.location.hash = _hashStr + key + "=" + value + ";";
      } else {
        _hashs = _hashStr.split(";");
        _newHashStr = "";
        for (j = 0, len1 = _hashs.length; j < len1; j++) {
          _hashItem = _hashs[j];
          if (!_hashItem || _hashItem === "") {
            continue;
          }
          _hash = _hashItem.split("=");
          if (key === _hash[0]) {
            if (value !== "") {
              _newHashStr = _newHashStr + key + "=" + value + ";";
            }
          } else {
            _newHashStr = _newHashStr + _hash[0] + "=" + _hash[1] + ";";
          }
        }
        return window.location.hash = _newHashStr;
      }
    },
    isInclude: function(key, words) {
      if (words.toLocaleLowerCase().indexOf(key.toLocaleLowerCase()) > -1) {
        return true;
      } else {
        return false;
      }
    },
    resolve: function(obj, path, value) {
      var key, r;
      r = path.split(".");
      if (r.length > 1) {
        key = r.shift();
        if (!obj[key]) {
          obj[key] = {};
        }
        return window.bz.resolve(obj[key], r.join("."), value);
      } else {
        obj[path] = value || {};
      }
      return this;
    }
  };

}).call(this);
