var data, v_share;

Vue.config({
  delimiters: ["[", "]"]
});

data = {};

data.error_info = false;

v_share = new Vue({
  el: '#v_comment',
  data: data,
  methods: {
    updateComment: function(id) {
      var comment;
      comment = this.$data.comment;
      if (comment.trim() === '') {
        data.error_info = '好歹说点什么吧!';
        return;
      }
      return window.superagent.post('/UpdateMyDescription', {
        id: id,
        description: comment
      }, function(error, res) {
        var result;
        result = JSON.parse(res.text);
        if (result.error !== '0') {
          return alert(result.error);
        } else {
          return location.reload();
        }
      });
    },
    cleanError: function() {
      return data.error_info = false;
    }
  }
});
