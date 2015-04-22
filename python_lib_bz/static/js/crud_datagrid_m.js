(function() {
  $(function() {
    var i, j, len, results, table_name, vues;
    vues = $(".safe-datagrid");
    results = [];
    for (j = 0, len = vues.length; j < len; j++) {
      i = vues[j];
      table_name = i.id;
      results.push(new Vue({
        el: '#' + table_name,
        data: {
          list: [],
          record: {},
          module: "normal",
          loading: true,
          loading_target: "#" + table_name,
          checked_list: {}
        },
        created: function() {
          this.table_name = table_name;
          return this.loadListData();
        },
        methods: {
          loadListData: function() {
            var _this;
            _this = this;
            return $.post('/crud_list_api/' + this.table_name).done(function(d1) {
              log(d1);
              if (d1.error !== "0") {
                window.bz.showError5(d1.error);
                return;
              }
              _this.$set("list", d1.array);
              return _this.loading = false;
            });
          },
          checkBox: function() {
            this.checked_list = _.where(this.list, {
              "checked": true
            });
            if (this.checked_list.length === 0) {
              return this.module = 'normal';
            } else if (this.checked_list.length === 1) {
              return this.module = 'select_one';
            } else if (this.checked_list.length > 1) {
              return this.module = 'select_more';
            }
          },
          getRecordDetail: function(id) {
            var _this, parm;
            parm = {
              table_name: this.table_name
            };
            _this = this;
            if (id !== '') {
              parm.id = id;
            }
            return $.post('/crud', JSON.stringify(parm)).done(function(result) {
              var field, record;
              if (result.error !== '0') {
                return window.bz.showError5(result.error);
              } else {
                if (result.data.length > 0) {
                  record = result.data[0];
                  for (field in record) {
                    if (record[field] !== null && typeof record[field] === "object") {
                      record[field] = JSON.stringify(record[field]);
                    }
                  }
                  _this.record = result.data[0];
                  return _this.record.id = id;
                } else if (id !== '') {
                  return window.bz.showError5('未找到这条数据!');
                }
              }
            });
          },
          edit: function() {
            var id;
            $('#modal-' + this.table_name).modal();
            id = this.checked_list[0].id;
            return this.getRecordDetail(id);
          },
          "new": function() {
            this.record = {};
            return $('#modal-' + this.table_name).modal();
          },
          confirm: function() {
            return $('#confirm-' + this.table_name).modal();
          },
          del: function() {
            var _this, del_array;
            _this = this;
            del_array = _.pluck(this.checked_list, "id");
            $.ajax({
              url: '/crud_list_api/' + this.table_name,
              type: 'DELETE',
              data: del_array.join(",")
            }).done(function(data) {
              if (data.error = "0") {
                window.bz.showSuccess5("删除成功");
                return _this.loadListData();
              } else {
                return window.bz.showError5(data.error);
              }
            });
          },
          save: function() {
            var _this;
            _this = this;
            this.loading = true;
            log(this.record);
            return $.post('/crud_api', JSON.stringify({
              table_name: this.table_name,
              record: this.record
            })).done(function(result) {
              _this.loading = false;
              $('#modal-' + _this.table_name).modal('hide');
              if (result.error !== '0') {
                return window.bz.showError5(result.error);
              } else if (result.error === void 0) {
                return data.error_info = '未知错误';
              } else {
                window.bz.showSuccess5("添加成功");
                return _this.loadListData();
              }
            });
          }
        }
      }));
    }
    return results;
  });

}).call(this);
