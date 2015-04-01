#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/02/22 14:36:50 评论相关的一些操作
'''

import tree_bz
sql = '''
    -- Table: comment

    -- DROP TABLE comment;

    CREATE TABLE comment
    (
    -- 继承 from table base:  id integer NOT NULL DEFAULT nextval('base_id_seq'::regclass),
    -- 继承 from table base:  created_date timestamp without time zone DEFAULT now(),
    -- 继承 from table base:  stat_date timestamp without time zone DEFAULT now(),
      user_id integer, -- 填写的用户 id
      key_type text, -- 用于那个类型....
      key text, -- 比如填入 site_id,...
      comment text, -- 评论
      parent_id integer -- 可空,父节点 id
    )
    INHERITS (base)
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE comment
      OWNER TO yemai;
    COMMENT ON COLUMN comment.user_id IS '填写的用户 id';
    COMMENT ON COLUMN comment.key_type IS '用于那个类型.

    比如一个系统有多个地方都要有评论,则用这个来区别

    为了站点可以填为 site';
    COMMENT ON COLUMN comment.key IS '比如填入 site_id,
    使用这个评论的元素';
    COMMENT ON COLUMN comment.comment IS '评论';
    COMMENT ON COLUMN comment.parent_id IS '可空,父节点 id';

'''


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
