(function() {
  $(function() {
    var i, j, len, results, table_name, vues;
    vues = $(".safe-datagrid");
    results = [];
    for (j = 0, len = vues.length; j < len; j++) {
      i = vues[j];
      table_name = i.id;
      results.push(new Vue({
        el: '#' + i.id,
        data: {
          list: [],
          module: "normal"
        },
        created: function() {
          var _this;
          _this = this;
          return $.post('/crud_list_api/' + table_name).done(function(d1) {
            if (d1.error !== "0") {
              window.bz.showError5(d1.error);
              return;
            }
            d1.array.forEach(function(n) {
              return n.checked = false;
            });
            return _this.$set("list", d1.array);
          });
        },
        methods: {
          detail: function(event, index) {
            var record;
            if (index === "new") {
              window.location.href = "/crud/" + table_name;
              return;
            }
            record = this.list[index];
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
      }));
    }
    return results;
  });

}).call(this);
