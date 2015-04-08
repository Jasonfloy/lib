# 按钮上的 loading
Vue.directive('btn-loading', (value)->
  el = $(@el)
    if !!value
        el.children().hide()
        el.prepend("<i class='fa fa-spin fa-spinner'></i>")
    else
        el.children(".fa.fa-spin.fa-spinner").remove()
        el.children().show()
)


