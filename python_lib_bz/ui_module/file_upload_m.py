#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado_bz
import json
import time
import tornado
import hashlib
from tornado_bz import UserInfoHandler
from ui_module import my_ui_module
from public_bz import storage


class file_upload_m(my_ui_module.MyUIModule):

    '''
    create by zhangrui at 15/03/12 14:29
    上传文件功能
    '''

    def render(self):
        return self.render_string(self.html_name)


class file_upload(UserInfoHandler):
    '''
    create by zhangrui at 15/03/12 14:50
    文件上传处理方法
    '''
    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def post(self):
        '''
        新增文件
        '''
        self.set_header("Content-Type", "application/json")
        if self.request.files:
            for f in self.request.files:
                file_name = f.get("filename")
                file_suffix = file_name[file_name.index("."):]
                file_path = "static/uploaded_files/%s_%s_%s" % (self.current_user, int(time.time()), file_name)
                file_body = f["body"]
                # hash 用来
                file_hash = hashlib.md5(file_body)
                img = open(file_path, 'w')
                img.write(file_body)
                img.close()
                new_file = storage(file_path=file_path, file_hash=file_hash, file_type="file", suffix=file_suffix, seqname='base_id_seq')
                file_id = self.pg.db.insert("uploaded_files", **new_file)
                self.write(json.dumps({'error': 0, 'file_id': file_id, 'file_name': file_name, 'file_path': file_path}))


class file_ref(UserInfoHandler):
    """
    create by zhangrui at 15/03/12 14:55
    文件关联方法
    """
    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def get(self, offset, limit, file_name):
        """
        获取文件
        url_mapping需要额外注册
        /file_ref/offset/.(*)/limit/.(*)/filename/.(*)
        """

        sql = """
        select id, file_name
        from uploaded_files
        where 1=1
        """
        if file_name:
            sql += " and file like '%%s%'" % file_name
        if offset:
            sql += "\n offset %s" % offset
        if limit:
            sql += "\n limit %s" % limit
        files = list(self.pg.db.query(sql))
        self.write(json.dumps({"error": 0, "files": files}))

    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def post(self):
        """
        新增文件链接
        """
        self.set_header("Content-Type", "application/json")
        parms = json.dumps(self.request.body)
        file_ref = {
            "uploaded_file_id": parms.get("file_id"),
            "ref_table": parms.get("table_name"),
            "ref_record_id": parms.get("record_id"),
            "create_user_id": self.get_current_user()
        }
        self.pg.db.insert("uploaded_file_record_ref", **file_ref)
        self.write(json.dumps({"error": 0}))

if __name__ == '__main__':
    pass
