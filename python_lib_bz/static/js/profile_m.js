(function() {
  $(function() {
    var v_profile;
    return v_profile = new Vue({
      el: "#v_profile",
      data: {
        btn_loading: false
      },
      methods: {
        previewImg: function(e) {
          var file, reader;
          file = e.target.files[0];
          if (file.type.indexOf("image") !== 0) {
            bz.showError5('上传的文件只能是图片哦~');
            return;
          }
          if (file.size > (1024 * 1024)) {
            bz.showError5('图片大小只能小于1m哦~');
            return;
          }
          reader = new FileReader();
          reader.onload = (function(uploadFile) {
            return function(e) {
              return $(".profile-img img").attr("src", e.target.result);
            };
          })(file);
          return reader.readAsDataURL(file);
        },
        edit: function() {
          $("input.editable").removeAttr("disabled");
          $("#btn-edit").hide();
          $("#btn-save").show();
        },
        save: function() {
          var _this;
          _this = this;
          _this.btn_loading = true;
          return $.post("profile", JSON.stringify({
            "slogan": this.slogan,
            "email": this.email
          })).done(function(d1) {
            var fd, file;
            if (d1.error !== 0) {
              bz.showError5(d1.error);
              _this.btn_loading = false;
              return;
            }
            fd = new FormData();
            file = $(".profile-img input[type='file']")[0].files[0];
            if (file) {
              fd.append("img", $(".profile-img input[type='file']")[0].files[0]);
              return $.ajax({
                url: "/file_upload",
                type: "POST",
                data: fd,
                processData: false,
                contentType: false
              }).done(function(d2) {
                if (d2.error === 0) {
                  bz.showSuccess5("保存成功");
                } else {
                  bz.showError5(d2.error);
                }
                return _this.btn_loading = false;
              });
            } else {
              $("input.editable").attr("disabled", "disabled");
              $("#btn-save").hide();
              $("#btn-edit").show();
              bz.showSuccess5("保存成功");
              return _this.btn_loading = false;
            }
          });
        }
      }
    });
  });

}).call(this);
