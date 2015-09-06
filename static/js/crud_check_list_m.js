(function() {
  $(function() {
    var selectPage, v_crud_check_list;
    selectPage = function(currPage, beginIndex, endIndex, limit) {
      var audit_state, table_name;
      if (!limit) {
        limit = 10;
      }
      if (!beginIndex) {
        beginIndex = 0;
      }
      table_name = window.bz.getUrlParm()[2];
      if (v_crud_check_list) {
        v_crud_check_list.table_name = table_name;
        audit_state = v_crud_check_list.audit_state;
      }
      return $.get('/crud_check_list_api/' + table_name + '?limit=' + limit + '&offset=' + beginIndex + '&audit_state=' + audit_state).done(function(data) {
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
        audit_state: 'pass',
        audit_state_text: '已确认',
        options: [
          {
            text: '已确认',
            value: 'pass'
          }, {
            text: '待确认',
            value: 'submit'
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
        detail: function(user_id, id) {
          if (this.table_name === "agency_info") {
            return window.location.href = "/" + this.table_name + "#user_id=" + user_id;
          } else {
            return window.location.href = "/" + this.table_name + "_detail/" + id + "#user_id=" + user_id;
          }
        },
        edit: function(row) {
          if (this.table_name === "agency_info") {
            return window.location.href = "/" + this.table_name + "#user_id=" + row.user_id + "_edit";
          } else {
            return window.location.href = "/" + this.table_name + "_detail/" + row.id + "#user_id=" + row.user_id + "_edit";
          }
        },
        deleteButton: function(row) {
          this.agency_id = row.id;
          this.agency_user_id = row.user_id;
          return $('#modal-delete').modal();
        },
        load: function() {
          var _this;
          _this = this;
          this.loading = true;
          return $.get('/oper?t=' + 'agency_info' + '&w=' + 'is_delete=0').done(function(data) {
            if (data.error !== "0") {
              window.bz.showError5(data.error);
            } else {
              _this.records = data.data;
            }
            return _this.loading = false;
          });
        },
        "delete": function() {
          var _this, agency, agency_user;
          _this = this;
          agency = {
            'id': this.agency_id,
            'is_delete': 1
          };
          agency_user = {
            'id': this.agency_user_id,
            'is_delete': 1
          };
          $.post('/oper', JSON.stringify({
            't': 'agency_info',
            'v': agency
          })).done(function(data) {
            if (data.error !== '0') {
              return window.bz.showError5(data.error);
            }
          });
          return $.post('/oper', JSON.stringify({
            't': 'user_info',
            'v': agency_user
          })).done(function(data) {
            if (data.error === '0') {
              window.bz.showSuccess5('删除成功!');
              _this.load();
            } else {
              window.bz.showError5(data.error);
            }
            return $('#modal-delete').hide();
          });
        },
        checkedSelect: function(e) {
          var i, len, option, ref;
          ref = this.options;
          for (i = 0, len = ref.length; i < len; i++) {
            option = ref[i];
            if (option.value === this.audit_state) {
              this.audit_state_text = option.text;
            }
          }
          return selectPage();
        },
        saveCheck: function(id) {
          var _this, update_record;
          _this = this;
          update_record = {
            'id': id,
            audit_state: 'pass'
          };
          return $.post('/oper', JSON.stringify({
            't': 'agency_info',
            'v': update_record
          })).done(function(data) {
            if (data.error === '0') {
              window.bz.showSuccess5('确认成功');
              _this.loading = false;
              return _this.load();
            } else {
              return window.bz.showError5(data.error);
            }
          });
        }
      }
    });
  });

}).call(this);
