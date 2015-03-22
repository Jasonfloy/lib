    currPageObj = {}
    genPage = (cfg) ->
        pages = []
        if(cfg.showFL)
            obj = {}
            obj.name = "第一页"
            obj.targetPage = 1
            if(cfg.currPage == 1)
                obj.classStr = "disabled"
                obj.canClick = false
            else
                obj.classStr = ""
                obj.canClick = true
            pages.push(obj)
        if(cfg.showFN)
            obj = {}
            obj.name = "上一页"
            obj.targetPage = cfg.currPage - 1
            if(cfg.currPage == 1)
                obj.classStr = "disabled"
                obj.canClick = false
            else
                obj.classStr = ""
                obj.canClick = true
            pages.push(obj)
        center = parseInt(cfg.showPageNum/2)
        if(cfg.currPage > center)
            showPageBegin = cfg.currPage - center
        else
            showPageBegin = 1
        showPageEnd = showPageBegin + cfg.showPageNum - 1
        if(showPageEnd > cfg.endPage)
            showPageBegin = cfg.endPage - cfg.showPageNum + 1
            showPageEnd = cfg.endPage
        if(showPageBegin < 1)
            showPageBegin = 1
        while showPageBegin <= showPageEnd
            obj = {}
            obj.name = showPageBegin
            obj.targetPage = showPageBegin
            obj.canClick = true
            if(cfg.currPage == showPageBegin)
                obj.classStr = "active"
                obj.canClick = false
                currPageObj = obj
            pages.push(obj)
            showPageBegin++
        if(cfg.showFN)
            obj = {}
            obj.name = "下一页"
            obj.targetPage = cfg.currPage + 1
            if(cfg.currPage >= cfg.endPage)
                obj.classStr = "disabled"
                obj.canClick = false
            else
                obj.classStr = ""
                obj.canClick = true
            pages.push(obj)
        if(cfg.showFL)
            obj = {}
            obj.name = "最后一页"
            obj.targetPage = cfg.endPage
            if(cfg.currPage >= cfg.endPage)
                obj.classStr = "disabled"
                obj.canClick = false
            else
                obj.classStr = ""
                obj.canClick = true
            pages.push(obj)
         return pages
         
    Vue.component 'vue_pagination', 
        inherit: true
        template: '<nav><ul class="pagination"><li class="(% p.classStr %)" v-repeat="p : pages"><a href="javascript:void(0);" v-on="click: butClick(p)">(%p.name%)</a></li></ul></nav>'
        attached: ->
            cfg =
                showFL: true #是否显示第一页,最后一页
                showFN: true #是否显示上一页,下一页
                pageCount: 10 #每页几行
                resultCount: 1 #总记录数,必须
                currPage: 1 #当前第几页
                showPageNum: 5 #显示几个页面按钮
                showGotoPage: true #是否显示直接跳转
                gotoPageFun: -> #点击页数按钮时的回掉方法,用以使用者加载数据.组件传递给该方法的参数:currPage(当前页), 
                                #beginIndex(数据库查询开始条数,部分数据库从0开始的需要减一), endIndex(数据库查询结束条数), limit(每页几条数据)
                onInitedLoadCurrPageData: false #组件初始化完成后自动调用gotoPageFun方法(用以加载当前页数据)的开关
                
            @$watch("pagination", (newVal, oldVal)->
                console.log @pagination
                if(!@pagination)
                    @pagination = {}
                if(typeof (@pagination.showFL) == "boolean")
                    cfg.showFL = @pagination.showFL
                if(typeof (@pagination.showFN) == "boolean")
                    cfg.showFN = @pagination.showFN
                if(@pagination.pageCount)
                    cfg.pageCount = @pagination.pageCount
                if(@pagination.resultCount)
                    cfg.resultCount = @pagination.resultCount
                if(@pagination.currPage)
                    cfg.currPage = @pagination.currPage
                    if(cfg.currPage < 1)
                        cfg.currPage = 1
                if(@pagination.showPageNum)
                    cfg.showPageNum = @pagination.showPageNum
                if(@pagination.showGotoPage)
                    cfg.showGotoPage = @pagination.showGotoPage
                if(@pagination.gotoPageFun)
                    cfg.gotoPageFun = @pagination.gotoPageFun
                if(@pagination.onInitedLoadCurrPageData)
                    cfg.onInitedLoadCurrPageData = @pagination.onInitedLoadCurrPageData
                
                cfg.endPage = parseInt(cfg.resultCount/cfg.pageCount)
                if(cfg.resultCount%cfg.pageCount > 0)
                    cfg.endPage = cfg.endPage + 1
                @$set("pagination_cfg", cfg)
                @$set("pages", genPage(cfg))
                if(cfg.onInitedLoadCurrPageData)
                    @butClick(currPageObj, true)
            ,true,true)
                
        methods: 
                butClick: (page, firstCall) ->
                    if(page.canClick || firstCall)
                        @pagination_cfg.currPage = page.targetPage
                        #计算起始行数(部分数据库从0开始,后端拿到这个值后需要减1)
                        beginIndex = (@pagination_cfg.currPage - 1) * @pagination_cfg.pageCount + 1
                        if(@pagination_cfg.currPage == 1)
                            beginIndex = 1
                        #计算结束行数(部分数据库通过起始行号及取多少条确定,不需要次参数)
                        endIndex = beginIndex + @pagination_cfg.pageCount - 1
                        @pagination_cfg.gotoPageFun(@pagination_cfg.currPage, beginIndex, endIndex, @pagination_cfg.pageCount)
                        @$set("pages", genPage(@pagination_cfg)) #生成分页组件数据模型并刷新组件
