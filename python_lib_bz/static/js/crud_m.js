(function() {
  $(function() {
    var id, parm, table_name, v_crud;
    v_crud = new Vue({
      el: '#v_crud',
      data: {
        editable: true,
        record: {},
        loading: false
      },
      methods: {
        toggleEdit: function() {
          if (this.$data.editable) {
            return this.$data.editable = false;
          } else {
            return this.$data.editable = true;
          }
        },
        getTableName: function() {
          var parm;
          parm = window.bz.getUrlParm();
          return parm[2];
        },
        save: function() {
          var data, table_name;
          data = this.$data;
          data.loading = true;
          table_name = this.getTableName();
          return $.post('/crud_api', JSON.stringify({
            table_name: table_name,
            record: data.record
          }), function(result, done) {
            data.loading = false;
            if (result.error !== '0') {
              return window.bz.showError5(result.error);
            } else if (result.error === void 0) {
              return data.error_info = '未知错误';
            } else {
              return window.bz.showSuccess5('成功提交');
            }
          });
        }
      }
    });
    table_name = v_crud.getTableName();
    parm = window.bz.getHashParms();
    id = parm[0].replace('#', '');
    if (id !== '') {
      id = parseInt(id);
      return $.post('/crud', JSON.stringify({
        table_name: table_name,
        id: id
      }), function(result, done) {
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
            v_crud.$data.record = result.data[0];
            return v_crud.$data.record.id = id;
          } else {
            return window.bz.showError5('未找到这条数据!');
          }
        }
      });
    }
  });

}).call(this);
