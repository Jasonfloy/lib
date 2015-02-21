var data, v_share;

Vue.config.delimiters = ['(%', '%)'];

Vue.directive("show-bz", {
  bind: function(value) {
    if (value && value.length !== 0) {
      return $(this.el).removeClass('hide_bz');
    } else {
      return $(this.el).addClass('hide_bz');
    }
  },
  update: function(value) {
    if (value && value.length !== 0) {
      return $(this.el).removeClass('hide_bz');
    } else {
      return $(this.el).addClass('hide_bz');
    }
  }
});

data = {};

data.error_info = false;

data.parent_id = 0;

v_share = new Vue({
  el: '#v_comment',
  data: function() {
    return data;
  },
  methods: {
    clean: function() {
      return this.$data.error_info = false;
    },
    submit: function(key_type, key) {
      var comment;
      comment = this.$data.comment;
      if (comment === void 0 || comment.trim() === '') {
        this.$data.error_info = '好歹说点什么吧!';
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
    reply: function(event, parent_id) {
      var comment_reply;
      comment_reply = $(event.target).closest('.comment-reply');
      $(comment_reply).append($('#comment_text_area'));
      this.$data.parent_id = parent_id;
      return $(".comment-textarea").focus();
    }
  }
});