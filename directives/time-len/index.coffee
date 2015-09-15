require './style.less'
bz = require '../../lib.coffee'
module.exports =
  bind: ->
  update: (new_value, old_value) ->
    if new_value
      el = $(@el)
      date_str = bz.timeLen(new_value)
      el.html(date_str)
  unbind: ->
