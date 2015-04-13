$(->
    v_header_m = new Vue
        el:'#v_header_m'
        data:
            loading:false
        methods:
            clickLink:->
                @loading = true
            submit:(e)->
                e.preventDefault()
                host = window.location.hostname
                url = "https://www.google.com/search?q=site:"+host+" "+@search+"&gws_rd=ssl"
                window.open(url)
)
