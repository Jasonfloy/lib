data = {}
data.error_info = false
data.parent_id = 0

v_share = new Vue
  el:'#v_comment'
  data:->
    data
  methods:
    submit:(key_type, key)->
      comment = @$data.comment
      if comment.trim() == ''
        data.error_info = '好歹说点什么吧!'
        return
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
      ,""
    cleanError:->
      data.error_info = false
    #要回复哪条评论
    reply:(parent_id)->
      @$data.parent_id = parent_id
