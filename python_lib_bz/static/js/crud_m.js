(function() {
  $(function() {
    var v_crud;
    return v_crud = new Vue({
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
          return $.post('/crud', JSON.stringify({
            table_name: table_name,
            record: data.record
          }), function(result, done) {
            data.loading = false;
            if (result.error !== '0') {
              return data.error_info = result.error;
            } else if (result.error === void 0) {
              return data.error_info = '未知错误';
            } else {
              return window.bz.showSuccess5('成功提交');
            }
          });
        }
      }
    });
  });

}).call(this);
