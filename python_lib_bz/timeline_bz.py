#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/02/03 11:39:54 用于存放系统操作的 timeline, 或者更类似于日志. 发起项目:叶脉
'''
from public_bz import storage
import json
import public_bz


class TimeLine():

    '''
    CREATE TABLE timeline
    (
    -- 继承 from table base:  id integer NOT NULL DEFAULT nextval('base_id_seq'::regclass),
    -- 继承 from table base:  created_date timestamp without time zone DEFAULT now(),
    -- 继承 from table base:  stat_date timestamp without time zone DEFAULT now(),
      oper text, -- 执行的动作
      user_id integer, -- 执行的用户
      target_type text, -- 执行的目标对象
      target_id integer, -- 目标的 id, 用于表关联
      other_info json -- 其他的附加信息, 使用 json 来存放
    )
    INHERITS (base)
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE timeline
      OWNER TO yemai;
    COMMENT ON COLUMN timeline.oper IS '执行的动作';
    COMMENT ON COLUMN timeline.user_id IS '执行的用户';
    COMMENT ON COLUMN timeline.target_type IS '执行的目标对象';
    COMMENT ON COLUMN timeline.target_id IS '目标的 id, 用于表关联';
    COMMENT ON COLUMN timeline.other_info IS '其他的附加信息, 使用 json 来存放';
    '''

    def __init__(self, pg):
        self.pg = pg

    def addTimeLine(self, oper, user_id, target_type, target_id, other_info=None):
        timeline = storage()
        timeline.oper = oper
        timeline.user_id = user_id
        timeline.target_type = target_type
        timeline.target_id = target_id
        if other_info:
            timeline.other_info = json.dumps(other_info, cls=public_bz.ExtEncoder)
        return self.pg.db.insert('timeline', **timeline)

    def getTimeLineByTargetID(self, target_type, target_id):
        sql = '''
        select t.*, u.user_name, u.picture from timeline t, user_info u
            where t.user_id = u.id
            and t.target_type = '%s'
            and t.target_id = %s
            order by t.created_date desc
        ''' % (target_type, target_id)
        return self.groupByCreatedDateDay(self.pg.db.query(sql))

    def getTimeLineByToday(self, target_type):
        # and date_trunc('day', t.created_date) = date_trunc('day', now())
        sql = '''
        select t.*, u.user_name, u.picture from timeline t, user_info u
            where t.user_id = u.id
            and t.target_type = '%s'
            order by t.created_date desc
            limit 40
        ''' % (target_type)
        return self.groupByCreatedDateDay(self.pg.db.query(sql))
    def getTimeLineByUserLast40(self, target_type, user_id):
        '''modify by bigzhu at 15/02/25 14:28:14 查询我的时间线,最近40条
        '''
        sql = '''
        select t.*, u.user_name, u.picture from timeline t, user_info u
            where t.user_id = u.id
            and t.user_id=%s
            and t.target_type = '%s'
            order by t.created_date desc
            limit 40
        ''' % (user_id, target_type)
        return self.groupByCreatedDateDay(self.pg.db.query(sql))
    def groupByCreatedDateDay(self, timelines):
        '''
        create by bigzhu at 15/02/03 13:44:24 按照天的精度,归并timeline
        modify by bigzhu at 15/02/06 13:29:58 修改为返回 list 而不是一个 dic, 以便于对时间按天的排序
        '''
        day_time_lines = []
        group_time_line = {}
        for timeline in timelines:
            day = timeline.created_date.strftime('%Y年%m月%d日')
            this_day_timeline = group_time_line.get(day)
            if this_day_timeline:
                #this_day_timeline.insert(0, timeline)
                this_day_timeline.append(timeline)
            else:
                group_time_line[day] = [timeline]
                day_time_lines.append(storage(day = day, timelines = group_time_line[day]))
        return day_time_lines

if __name__ == '__main__':
    pass
