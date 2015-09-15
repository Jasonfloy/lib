# 把disabled和href合并了
module.exports =
  bind: ->
    $(@el).prepend("<i class='fa fa-spin fa-spinner'></i>")
    return
  update: (value, old_value) ->
    if value
      $(@el).removeAttr('disabled').attr 'href', value
    else
      $(@el).attr 'disabled', true
    return
  unbind: ->
