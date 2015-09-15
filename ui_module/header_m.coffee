$ ->
  v_header_m = new Vue
    el:'#v_header_m'
    data:
      loading:false
    methods:
      clickLink:->
        @loading = true
      search:(e)->
        # 如果定义了 header_search 方法, 就不用默认的 google search 了
        e.preventDefault()
        if window.header_search
          window.header_search(@search_value)
          return
        host = window.location.hostname
        url = "https://www.google.com/search?q=site:"+host+" "+@search_value+"&gws_rd=ssl"
        window.open(url)
