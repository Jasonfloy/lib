(function() {
  $(function() {
    var count, load, search_parms, table_name, v_crud_list, _pageCount;
    table_name = window.bz.getUrlParm()[2];
    v_crud_list = {};
    count = 0;
    search_parms = [];
    _pageCount = 10;
    load = function(currPage, beginIndex, endIndex, limit) {
      window.location.hash = currPage;
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
        var eventAndFun, eventName;
        eventAndFun = this.raw.split(":");
        this["search_fn_" + eventAndFun[0] + eventAndFun[1]] = (function() {
          return this.vm[eventAndFun[1]]();
        }).bind(this);
        eventName = "on" + eventAndFun[0];
        return this.el[eventName] = this["search_fn_" + eventAndFun[0] + eventAndFun[1]];
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
          currPage: 1,
          showPageNum: 7,
          gotoPageFun: load,
          onInitedLoadCurrPageData: true
        }
      },
      methods: {
        detail: function(event, record) {
          console.log(record);
          if (record === "new") {
            window.location.href = "/crud/" + table_name;
            return;
          }
          if (this.module === 'normal') {
            window.location.href = "/crud/" + table_name + "#" + record.id;
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
          return $('.moreSearch').toggle();
        },
        find: function() {
          var a, i, s, searchs, _i, _len;
          search_parms = [];
          i = 0;
          searchs = $(".form-search");
          for (_i = 0, _len = searchs.length; _i < _len; _i++) {
            s = searchs[_i];
            if (s.value) {
              a = {
                "name": s.name,
                "value": s.value
              };
              search_parms[i] = a;
              i = i + 1;
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
    return $.post('/crud_list_api/' + table_name + '?queryCount=true').done(function(data) {
      var _currPageNo, _endPage, _resultCount;
      if (window.location.hash === '' || isNaN(window.location.hash.replace('#', ''))) {
        window.location.hash = '1';
      }
      _resultCount = data.count;
      _currPageNo = parseInt(window.location.hash.replace('#', ''));
      _endPage = parseInt(_resultCount / _pageCount);
      if (_resultCount % _pageCount > 0) {
        _endPage = _endPage + 1;
      }
      if (_currPageNo > _endPage) {
        window.location.hash = '1';
        _currPageNo = 1;
      }
      v_crud_list.$data.pagination.resultCount = _resultCount;
      return v_crud_list.$data.pagination.currPage = _currPageNo;
    });
  });

}).call(this);
