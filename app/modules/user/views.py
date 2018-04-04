# -*- encoding: utf-8 -*- 编码

import json
import random
import string

from flask import Blueprint
from flask import render_template, flash, redirect, session, url_for, request, abort, g
#from flask_login import login_user, logout_user, login_required, current_user
#from app import login_manager
#from app.utils.encrypt import md5
from app.common.data import db
from app.common.log import logger
from app.modules.user.models.UserTags import UserTags
from app.modules.user.models.TagArticles import TagArticles

#from tenacity import retry
from time import time as timestamp

userRoute = Blueprint('user', __name__, url_prefix='/muu/recommend/user')

PAGESIZE = 10
#TAGARTICLESLEN = 30

@userRoute.route('/add_tags', methods=['GET', 'POST'])
def add_user_tags():
    logger.debug("function add_user_tags __enter__")
    #print (request.args)
    if request.method == 'POST' or request.method == 'GET':
        user_tags = UserTags()
        user_tags.user_id = request.values.get("user_id", '', type=str)        # user_id
        user_tags.tags = request.values.get("tags", '', type=str).replace(',','|')    # tags
        user_tags.create_time = timestamp()
        user_tags.update_time = timestamp()
        
        ut = UserTags.query.filter(UserTags.user_id == user_tags.user_id).first()
        if ut:
            logger.info("user exist, update. user_id: " + str(ut.user_id))
            ut.user_id = user_tags.user_id
            ut.tags = user_tags.tags.replace(',','|')
            ut.update_time = user_tags.update_time
            if 'user_tags_update_times' in session:
                session['user_tags_update_times'] = session['user_tags_update_times'] + 1
            else:
                session['user_tags_update_times'] = 1
            ut.modify_times = session['user_tags_update_times']
            #ut.session.add()
            db.session.commit()
            end = '{"code": 1000, "msg": "%s" }' % ("用户标签已更新。")
            return json.loads(json.dumps(end)) 
        else:
            db.session.add(user_tags)
            db.session.commit()
            logger.info("user tags added, user_id: " + str(user_tags.user_id))
            end = '{"code": 1000, "msg": "%s" }' % ("用户标签已添加。")
            return json.loads(json.dumps(end))
    logger.warning("error, GET/POST wrong. ")
    end = '{"code": 1003, "msg": "%s" }' % ("请求方法不正确。")
    retstr = json.loads(json.dumps(end.encode('utf-8')))
    return retstr

def _get_default_recomm_articles(page, page_size = 10):
    logger.debug("function _get_default_recomm_articles __enter__")
    
    if not str(page).isdigit():
        return []
    #import random
    #offset = random.randint(0,300)
    #user_id = request.args.get('user_id', 1, type = int)
    #logger.debug('user id: ' + str(user_id))
    if 'default_articles' in session:
        return session['default_articles'][page*page_size:(page+1)*page_size]
    else:
        session['default_articles'] = []
    
        utags = TagArticles.query.all() #limit(1).offset(page) #(page-1)*PAGESIZE
    
        if utags:
            articles = {}
            retids = []
            for utag in utags:
                for article in utag.article_ids.split('|'):
                #set([]).issubset(s)
                    artids = article.split(':')
                    uid = artids[0].encode('utf-8')
                    uval = artids[1]
                    #if not set([uid]).issubset(session['hit_articles']):
                    #    session['hit_articles'].add(uid)
                    #articles[uid] = uval
                    #retids.append(uid)
                    if uid not in session['default_articles']:
                        session['default_articles'].append(uid)
                #logger.debug(articles)
            logger.debug("default articles array, total: " + str(len(session['default_articles'])))
            if page != 0:
                logger.warning("page is not 0: " + str(page))
            logger.debug("function _get_default_recomm_articles __exit__")
            return session['default_articles'][page*page_size:(page+1)*page_size]
        return []
    return ['1']    # untouchable land
    
@userRoute.route('/get_recomm_articles', methods=['GET', 'POST'])
def get_user_recomm_articles():
    logger.debug("function get_user_recomm_articles __enter__")

    if request.method == 'POST' or request.method == 'GET':
        logger.debug(str(request.args) + '\n' + str(request.values) + '\n'  + str(request.data) + '\n' + str(request.get_json()) + '\n' + str(request.json))
        user_id = request.values.get('user_id', '', type=str)
        page_size = request.values.get('page_size', 10, type = int)
        page = request.values.get('page', 1, type = int)
        #if not page_size or not str(page_size).isdigit():
        #    page_size = 10
        #if not page or not str(page).isdigit():
        #    page = 1
        page = page - 1        # page start with 1, mysql db offset start with 0
        logger.debug(request.values)
        #session.clear()

        # check if session cache articles exist
        session.clear()
        user_recomm_articles = user_id + "_recomm_articles"
        if user_recomm_articles in session:
            #logger.debug(session)
            article_ids = session[user_recomm_articles][page*page_size:(page+1)*page_size]
            end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(article_ids), json.dumps(article_ids))
            logger.debug('recomm_articles in session: user %s got articles page %d' % (user_id, page))
            logger.debug("function get_user_recomm_articles __exit__ 0")
            retstr = json.loads(json.dumps(end.encode('utf-8')))
            return retstr
        else:
            session[user_recomm_articles] = []

        # get user's tags
        utag = UserTags.query.filter(UserTags.user_id == user_id).first()
        if not utag:
            logger.warning("user-tags not exist, user_id: " + str(user_id))
            article_ids = _get_default_recomm_articles(page)
            end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(article_ids), json.dumps(article_ids))
            logger.debug(end)
            logger.debug("function get_user_recomm_articles __exit__ 1")
            retstr = json.loads(json.dumps(end.encode('utf-8')))
            return retstr
        articles = {}
        tags = utag.tags
        logger.debug('User tags found for ' + str(user_id) + ': ' + tags)
        empty_num = 0
        tags_arr = tags.split('|')
        for tag in tags_arr:
            if not tag:
                empty_num += 1
                logger.debug('Empty tag ' + str(tag))
                if empty_num == tags_arr.len:
                    article_ids = _get_default_recomm_articles(page)
                    end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(article_ids), json.dumps(article_ids))
                    logger.debug(end)
                    logger.debug("function get_user_recomm_articles __exit__ 2")
                    retstr = json.loads(json.dumps(end.encode('utf-8')))
                    return retstr
                continue
            tagarticle = TagArticles.query.filter(TagArticles.tag == tag).first()
            if not tagarticle:
                empty_num += 1
                logger.debug('No article found for tag ' + str(tag))
                if empty_num == tags_arr.len:
                    article_ids = _get_default_recomm_articles(page)
                    end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(article_ids), json.dumps(article_ids))
                    logger.debug(end)
                    logger.debug("function get_user_recomm_articles __exit__ 2")
                    retstr = json.loads(json.dumps(end.encode('utf-8')))
                    return retstr
                continue
            for article_id in tagarticle.article_ids.split('|'):
                artids = article_id.split(':')
                uid = artids[0].encode('utf-8')
                uval = float(artids[1])
                #if not set([uid]).issubset(session['hit_articles']):
                #    session['hit_articles'].add(uid)
                articles[uid] = uval
        #logger.debug(articles)
        articles = sorted(articles.items(),key = lambda x:float(x[1]),reverse = True)
        logger.debug(articles)
        for article in articles:
            if article[0] not in session[user_recomm_articles]:
                session[user_recomm_articles].append(article[0])
        lastids = session[user_recomm_articles][page*page_size:(page+1)*page_size]
        
        end = '{"code": 1000, "article_num": %d, "article_ids": %s }' % (len(lastids), json.dumps(lastids))
        retstr = json.loads(json.dumps(end.encode('utf-8')))
        logger.debug('user ' + user_id + ' request article: ' + str(lastids))
        logger.debug(retstr)
        logger.debug("function get_user_recomm_articles __exit__ 3")
        return retstr
        #return render_template('private.html', form=form)
    end = '{"code": 1003, "msg": "%s" }' % ("请求方法错误") 
    logger.info(end)
    logger.debug("function get_user_recomm_articles __exit__ 4")
    retstr = json.loads(json.dumps(end.encode('utf-8')))
    return retstr

