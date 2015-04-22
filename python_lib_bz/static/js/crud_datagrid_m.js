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
          del: function() {
            var del_array;
            del_array = _.pluck(_.where(this.list, {
              "checked": true
            }), "id");
            log(del_array);
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
      }));
    }
    return results;
  });

}).call(this);
