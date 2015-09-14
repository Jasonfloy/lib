#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/07/03 16:39:13 通用的图片上传功能. 兼容 simditor 以及 profile
'''
import hashlib
import public_bz
import tornado_bz
import json
md5 = hashlib.md5()


class upload_image(tornado_bz.BaseHandler):

    '''
    create by bigzhu at 15/07/03 19:59:33
    '''

    def post(self):
        '''
        create by bigzhu at 15/07/03 16:52:52 接收图片文件
        modify by bigzhu at 15/07/03 20:27:25 只允许上传一个文件
        '''
        self.set_header("Content-Type", "application/json")
        if self.request.files:
            for file_key, file_contents in self.request.files.items():
                #只取一个文件
                file_content = file_contents[0]
                body = file_content.pop("body")
                file_name = file_content.pop("filename")
                content_type = file_content.pop("content_type")
                print content_type
                if content_type not in( 'image/jpeg', 'image/png', 'image/svg'):
                    error_info = '只允许上传图片文件'
                    result = {
                        "success": False,
                        "msg": error_info,  # 可选
                    }
                else:
                    file_suffix = file_name[file_name.rfind("."):]
                    md5.update(body)
                    file_hash = md5.hexdigest()
                    file_path = "static/uploaded_files/%s" % (file_hash + file_suffix)
                    real_path = "/" + file_path
                    img = open(file_path, 'w')
                    img.write(body)
                    img.close()
                    result = {
                        "success": True,
                        "msg": "上传失败信息",  # 可选
                        "file_path": real_path
                    }

        self.write(json.dumps(result, cls=public_bz.ExtEncoder))


if __name__ == '__main__':
    pass
