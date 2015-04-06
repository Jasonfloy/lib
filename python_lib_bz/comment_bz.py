#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/02/22 14:36:50 评论相关的一些操作
'''

import tree_bz


def createTable(db_name):
    '''
    create by bigzhu at 15/04/06 20:36:55 依赖的数据模型
    '''
    import model_bz
    import model_oper_bz
    model_oper_bz.createTable(model_bz.comment, db_name)


class Comment():

    '''
    '''

    def __init__(self, pg):
        self.pg = pg

    def getComment(self, key_type, key):
        sql = '''
        select c.*,u.user_name, u.picture
        from comment c, user_info u
                where c.user_id=u.id
                and c.key_type='%s'
                and c.key='%s'
                order by created_date
                    ''' % (key_type, key)

        comments = list(self.pg.db.query(sql))
        return tree_bz.makeTree(comments)

    def addComment(self, comment, parent_id, user_id, key_type=None, key=None):
        return self.pg.db.insert('comment', seqname='base_id_seq', key_type=key_type, key=key, comment=comment, parent_id=parent_id, user_id=user_id)
if __name__ == '__main__':
    pass
