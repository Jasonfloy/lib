v_profile = new Vue
    el: "#v_profile"
    data:
        btn_loading: false
    methods:
        previewImg:(e)->
            file = e.target.files[0]
            if file.type.indexOf("image") != 0
                bz.showError5('上传的文件只能是图片哦~')
                return
            if file.size > (1024 * 1024)
                bz.showError5('图片大小只能小于1m哦~')
                return
            reader = new FileReader()
            reader.onload = ((uploadFile)->
                return (e)->
                    $(".profile-img img").attr("src", e.target.result)
            )(file)
            reader.readAsDataURL(file)
        save:->
            _this = @
            _this.btn_loading = true
            $.post("profile",JSON.stringify({"slogan": @slogan, "email": @email}))
            .done((d1)->
                if d1.error != 0
                    bz.showError5(d1.error)
                    _this.btn_loading = false
                    return
                fd = new FormData()
                file = $(".profile-img input[type='file']")[0].files[0]
                if file
                    fd.append("img", $(".profile-img input[type='file']")[0].files[0])
                    $.ajax({
                        url: "/profile",
                        type:"POST",
                        data: fd,
                        processData: false,
                        contentType: false
                    }).done((d2)->
                        if d2.error == 0
                            bz.showSuccess5("保存成功")
                        else
                            bz.showError5(d2.error)
                        _this.btn_loading = false
                    )
                else
                    bz.showSuccess5("保存成功")
                    _this.btn_loading = false
            )

