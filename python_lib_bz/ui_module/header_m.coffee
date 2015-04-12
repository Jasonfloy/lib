$(->
    v_header_m = new Vue
        el:'#v_header_m'
        data:
            loading:false
        methods:
            clickLink:->
                @$data.loading = true
)
