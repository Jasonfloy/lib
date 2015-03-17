(function() {
  var genPage;

  genPage = function(cfg) {
    var center, obj, pages, showPageBegin, showPageEnd;
    pages = [];
    if (cfg.showFL) {
      obj = {};
      obj.name = "第一页";
      obj.targetPage = 1;
      if (cfg.currPage === 1) {
        obj.classStr = "disabled";
        obj.canClick = false;
      } else {
        obj.classStr = "";
        obj.canClick = true;
      }
      pages.push(obj);
    }
    if (cfg.showFN) {
      obj = {};
      obj.name = "上一页";
      obj.targetPage = cfg.currPage - 1;
      if (cfg.currPage === 1) {
        obj.classStr = "disabled";
        obj.canClick = false;
      } else {
        obj.classStr = "";
        obj.canClick = true;
      }
      pages.push(obj);
    }
    center = parseInt(cfg.showPageNum / 2);
    if (cfg.currPage > center) {
      showPageBegin = cfg.currPage - center;
    } else {
      showPageBegin = 1;
    }
    showPageEnd = showPageBegin + cfg.showPageNum - 1;
    if (showPageEnd > cfg.endPage) {
      showPageBegin = cfg.endPage - cfg.showPageNum + 1;
      showPageEnd = cfg.endPage;
    }
    while (showPageBegin <= showPageEnd) {
      obj = {};
      obj.name = showPageBegin;
      obj.targetPage = showPageBegin;
      obj.canClick = true;
      if (cfg.currPage === showPageBegin) {
        obj.classStr = "active";
        obj.canClick = false;
      }
      pages.push(obj);
      showPageBegin++;
    }
    if (cfg.showFN) {
      obj = {};
      obj.name = "下一页";
      obj.targetPage = cfg.currPage + 1;
      if (cfg.currPage >= cfg.endPage) {
        obj.classStr = "disabled";
        obj.canClick = false;
      } else {
        obj.classStr = "";
        obj.canClick = true;
      }
      pages.push(obj);
    }
    if (cfg.showFL) {
      obj = {};
      obj.name = "最后一页";
      obj.targetPage = cfg.endPage;
      if (cfg.currPage >= cfg.endPage) {
        obj.classStr = "disabled";
        obj.canClick = false;
      } else {
        obj.classStr = "";
        obj.canClick = true;
      }
      pages.push(obj);
    }
    return pages;
  };

  Vue.component('vue_pagination', {
    inherit: true,
    template: '<nav><ul class="pagination"><li class="(% p.classStr %)" v-repeat="p : pages"><a href="javascript:void(0);" v-on="click: butClick(p)">(%p.name%)</a></li></ul></nav>',
    created: function() {
      var cfg;
      cfg = {
        showFL: true,
        showFN: true,
        pageCount: 10,
        resultCount: void 0,
        currPage: 1,
        showPageNum: 5,
        showGotoPage: true
      };
      if (!this.pagination || !this.pagination.resultCount) {
        return;
      }
      if (typeof this.pagination.showFL === "boolean") {
        cfg.showFL = this.pagination.showFL;
      }
      if (typeof this.pagination.showFN === "boolean") {
        cfg.showFN = this.pagination.showFN;
      }
      if (this.pagination.pageCount) {
        cfg.pageCount = this.pagination.pageCount;
      }
      cfg.resultCount = this.pagination.resultCount;
      if (this.pagination.currPage) {
        cfg.currPage = this.pagination.currPage;
        if (cfg.currPage < 1) {
          cfg.currPage = 1;
        }
      }
      if (this.pagination.showPageNum) {
        cfg.showPageNum = this.pagination.showPageNum;
      }
      if (this.pagination.showGotoPage) {
        cfg.showGotoPage = this.pagination.showGotoPage;
      }
      if (this.pagination.gotoPageFun) {
        cfg.gotoPageFun = this.pagination.gotoPageFun;
      }
      cfg.endPage = parseInt(cfg.resultCount / cfg.pageCount);
      if (cfg.resultCount % cfg.pageCount > 0) {
        cfg.endPage = cfg.endPage + 1;
      }
      this.$set("pagination_cfg", cfg);
      return this.$set("pages", genPage(cfg));
    },
    methods: {
      butClick: function(page) {
        if (page.canClick) {
          this.pagination_cfg.currPage = page.targetPage;
          this.$set("pages", genPage(this.pagination_cfg));
          return this.pagination_cfg.gotoPageFun(this.pagination_cfg.currPage);
        }
      }
    }
  });

}).call(this);
