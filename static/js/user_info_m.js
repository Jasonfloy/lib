(function() {
  $(function() {
    window.v_user_info = new Vue({
      el: "#v_user_info",
      ready: function() {
        return bz.setOnErrorVm(this);
      },
      data: {
        loading: false,
        user_info: {},
        disable_edit: true,
        button_text: '修改资料'
      },
      methods: {
        autoInsert: function(key, scheme) {
          if (scheme == null) {
            scheme = 'http://';
          }
          if (!this.user_info[key]) {
            return this.user_info.$set(key, scheme);
          }
        },
        changeImg: function() {
          return $('#profile-image-upload').click();
        },
        previewImg: function(e) {
          var file, reader;
          file = e.target.files[0];
          if (!file) {
            return;
          }
          if (file.size > (10 * 1024 * 1024)) {
            throw new Error("图片大小只能小于10m哦~");
          }
          reader = new FileReader();
          reader.onload = function(e) {
            return $("#profile-image-upload").attr("src", e.target.result);
          };
          reader.readAsDataURL(file);
          return this.uploadImage();
        },
        uploadImage: function() {
          var fd, file;
          fd = new FormData();
          file = $("#profile-image-upload")[0].files[0];
          if (file) {
            fd.append("img", file);
            return $.ajax({
              url: '/upload_image',
              type: 'POST',
              data: fd,
              processData: false,
              contentType: false,
              success: (function(_this) {
                return function(data, status, response) {
                  _this.loading = false;
                  console.log(data);
                  if (!data.success) {
                    throw new Error(data.msg);
                  } else {
                    bz.showSuccess5("保存成功");
                    _this.user_info.picture = data.file_path;
                    return $("#profile-image").attr("src", _this.user_info.picture);
                  }
                };
              })(this),
              error: function(error_info) {
                this.loading = false;
                throw new Error(error_info);
              }
            });
          }
        },
        save: function() {
          var parm, path;
          if (this.disable_edit) {
            this.disable_edit = false;
            return $("#btn-edit").text('保存');
          } else {
            this.loading = true;
            parm = JSON.stringify(this.user_info);
            path = bz.getUrlPath(1);
            return $.ajax({
              url: '/' + path,
              type: 'POST',
              data: parm,
              success: (function(_this) {
                return function(data, status, response) {
                  _this.loading = false;
                  _this.disable_edit = true;
                  $("#btn-edit").text('编辑');
                  if (data.error !== '0') {
                    throw new Error(data.error);
                  } else {
                    return bz.showSuccess5("保存成功");
                  }
                };
              })(this),
              error: (function(_this) {
                return function() {};
              })(this)
            });
          }
        }
      }
    });
    window.setVueValueForSimditor = function(value) {
      return v_user_info.$set('user_info.slogan', value);
    };
    if (bz.getLastParm() === 'add') {
      window.v_user_info.disable_edit = false;
      return $("#btn-edit").text('保存');
    }
  });

}).call(this);
