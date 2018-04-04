# -*- encoding: utf-8 -*-

from app.common.data import db


class TagArticles(db.Model):
    """
    标签-相关文章模型

        
    """
    id = db.Column('id', db.Integer, primary_key=True, comment="自增ID")
    tag = db.Column(db.String(50), comment="一个标签")
    article_ids = db.Column(db.Text, comment="相关文章ID列表，以|分隔")
    id_num = db.Column(db.Integer, comment="相关文章ID总数")
    
    __bind_key__ = 'meiyo'
    __tablename__ = 'tag_articles'

    def __init__(self, tag="", article_ids="", id_num=0):
        """
        初始化对象信息。
        """
        self.tag = tag
        self.article_ids = article_ids
        self.id_num = id_num

