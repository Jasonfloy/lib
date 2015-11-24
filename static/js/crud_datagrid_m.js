(function() {
  $(function() {
    var i, ids, j, len, results, table_name, user_id, user_id_edit, vues;
    Vue.directive("datagrid-file-list", function(value) {
      var column, params, parms_str, table_name;
      params = this.arg.split(".");
      if (params.length < 2) {
        throw "file-list 指令中的参数不足，请检查是否指定表名与字段名.";
      }
      if (!$) {
        throw "JQuery没有正确引用.";
      }
      table_name = params[0];
      column = params[1];
      parms_str = [table_name, column, value].join("/");
      return (function(_this, str) {
        return $.get('/file_upload/' + str).done(function(d) {
          var f, html, i;
          html = '';
          if (d.results.length === 0) {
            return;
          }
          for (i in d.results) {
            f = d.results[i];
            html += '<div><a href=\'' + f.file_path + '\'\' target=\'_blank\'>下载</a></div>';
          }
          $(_this.el).html(html);
        });
      })(this, parms_str);
    });
    vues = $(".safe-datagrid");
    results = [];
    for (j = 0, len = vues.length; j < len; j++) {
      i = vues[j];
      table_name = i.id;
      user_id = window.bz.getHashPram("user_id");
      user_id_edit = null;
      if (user_id) {
        ids = user_id.split("_");
        if (ids.length > 1) {
          user_id_edit = ids[0];
        } else {
          user_id = ids[0];
        }
      }
      results.push(new Vue({
        el: '#' + table_name,
        data: {
          list: [],
          record: {},
          stat: "normal",
          loading: true,
          loading_target: "#" + table_name,
          file_columns: []
        },
        created: function() {
          this.table_name = table_name;
          this.user_id = user_id;
          this.user_id_edit = user_id_edit;
          this.initStat();
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
          look: function(r) {
            if (this.stat === 'normal') {
              this.stat = "look";
            }
            $('#modal-' + this.table_name).modal();
            return this.getRecordDetail(r.id);
          },
          initStat: function() {
            this.select = 'null';
            if (this.user_id && !user_id_edit) {
              return this.stat = "check";
            } else {
              return this.stat = "normal";
            }
          },
          loadListData: function() {
            var _this, url;
            _this = this;
            this.initStat();
            url = '/crud_list_api/' + this.table_name;
            if (this.user_id && !user_id_edit) {
              url += '?user_id=' + this.user_id;
            } else if (this.user_id_edit) {
              url += '?user_id=' + this.user_id_edit;
            } else {
              url = url;
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
          edit: function(row) {
            var id;
            this.stat = "normal";
            $('#modal-' + this.table_name).modal();
            id = row.id;
            return this.getRecordDetail(id);
          },
          "new": function() {
            var key, new_record;
            this.stat = "normal";
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
          del: function(row) {
            var _this, del_array;
            _this = this;
            del_array = [row.id];
            $.ajax({
              url: '/crud_list_api/' + this.table_name,
              type: 'DELETE',
              data: del_array.join(",")
            }).done(function(data) {
              if (data.error === "0") {
                window.bz.showSuccess5("删除成功");
                _this.initStat();
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
            if (_this.user_id_edit) {
              _this.$set("record.user_id", _this.user_id_edit);
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
