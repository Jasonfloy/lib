#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_module import my_ui_module
import tornado_bz

import json
import hashlib
md5 = hashlib.md5()

class simditor_m(my_ui_module.MyUIModule):

    '''
    富文本编辑器
        create by bigzhu at 15/06/28 00:45:09 彩程出品, 目前能找到的最好的
    '''

    def __init__(self, handler):
        my_ui_module.MyUIModule.__init__(self, handler)

        simditor_path = self.LIB_PATH + 'simditor-2.1.14/'
        simditor_script = simditor_path + 'scripts/'
        simditor_styles = simditor_path + 'styles/'
        self.all_js_files += [
            simditor_script + 'module.js',
            simditor_script + 'hotkeys.js',
            simditor_script + 'uploader.js',
            simditor_script + 'simditor.js',
        ]
        self.all_css_files += [
            simditor_styles + 'simditor.css',
        ]

    def render(self, html=True):
        if html:
            return self.render_string(self.html_name)
        else:
            return ''
    def css_files(self):
        return self.all_css_files

class upload_file(tornado_bz.BaseHandler):
    '''
    create by zhangrui at 15/03/12 14:50
    文件上传相关API
    '''
    def post(self):
        '''
        新增文件
        '''
        global md5
        self.set_header("Content-Type", "application/json")
        results = []
        if self.request.files:
            for i in self.request.files:
                fd = self.request.files[i]
                for f in fd:
                    file_name = f.get("filename")
                    file_suffix = file_name[file_name.rfind("."):]
                    file_body = f["body"]
                    md5.update(file_body)
                    file_hash = md5.hexdigest()
                    file_path = "static/uploaded_files/%s" % (file_hash+file_suffix)
                    real_path = "/"+file_path
                    # hash
                    img = open(file_path, 'w')
                    img.write(file_body)
                    img.close()
                    #new_file = storage(file_name=file_name, file_path="/" + file_path, file_hash=file_hash, file_type="file", suffix=file_suffix, seqname='uploaded_files_id_seq')
                    result = {
                      "success": True,
                      "msg": "上传失败信息", # 可选
                      "file_path": real_path
                    }
        self.write(json.dumps(result))

if __name__ == '__main__':
    pass
