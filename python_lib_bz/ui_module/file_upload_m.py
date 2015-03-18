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


md5 = hashlib.md5()


class file_upload_m(my_ui_module.MyUIModule):

    '''
    create by zhangrui at 15/03/12 14:29
    上传文件功能
    '''

    def render(self):
        return self.render_string(self.html_name)

    def javascript_files(self):
        pass


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
        global md5
        self.set_header("Content-Type", "application/json")
        if self.request.files:
            results = []
            for i in self.request.files:
                fd = self.request.files[i]
                for f in fd:
                    file_name = f.get("filename")
                    file_suffix = file_name[file_name.rfind("."):]
                    file_body = f["body"]
                    md5.update(file_body)
                    file_hash = md5.hexdigest()
                    file_path = "static/uploaded_files/%s_%s_%s" % (self.current_user, int(time.time()), file_name)
                    # hash
                    img = open(file_path, 'w')
                    img.write(file_body)
                    img.close()
                    new_file = storage(file_name=file_name, file_path=file_path, file_hash=file_hash, file_type="file", suffix=file_suffix, seqname='id_base_seq')
                    file_id = self.pg.db.insert("uploaded_files", **new_file)
                    r = {
                        'file_id': file_id,
                        'file_name': file_name,
                        'file_path': "/" + file_path,
                        'suffix': file_suffix
                    }
                    results.append(r)
            self.write(json.dumps({'error': 0, 'results': results}))


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
        保存文件关联
        """
        self.set_header("Content-Type", "application/json")
        parms = json.loads(self.request.body)
        column = parms.get("column")
        append_files = parms.get("append_files")
        remove_files = parms.get("remove_files")
        table_name = parms.get("table_name")
        record_id = parms.get("record_id")
        # 新增文件关联
        if append_files:
            for f in append_files:
                file_ref = {
                    "uploaded_file_id": f.get("file_id"),
                    "ref_table": table_name,
                    "ref_record_id": record_id,
                    "ref_column": column,
                    "create_user_id": self.get_current_user()
                }
                self.pg.db.insert("uploaded_file_record_ref", **file_ref)
        if remove_files:
            self.pg.db.update("uploaded_file_record_ref", where="id in (%s)" % ','.join(map(str, remove_files)), is_delete="T")
        self.write(json.dumps({"error": 0}))

if __name__ == '__main__':
    pass
