(function() {
  $(function() {
    var selectPage, v_crud_check_list;
    selectPage = function(currPage, beginIndex, endIndex, limit) {
      var table_name;
      if (!limit) {
        limit = 10;
      }
      if (!beginIndex) {
        beginIndex = 0;
      }
      table_name = window.bz.getUrlParm()[2];
      if (v_crud_check_list) {
        v_crud_check_list.table_name = table_name;
      }
      return $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex).done(function(data) {
        if (data.error === "0") {
          v_crud_check_list.records = data.records;
          return v_crud_check_list.pagination.resultCount = data.count;
        } else {
          return window.bz.showError5(d1.error);
        }
      });
    };
    return v_crud_check_list = new Vue({
      el: '#v_crud_check_list',
      data: {
        records: [],
        table_name: '',
        pagination: {
          showFL: true,
          showFN: true,
          resultCount: 10,
          pageCount: 20,
          currPage: 1,
          showPageNum: 7,
          gotoPageFun: selectPage,
          onInitedLoadCurrPageData: false
        }
      },
      methods: {
        detail: function(record_id) {
          return window.location.href = "/crud_check/" + this.table_name + "#" + record_id;
        }
      }
    });
  });

}).call(this);
