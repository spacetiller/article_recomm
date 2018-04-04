# -*- encoding: utf-8 -*-

from app.common.data import db


class ArticlesSimi(db.Model):
    """
    	文章相关度

        
    """
    article_id = db.Column('uid', db.Integer, primary_key=True, comment="文章ID")
    simi_ids = db.Column('uid_simi', db.Integer, primary_key=True, comment="相关文章ID列表，以|分隔")

    __bind_key__ = 'meiyo'
    __tablename__ = 'articles_simi'

    def __init__(self, article_id="", simi_ids=""):
        """
        初始化对象信息。
        """
        self.article_id = article_id
        self.simi_ids = simi_ids

