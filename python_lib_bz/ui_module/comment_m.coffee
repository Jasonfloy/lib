$(->
  v_comment = new Vue
    el:'#v_comment'
    data:
      error_info:false
      btn_loading: false
      loading:false
      parent_id:0
    methods:
      clean:->
        @$data.error_info=false
      clickLink:(key_type, key)->
        comment = @$data.comment
        data = @$data
        if comment == undefined or comment.trim() == ''
          data.error_info = '好歹说点什么吧!'
          return
        data.btn_loading = true
        $.post '/comment',
          JSON.stringify
            key_type:key_type
            key:key
            comment:comment
            parent_id:@$data.parent_id
        , (result) ->

          if result.error != '0'
            console.log result.error
            data.btn_loading = false
            alert result.error
          else
            location.reload()
      #要回复哪条评论
      reply:(event, parent_id)->
        comment_reply = $(event.target).closest('.comment-reply')
        $(comment_reply).append($('#comment_text_area'))
        @$data.parent_id = parent_id
        $(".comment-textarea").focus()
)
