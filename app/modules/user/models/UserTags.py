# -*- encoding: utf-8 -*-

from app.common.data import db

class UserTags(db.Model):
    """
    文章实体信息
    
        
    """
    user_id = db.Column('user_id', db.String(50), primary_key=True, comment="用户ID")
    tags = db.Column('tags',db.String(100), comment="标签，以英文竖线隔开")
    create_time = db.Column('create_time',db.String(20), comment="创建时间")
    update_time = db.Column('update_time',db.String(20), comment="更新时间")
    modify_times = db.Column('modify_times',db.Integer, comment="标签更新次数")
    
    __bind_key__ = 'meiyo'
    __tablename__ = 'user_tags'

    def __init__(self, user_id=None, tags="", create_time="", update_time=""):
        """
        初始化对象信息。
        """
        self.user_id = user_id
        self.tags = tags
        self.create_time = create_time
        self.update_time = update_time
        self.modify_times = 0
