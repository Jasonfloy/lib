(function() {
  $(function() {
    var selectPage, v_crud_check_list;
    selectPage = function(currPage, beginIndex, endIndex, limit) {
      var checked, table_name;
      if (!limit) {
        limit = 10;
      }
      if (!beginIndex) {
        beginIndex = 0;
      }
      table_name = window.bz.getUrlParm()[2];
      checked = 'nocheck';
      if (v_crud_check_list) {
        v_crud_check_list.table_name = table_name;
        checked = v_crud_check_list.checked;
      }
      return $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex + '&checked=' + checked).done(function(data) {
        if (data.error === "0") {
          v_crud_check_list.records = data.records;
          return v_crud_check_list.pagination.resultCount = data.count;
        } else {
          return window.bz.showError5(data.error);
        }
      });
    };
    return v_crud_check_list = new Vue({
      el: '#v_crud_check_list',
      data: {
        records: [],
        table_name: '',
        checked: 'nocheck',
        checked_text: '待审核',
        options: [
          {
            text: '待审核',
            value: 'nocheck'
          }, {
            text: '未通过',
            value: 'nopass'
          }, {
            text: '已通过',
            value: 'pass'
          }
        ],
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
        },
        checkedSelect: function(e) {
          var i, len, option, ref;
          ref = this.options;
          for (i = 0, len = ref.length; i < len; i++) {
            option = ref[i];
            if (option.value === this.checked) {
              this.checked_text = option.text;
            }
          }
          return selectPage();
        }
      }
    });
  });

}).call(this);
