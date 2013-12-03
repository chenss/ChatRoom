#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import re
import cgi
import time
import datetime
import json
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Set the debug level
_DEBUG = True


class User(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    joined = db.DateTimeProperty(auto_now_add=True)
    picture = db.StringProperty()

class Msg(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    time = db.DateTimeProperty(auto_now_add=True)
    message = db.StringProperty()


class BaseRequestHandler(webapp2.RequestHandler):
    ''' 
        BaseRequestHandler负责从数据库查询聊天记录并返回到客户端，
        包括第一次打开一次性返回100条记录，及之后对每次请求返回最新
        记录.
    '''
    def getChats(self, last_request_time):
        
        if(last_request_time == datetime.datetime(1970,1,1,0,0,0,0)):
            msg_query = db.GqlQuery("SELECT * FROM Msg ORDER BY time DESC LIMIT 100").fetch(100)     # GqlQuery --> Query
            msg_query.reverse()
        else:
            msg_query = db.GqlQuery("SELECT * FROM Msg WHERE time > :1 ORDER BY time", last_request_time)
            
        msgs = [{'user': str(msg.user), 'time': str(msg.time), 'message': msg.message} for msg in msg_query]
        msgs = json.dumps(msgs)
        
        self.response.write(msgs)


        
class MainRequestHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            log_in_out_url = users.create_logout_url(self.request.uri)
            link_text = 'Logout'
            home = '/home?user_id=' + user.user_id()
        else:
            log_in_out_url = users.create_login_url(self.request.uri)
            link_text = 'Login'
            home = log_in_out_url
            
        template_values = {
            'home': home,
            'user': user,
            'log_in_out_url': log_in_out_url,
            'link_text': link_text,
        }

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'chat.html')
        self.response.write(template.render(path, template_values))
        

class ChatsRequestHandler(BaseRequestHandler):

    def strToDatetime(self, str):
        array = re.split('[^\d]', str)
        try:
            for i in range(len(array)):
                array[i] = int(array[i])
            
            date_time = datetime.datetime(array[0], array[1], array[2], array[3], array[4], array[5], array[6])
        except:
            date_time = datetime.datetime.now()+datetime.timedelta(seconds = -5)    #五秒之前

        return date_time

    def get(self):
        last_request_time = self.strToDatetime(self.request.get('time'))
        self.getChats(last_request_time)

    def post(self):
        ms = Msg()
        ms.message = cgi.escape(self.request.get('data'))
        ms.put()

        last_request_time = self.strToDatetime(self.request.get('time'))
        self.getChats(last_request_time)

class UserHomePageHandler(webapp2.RequestHandler):
    def get(self):
        pass

app = webapp2.WSGIApplication([
    ('/', MainRequestHandler),
    ('/getchats', ChatsRequestHandler),
    ('/home', UserHomePageHandler),
], debug=True)
