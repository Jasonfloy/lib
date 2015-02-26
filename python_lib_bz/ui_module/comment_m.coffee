$(->
  v_comment = new Vue
    el:'#v_comment'
    data:
      error_info:false
      loading:false
      parent_id:0
    methods:
      commentEdit:->
        $(".placeholder-text").html(" ").removeAttr("class")
      clean:->
        @$data.error_info=false
      clickLink:(key_type, key, type)->
        if type == "comment"
          comment = $("#comment_text_area .comment-editable").html()
        else if type == "reply"
          comment = $("#reply_text_area .comment-editable").html()
        
        if comment == undefined or comment.trim() == ''
          @$data.error_info = '好歹说点什么吧!'
          return
        # 处理字符串, 为了在 new 页面中显示
        comment = comment.replace("\n", "").replace("<div>", "").replace("</div>", "\n")
        comment = comment.substr(0, comment.length - 1)
        $.post '/comment',
          JSON.stringify
            key_type:key_type
            key:key
            comment:comment
            parent_id:@$data.parent_id
        , (result) ->
          if result.error != '0'
            console.log result.error
            alert result.error
          else
            location.reload()
      #要回复哪条评论
      reply:(event, parent_id)->
        comment_reply = $(event.target).closest('.comment-reply')
        $(comment_reply).append($('#reply_text_area'))
        @$data.parent_id = parent_id
        $('#reply_text_area').removeClass("hide")
        $("#reply_text_area .comment-editable").focus()
)
