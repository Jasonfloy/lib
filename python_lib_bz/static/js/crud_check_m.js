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
          return parm[2];
        },
        jump2List: function() {
          var path;
          path = '/crud_check_list/' + this.getTableName();
          return location.pathname = path;
        },
        save: function(checked) {
          var _this, record, table_name;
          _this = this;
          this.loading = true;
          table_name = this.getTableName();
          record = {
            'id': this.record.id,
            'checked': checked
          };
          console.log("record: ", record);
          return $.post('/crud_api', JSON.stringify({
            table_name: table_name,
            record: record
          })).done(function(data) {
            if (data.error === '0') {
              window.bz.showSuccess5('审核成功...正在返回列表');
              _this.loading = false;
              return delay(2000, function() {
                return _this.jump2List();
              });
            } else {
              return window.bz.showError5(data.error);
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
            if (result.error !== '0') {
              return window.bz.showError5(result.error);
            } else {
              if (result.data.length > 0) {
                record = result.data[0];
                record.id = id;
                for (field in record) {
                  if (record[field] !== null && typeof record[field] === "object") {
                    record[field] = JSON.stringify(record[field]);
                  }
                }
                return _this.record = record;
              } else if (id !== '') {
                return window.bz.showError5('未找到这条数据!');
              }
            }
          });
        }
      }
    });
  });

}).call(this);
