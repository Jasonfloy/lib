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
          loading_target: "#" + table_name
        },
        created: function() {
          var _this;
          _this = this;
          this.table_name = table_name;
          return $.post('/crud_list_api/' + this.table_name).done(function(d1) {
            if (d1.error !== "0") {
              window.bz.showError5(d1.error);
              return;
            }
            _this.$set("list", d1.array);
            return _this.loading = false;
          });
        },
        methods: {
          checkBox: function() {
            var checked_list;
            checked_list = _.where(this.list, {
              "checked": true
            });
            if (checked_list.length === 0) {
              return this.module = 'normal';
            } else if (checked_list.length === 1) {
              return this.module = 'select_one';
            } else if (checked_list.length > 1) {
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
            id = _.where(this.list, {
              "checked": true
            })[0].id;
            return this.getRecordDetail(id);
          },
          "new": function() {
            this.record = {};
            return $('#modal-' + this.table_name).modal();
          },
          del: function() {
            var del_array;
            del_array = _.pluck(_.where(this.list, {
              "checked": true
            }), "id");
            log(del_array);
            return log(del_array.join(","));
          },
          moduleToggle: function() {
            if (this.module === 'edit') {
              return this.$set('module', 'normal');
            } else if (this.module === 'normal') {
              return this.$set('module', 'edit');
            }
          }
        }
      }));
    }
    return results;
  });

}).call(this);
