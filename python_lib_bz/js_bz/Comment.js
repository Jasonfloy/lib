var data, v_share;

data = {};

data.error_info = false;

data.parent_id = 0;

v_share = new Vue({
  el: '#v_comment',
  data: function() {
    return data;
  },
  methods: {
    submit: function(key_type, key) {
      var comment;
      comment = this.$data.comment;
      if (comment.trim() === '') {
        data.error_info = '好歹说点什么吧!';
        return;
      }
      return $.post('/comment', JSON.stringify({
        key_type: key_type,
        key: key,
        comment: comment,
        parent_id: this.$data.parent_id
      }), function(result) {
        if (result.error !== '0') {
          console.log(result.error);
          return alert(result.error);
        } else {
          return location.reload();
        }
      }, "");
    },
    cleanError: function() {
      return data.error_info = false;
    },
    reply: function(event, parent_id) {
      var comment_reply;
      comment_reply = $(event.target).closest('.comment-reply');
      $(comment_reply).append($('#comment_text_area'));
      this.$data.parent_id = parent_id;
      return $(".comment-textarea").focus();
    }
  }
});
