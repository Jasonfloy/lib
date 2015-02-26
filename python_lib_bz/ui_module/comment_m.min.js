(function() {
  $(function() {
    var v_comment;
    return v_comment = new Vue({
      el: '#v_comment',
      data: {
        error_info: false,
        btn_loading: false,
        loading: false,
        parent_id: 0
      },
      methods: {
        commentEdit: function() {
          return $(".placeholder-text").html(" ").removeAttr("class");
        },
        clean: function() {
          return this.$data.error_info = false;
        },
        clickLink: function(key_type, key, type) {
          var comment;
          if (type === "comment") {
            comment = $("#comment_text_area .comment-editable").html();
          } else if (type === "reply") {
            comment = $("#reply_text_area .comment-editable").html();
          }
          if (comment === void 0 || comment.trim() === '') {
            data.error_info = '好歹说点什么吧!';
            return;
          }
          comment = comment.replace("\n", "").replace("<div>", "").replace("</div>", "\n");
          comment = comment.substr(0, comment.length - 1);
          this.$data.btn_loading = true;
          return $.post('/comment', JSON.stringify({
            key_type: key_type,
            key: key,
            comment: comment,
            parent_id: this.$data.parent_id
          }), function(result) {
            if (result.error !== '0') {
              console.log(result.error);
              data.btn_loading = false;
              return alert(result.error);
            } else {
              return location.reload();
            }
          });
        },
        reply: function(event, parent_id) {
          var comment_reply;
          comment_reply = $(event.target).closest('.comment-reply');
          $(comment_reply).append($('#reply_text_area'));
          this.$data.parent_id = parent_id;
          $('#reply_text_area').removeClass("hide");
          return $("#reply_text_area .comment-editable").focus();
        }
      }
    });
  });

}).call(this);
