#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado_bz
import json
import time
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
    文件上传相关API
    '''
    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def get(self, parms_str):
        '''
        根据 table_name, column, id 获取已有文件
        '''
        parms = parms_str.split("/")
        self.set_header("Content-Type", "application/json")
        sql = """
            select r.id, f.file_name, f.file_path, f.file_type, f.suffix, 'false' as remove
            from uploaded_file_record_ref r left join uploaded_files f on r.uploaded_file_id = f.id
            where r.ref_table = '%s' and r.ref_column = '%s' and r.ref_record_id = '%s' and r.is_delete != 1 and r.uploaded_file_id is not null
        """ % (parms[0], parms[1], parms[2])
        results = list(self.pg.db.query(sql))
        self.write(json.dumps({'error': '0', 'results': results}))

    @tornado_bz.mustLogin
    @tornado_bz.handleError
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
                    file_path = "/static/uploaded_files/%s_%s_%s" % (self.current_user, int(time.time()), file_name)
                    # hash
                    img = open(file_path, 'w')
                    img.write(file_body)
                    img.close()
                    new_file = storage(file_name=file_name, file_path=file_path, file_hash=file_hash, file_type="file", suffix=file_suffix, seqname='uploaded_files_id_seq')
                    file_id = self.pg.db.insert("uploaded_files", **new_file)
                    r = {
                        'file_id': file_id,
                        'file_name': file_name,
                        'file_path': file_path,
                        'suffix': file_suffix
                    }
                    results.append(r)
        self.write(json.dumps({'error': '0', 'results': results}))


class file_ref(UserInfoHandler):
    """
    create by zhangrui at 15/03/12 14:55
    文件关联方法
    """
    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def post(self):
        """
        保存文件关联
        """
        self.set_header("Content-Type", "application/json")
        parms = json.loads(self.request.body)
        column = parms.get("column")
        new_file_ids = parms.get("new_file_ids")
        table_name = parms.get("table_name")
        record_id = parms.get("record_id")
        remove_file = parms.get("remove_file")
        # 新增文件关联
        results = []
        if new_file_ids:
            for file_id in new_file_ids:
                file_ref = {
                    "uploaded_file_id": file_id,
                    "ref_table": table_name,
                    "ref_record_id": record_id,
                    "ref_column": column,
                    "create_user_id": self.get_current_user()
                }
                ref_id = self.pg.db.insert("uploaded_file_record_ref", seqname='uploaded_file_record_ref_id_seq', **file_ref)
                results.append(ref_id)
        if remove_file:
            self.pg.db.update("uploaded_file_record_ref", where="id = %s" % remove_file, is_delete=1)
        self.write(json.dumps({"error": '0', "results": results}))

if __name__ == '__main__':
    pass
