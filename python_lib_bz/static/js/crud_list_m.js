(function() {
  $(function() {
    var load, table_name, v_crud_list;
    v_crud_list = new Vue({
      el: '#v_crud_list',
      data: {
        list: [],
        module: "normal",
        loading: true,
        loading_target: "#v_crud_list",
        pagination: {
          resultCount: 101,
          showFL: true,
          showFN: true,
          currPage: 1,
          showPageNum: 7,
          gotoPageFun: function(currPage) {
            return console.log(currPage);
          }
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
    table_name = window.bz.getUrlParm()[2];
    load = function() {
      return $.get('/crud_list_api/' + table_name).done(function(d1) {
        v_crud_list.$data.loading = false;
        if (d1.error !== "0") {
          window.bz.showError5(d1.error);
          return;
        }
        d1.array.forEach(function(n) {
          return n.checked = false;
        });
        return v_crud_list.$set("list", d1.array);
      });
    };
    return load();
  });

}).call(this);
