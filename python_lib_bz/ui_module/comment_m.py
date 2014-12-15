
from . import my_ui_module
import time_bz
from public_bz import storage
from tornado_bz import BaseHandler


class comment_m(my_ui_module.MyUIModule):

    '''
    评论,需要传入参数
    comments: 评论组, 包括评论内容,以及评论时间,具体参见 comment 表
    key_type: 一个网站有多个地方有评论时候,用于区分哪个模块,可空
    key: 关键字,一般就是 id, 比如 site_id,定位是哪个东西的评论
    user_info:用户信息,发评论的人的信息



    -- Table: comment

    -- DROP TABLE comment;

    CREATE TABLE comment
    (
    -- 继承 from table base:  id integer NOT NULL DEFAULT nextval('base_id_seq'::regclass),
    -- 继承 from table base:  created_date timestamp without time zone DEFAULT now(),
    -- 继承 from table base:  stat_date timestamp without time zone DEFAULT now(),
      key_type text, -- 用于那个类型....
      key text, -- 比如填入 site_id,...
      user_name text, -- 用户名...
      picture text, -- 用户头像...
      comment text, -- 评论
      parent_id integer -- 可空,父节点 id
    )
    INHERITS (base)
    WITH (
      OIDS=FALSE
    );
    COMMENT ON COLUMN comment.user_id IS '填写的用户 id';
    COMMENT ON COLUMN comment.key_type IS '用于那个类型.

    比如一个系统有多个地方都要有评论,则用这个来区别

    为了站点可以填为 site';
    COMMENT ON COLUMN comment.key IS '比如填入 site_id,
    使用这个评论的元素';
    COMMENT ON COLUMN comment.user_name IS '用户名
    可以为空,如果你用 user_id 去关联其他表的话';
    COMMENT ON COLUMN comment.picture IS '用户头像

    可空';
    COMMENT ON COLUMN comment.comment IS '评论';
    COMMENT ON COLUMN comment.parent_id IS '可空,父节点 id';


    '''

    def render(self, comments, key_type, key, user_info):
        parm = storage()
        parm.comments = comments
        parm.key_type = key_type
        parm.key = key
        parm.user_info = user_info

        return self.render_string(self.html_name, parm=parm, timeLen=time_bz.timeLen)


class comment(BaseHandler):

    '''
    公用的评论系统
    key_type 评论的挂载类型
    key 评论的挂载 id
    '''
    def initialize(self):
        BaseHandler.initialize(self)
        self.key_type = 'site'
        self.key = 1

    def get(self):
        parm = InitParm(pg, self).getParm()
        sql = '''
        select c.*,u.user_name
        from comment c, user_info u
                where c.user_id=u.id order by created_date
                '''
        comments = list(pg.db.query(sql))

        comments = tree_bz.makeTree(comments)
        key_type = self.key_type
        key = self.key
        self.render(tornado_bz.getTName(self), )

    @tornado_bz.handleError
    def post(self):
        parm = InitParm(pg, self).getParm()

        self.set_header("Content-Type", "application/json")
        comment = json.loads(self.request.body)

        if parm.user_info:
            comment['user_id'] = parm.user_info.id

        pg.db.insert('comment', seqname='base_id_seq', **comment)
        self.write(json.dumps({'error': OK}, cls=public_bz.ExtEncoder))
