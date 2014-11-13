Vue.config({ delimiters: ["[", "]"] })
data = {}
data.error_info = false

v_share = new Vue
  el:'#v_comment'
  data:data
  methods:
    updateComment:(id)->
      comment = @$data.comment
      if comment.trim() == ''
        data.error_info = '好歹说点什么吧!'
        return
      window.superagent.post '/UpdateMyDescription',
        id:id
        description:comment
      , (error, res) ->
        result = JSON.parse(res.text)
        if result.error != '0'
          alert result.error
        else
          location.reload()
    cleanError:->
      data.error_info = false
