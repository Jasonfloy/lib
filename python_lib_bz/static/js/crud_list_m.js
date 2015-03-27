(function() {
  $(function() {
    var _currPageNo, _hashItemTemp, _hashStrTemp, _hashTemp, _hashsTemp, _onbeforeunloadCleanStorage, _pageCount, count, getHashPram, j, k, len, len1, load, objTemp, searchKeyValue, searchPam, searchPams, search_parms, setHashPram, storageData, table_name, v_crud_list;
    table_name = window.bz.getUrlParm()[2];
    v_crud_list = {};
    count = 0;
    search_parms = [];
    _pageCount = 10;
    _currPageNo = 1;
    _onbeforeunloadCleanStorage = true;
    window.onbeforeunload = function(event) {
      if (_onbeforeunloadCleanStorage) {
        return window.sessionStorage.clear();
      }
    };
    getHashPram = function(key) {
      var _hash, _hashItem, _hashStr, _hashs, j, len;
      _hashStr = window.location.hash.replace('#', '');
      if (!_hashStr || _hashStr === "") {
        return void 0;
      }
      _hashs = _hashStr.split(";");
      for (j = 0, len = _hashs.length; j < len; j++) {
        _hashItem = _hashs[j];
        _hash = _hashItem.split("=");
        if (key === _hash[0]) {
          return _hash[1];
        }
      }
      return void 0;
    };
    setHashPram = function(key, value) {
      var _hash, _hashItem, _hashStr, _hashs, _newHashStr, j, len;
      _hashStr = window.location.hash.replace('#', '');
      if (!getHashPram(key) && value) {
        return window.location.hash = _hashStr + key + "=" + value + ";";
      } else {
        _hashs = _hashStr.split(";");
        _newHashStr = "";
        for (j = 0, len = _hashs.length; j < len; j++) {
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
    };
    if (window.sessionStorage) {
      storageData = window.sessionStorage.getItem("search_curd_list_" + table_name);
      if (storageData) {
        window.location.hash = "";
        searchPams = storageData.split(";");
        if (searchPams[0] !== "") {
          for (j = 0, len = searchPams.length; j < len; j++) {
            searchPam = searchPams[j];
            if (searchPam === "") {
              continue;
            }
            searchKeyValue = searchPam.split("=");
            if (searchKeyValue[0] === "" || searchKeyValue[1] === "") {
              continue;
            }
            setHashPram(searchKeyValue[0], searchKeyValue[1]);
          }
        }
      }
    }
    _hashStrTemp = window.location.hash.replace('#', '');
    if (_hashStrTemp) {
      search_parms = [];
      _hashsTemp = _hashStrTemp.split(";");
      for (k = 0, len1 = _hashsTemp.length; k < len1; k++) {
        _hashItemTemp = _hashsTemp[k];
        if (_hashItemTemp === "") {
          continue;
        }
        _hashTemp = _hashItemTemp.split("=");
        if (_hashTemp[0] === "" || _hashTemp[1] === "" || _hashTemp[0].indexOf("search_") === -1) {
          continue;
        }
        if ($("#" + _hashTemp[0])) {
          $("#" + _hashTemp[0]).val(_hashTemp[1]);
          objTemp = {
            "name": _hashTemp[0].replace("search_", ""),
            "value": _hashTemp[1]
          };
          search_parms.push(objTemp);
        }
      }
    }
    if (!getHashPram("p") || isNaN(getHashPram("p"))) {
      setHashPram("p", "1");
    }
    _currPageNo = parseInt(getHashPram("p"));
    load = function(currPage, beginIndex, endIndex, limit) {
      setHashPram("p", currPage);
      if (window.sessionStorage) {
        window.sessionStorage.setItem("search_curd_list_" + table_name, window.location.hash.replace("#", ""));
      }
      if (v_crud_list.$data) {
        v_crud_list.$data.loading = true;
      }
      if (!limit) {
        limit = 10;
      }
      if (!beginIndex) {
        beginIndex = 1;
      }
      return $.post('/crud_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex + '&find=true', JSON.stringify({
        table_name: table_name,
        search_parms: search_parms
      })).done(function(d1) {
        if (d1.error !== "0") {
          window.bz.showError5(d1.error);
          return;
        }
        d1.array.forEach(function(n) {
          return n.checked = false;
        });
        v_crud_list.$set("list", d1.array);
        return v_crud_list.$data.loading = false;
      });
    };
    Vue.directive('on-search', {
      twoWay: true,
      bind: function(value) {
        var _vue_this, eventAndFun, eventName;
        eventAndFun = this.raw.split(":");
        this["search_fn_" + eventAndFun[0] + eventAndFun[1]] = (function() {
          return this.vm[eventAndFun[1]]();
        }).bind(this);
        if (eventAndFun[0] === "enter") {
          eventName = "onkeypress";
          _vue_this = this;
          return this.el[eventName] = function(event) {
            if (event && event.keyCode === 13) {
              return _vue_this["search_fn_" + eventAndFun[0] + eventAndFun[1]]();
            }
          };
        } else {
          eventName = "on" + eventAndFun[0];
          return this.el[eventName] = this["search_fn_" + eventAndFun[0] + eventAndFun[1]];
        }
      },
      update: function(value) {},
      unbind: function() {
        var eventName, eventNameKey;
        eventNameKey = this.raw.split(":")[0];
        eventName = "on" + eventNameKey;
        return this.el[eventName] = void 0;
      }
    });
    v_crud_list = new Vue({
      el: '#v_crud_list',
      data: {
        list: [],
        record: {},
        module: "normal",
        loading: true,
        loading_target: "#v_crud_list",
        pagination: {
          resultCount: 1,
          showFL: true,
          showFN: true,
          pageCount: _pageCount,
          currPage: _currPageNo,
          showPageNum: 7,
          gotoPageFun: load,
          onInitedLoadCurrPageData: false
        }
      },
      methods: {
        detail: function(event, record) {
          console.log(record);
          if (record === "new") {
            window.location.href = "/crud/" + table_name;
            _onbeforeunloadCleanStorage = false;
            return;
          }
          if (this.module === 'normal') {
            window.location.href = "/crud/" + table_name + "#" + record.id;
            _onbeforeunloadCleanStorage = false;
          } else if (record.checked) {
            record.checked = false;
            return $(event.target).siblings(".check-column").find("input[type=checkbox]").prop('checked', false);
          } else {
            record.checked = true;
            return $(event.target).siblings(".check-column").find("input[type=checkbox]").prop('checked', true);
          }
        },
        moduleToggle: function() {
          if (this.module === 'edit') {
            return this.$set('module', 'normal');
          } else if (this.module === 'normal') {
            return this.$set('module', 'edit');
          }
        },
        searchToggle: function() {
          $('.moreSearch').toggle();
          return $('#gridSearch').toggle();
        },
        find: function() {
          var a, i, l, len2, s, searchs;
          search_parms = [];
          i = 0;
          searchs = $(".form-search");
          for (l = 0, len2 = searchs.length; l < len2; l++) {
            s = searchs[l];
            if (s.value) {
              a = {
                "name": s.name,
                "value": s.value
              };
              setHashPram("search_" + s.name, s.value);
              search_parms[i] = a;
              i = i + 1;
            } else {
              setHashPram("search_" + s.name, "");
            }
          }
          return $.post('/crud_list_api/' + table_name + '?queryCount=true&find=true', JSON.stringify({
            table_name: table_name,
            search_parms: search_parms
          })).done(function(data) {
            return v_crud_list.$data.pagination.resultCount = data.count;
          });
        },
        del: function() {
          var del_array;
          del_array = _.pluck(_.where(this.list, {
            "checked": true
          }), "id");
          $.ajax({
            url: '/crud_list_api/' + table_name,
            type: 'DELETE',
            data: del_array.join(",")
          }).done(function(data) {
            if (data.error = "0") {
              window.bz.showSuccess5("删除成功。");
              return load();
            } else {
              return window.bz.showError5(data.error);
            }
          });
        }
      }
    });
    return $.post('/crud_list_api/' + table_name + '?queryCount=true&find=true', JSON.stringify({
      table_name: table_name,
      search_parms: search_parms
    })).done(function(data) {
      var _endPage, _resultCount;
      _resultCount = data.count;
      _endPage = parseInt(_resultCount / _pageCount);
      if (_resultCount % _pageCount > 0) {
        _endPage = _endPage + 1;
      }
      if (_currPageNo > _endPage) {
        setHashPram("p", "1");
        _currPageNo = 1;
        v_crud_list.$data.pagination.currPage = _currPageNo;
      }
      return v_crud_list.$data.pagination.resultCount = _resultCount;
    });
  });

}).call(this);
