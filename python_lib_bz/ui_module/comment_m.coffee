Vue.config.delimiters = ['(%', '%)']
Vue.directive "show-bz",
  bind: (value) ->
    if value and value.length != 0
      $(@el).removeClass('hide_bz')
    else
      $(@el).addClass('hide_bz')
  update: (value) ->
    if value and value.length != 0
      $(@el).removeClass('hide_bz')
    else
      $(@el).addClass('hide_bz')

data = {}
data.error_info = false
data.parent_id = 0

v_share = new Vue
  el:'#v_comment'
  data:->
    data
  methods:
    clean:->
      @$data.error_info=false
    submit:(key_type, key)->
      comment = @$data.comment
      if comment == undefined or comment.trim() == ''
        @$data.error_info = '好歹说点什么吧!'
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
    #要回复哪条评论
    reply:(event, parent_id)->
      comment_reply = $(event.target).closest('.comment-reply')
      $(comment_reply).append($('#comment_text_area'))
      @$data.parent_id = parent_id
      $(".comment-textarea").focus()
