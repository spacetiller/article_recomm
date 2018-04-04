# -*- encoding: utf-8 -*- 编码

import json
import time

from flask import Blueprint
from flask import render_template, flash, redirect, session, url_for, request, abort, g
from app.common.data import db
from app.common.log import logger
from app.modules.article.models.ArticlesSimi import ArticlesSimi

#from flask-sqlalchemy import pagination
#from tenacity import retry
from pyquery import PyQuery as pq

articleRoute = Blueprint('article', __name__, url_prefix='/muu/recommend/article')

@articleRoute.route('/get_simi_ids', methods=['GET', 'POST'])
def get_simi_ids():
    logger.debug("function get_simi_ids __enter__")

    if request.method == 'POST' or request.method == 'GET':
    	#logger.debug(str(request.args)+ str(request.values) + str(request.data)+ str(request.get_json())+ str(request.json))
        logger.debug(request.args)
        item_id = request.values.get('article_id')
        page_size = request.values.get('page_size', 10, type = int)
        page = request.args.get('page', 1, type = int)
        page = page - 1

        # check if session cache articles exist
        session.clear()
        article_simi_articles = item_id + "_simi_articles"
        if article_simi_articles in session:
            #logger.debug(session[article_simi_articles])
            article_ids = session[article_simi_articles][page*page_size:(page+1)*page_size]
            end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(article_ids), json.dumps(article_ids))
            logger.debug('simi_articles in session: article %s got articles page %d' % (item_id, page))
            logger.debug(end)
            logger.debug("function get_simi_ids __exit__ 0")
            retstr = json.loads(json.dumps(end.encode('utf-8')))
            return retstr
        else:
            session[article_simi_articles] = []

        item = ArticlesSimi.query.filter(ArticlesSimi.article_id == item_id).first()
        #article = ArticlesSimi()
        #article.username = "title unknown's battle ground"
    
        if not item:
            logger.warning("article not exist, item_id: " + str(item_id))
            end = '{"code": 1006, "msg": "%s" }' % ("请求的文章不存在")
            retstr = json.loads(json.dumps(end.encode('utf-8')))
            logger.debug(retstr)
            logger.debug("function get_simi_ids __exit__ 1")
            return retstr
        #lastids = []
        for article in item.simi_ids.split('|'):
            if article not in session[article_simi_articles]:
                session[article_simi_articles].append(article.encode('utf-8'))
        lastids = session[article_simi_articles][page*page_size:(page+1)*page_size]
        
        #logger.debug(session)
        end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(lastids),json.dumps(lastids))
        retstr = json.loads(json.dumps(end.encode('utf-8')))
        logger.debug('similarity article: ' + str(lastids).encode('utf-8'))
        logger.debug(end)
        logger.debug("function get_simi_ids __exit__ 2")
        return retstr
        #return render_template('private.html', form=form)
    end = '{"code": 1003, "msg": "%s" }' % ("请求方法错误")
    logger.info(end)
    logger.debug("function get_simi_ids __exit__ 3")
    retstr = json.loads(json.dumps(end.encode('utf-8')))
    return retstr

