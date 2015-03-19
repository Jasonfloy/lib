(function() {
  $(function() {
    var load, table_name, v_crud_list;
    table_name = window.bz.getUrlParm()[2];
    v_crud_list = {};
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
      return $.get('/crud_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex).done(function(d1) {
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
    return $.get('/crud_list_api/' + table_name + '?queryCount=true').done(function(data) {
      var _currPageNo, _endPage, _pageCount, _resultCount;
      if (window.location.hash === '' || isNaN(window.location.hash.replace('#', ''))) {
        window.location.hash = '1';
      }
      _pageCount = 10;
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
      return v_crud_list = new Vue({
        el: '#v_crud_list',
        data: {
          list: [],
          module: "normal",
          loading: true,
          loading_target: "#v_crud_list",
          pagination: {
            resultCount: _resultCount,
            showFL: true,
            showFN: true,
            pageCount: _pageCount,
            currPage: _currPageNo,
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
    });
  });

}).call(this);
