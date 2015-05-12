(function() {
  $(function() {
    var v_crud_check;
    return v_crud_check = new Vue({
      el: '#v_crud_check',
      data: {
        editable: false,
        record: {},
        loading: false
      },
      created: function() {
        return this.loadData();
      },
      methods: {
        getTableName: function() {
          var parm;
          parm = window.bz.getUrlParm();
          console.log("parm: ", parm);
          return parm[2];
        },
        jump2List: function() {
          var path;
          path = '/crud_check_list/' + this.getTableName();
          return location.pathname = path;
        },
        save: function() {
          var data, table_name;
          data = this.$data;
          data.loading = true;
          table_name = this.getTableName();
          return $.post('/crud_api', JSON.stringify({
            table_name: table_name,
            record: data.record
          })).done(function(result) {
            if (result.error !== '0') {
              return window.bz.showError5(result.error);
            } else if (result.error === void 0) {
              return data.error_info = '未知错误';
            } else {
              return window.bz.showSuccess5('审核成功...正在返回列表');
            }
          });
        },
        loadData: function() {
          var id, parm, table_name, _this;
          _this = this;
          table_name = this.getTableName();
          parm = window.bz.getHashParms();
          id = parm[0].replace('#', '');
          return $.post('/crud_check', JSON.stringify({
            'table_name': table_name,
            'id': id
          })).done(function(result) {
            var field, record;
            console.log(result);
            if (result.error !== '0') {
              window.bz.showError5(result.error);
            } else {
              if (result.data.length > 0) {
                record = result.data[0];
                for (field in record) {
                  if (record[field] !== null && typeof record[field] === "object") {
                    record[field] = JSON.stringify(record[field]);
                  }
                }
                _this.record = record;
              } else if (id !== '') {
                window.bz.showError5('未找到这条数据!');
              }
            }
            return console.log("record:", _this.record);
          });
        }
      }
    });
  });

}).call(this);
