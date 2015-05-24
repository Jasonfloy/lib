(function() {
  $(function() {
    var i, j, len, results, table_name, user_id, vues;
    vues = $(".safe-datagrid");
    results = [];
    for (j = 0, len = vues.length; j < len; j++) {
      i = vues[j];
      table_name = i.id;
      user_id = window.bz.getHashPram("user_id");
      results.push(new Vue({
        el: '#' + table_name,
        data: {
          list: [],
          record: {},
          module: "normal",
          loading: true,
          loading_target: "#" + table_name,
          checked_list: {},
          file_columns: []
        },
        created: function() {
          this.table_name = table_name;
          this.user_id = user_id;
          this.initModule();
          this.loadListData();
          return this.getRecordDetail();
        },
        watch: {
          "record.id": function() {
            var _this;
            _this = this;
            return _this.file_columns.forEach(function(column) {
              return _this.$[column.name + "_c"].getExistFiles();
            });
          }
        },
        methods: {
          clickLine: function(r) {
            if (this.user_id) {
              $('#modal-' + this.table_name).modal();
              return this.getRecordDetail(r.id);
            }
          },
          look: function(r) {
            this.module = "look";
            $('#modal-' + this.table_name).modal();
            return this.getRecordDetail(r.id);
          },
          initModule: function() {
            if (this.user_id) {
              return this.module = "look";
            } else {
              return this.module = "normal";
            }
          },
          loadListData: function() {
            var _this, url;
            _this = this;
            this.initModule();
            url = '/crud_list_api/' + this.table_name;
            if (this.user_id) {
              url += '?user_id=' + this.user_id;
            }
            return $.post(url).done(function(d1) {
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
              return this.initModule();
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
                _this.$set("file_columns", result.file_columns);
                if (result.data.length > 0) {
                  record = result.data[0];
                  for (field in record) {
                    if (record[field] !== null && typeof record[field] === "object") {
                      record[field] = JSON.stringify(record[field]);
                    }
                  }
                  _this.record = result.data[0];
                  return _this.record.id = id;
                } else if (id !== '' && typeof id !== "undefined") {
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
            var key, new_record;
            this.module = "normal";
            new_record = {};
            for (key in this.record) {
              if (key === 'id') {
                continue;
              }
              new_record[key] = null;
            }
            this.$set("record", new_record);
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
              if (data.error === "0") {
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
            if (window.bz.isEmpty(this.record)) {
              window.bz.showError5('没有填写任何值!');
              _this.loading = false;
              $('#modal-' + _this.table_name).modal('hide');
              return;
            }
            return $.post('/crud_api', JSON.stringify({
              table_name: this.table_name,
              record: this.record
            })).done(function(result) {
              _this.loading = false;
              $('#modal-' + _this.table_name).modal('hide');
              if (result.error !== '0') {
                return window.bz.showError5(result.error);
              } else if (result.error === void 0) {
                return window.bz.showError5('未知错误');
              } else {
                _this.$set("record.id", result.id);
                _this.file_columns.forEach(function(column) {
                  _this.$[column.name + "_c"].createFileRef(result.id);
                  return _this.$[column.name + "_c"].clear();
                });
                window.bz.showSuccess5("操作成功");
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
