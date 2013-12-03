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
import datetime
import json
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Msg(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    time = db.DateTimeProperty(auto_now_add=True)
    message = db.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            log_in_out_url = users.create_logout_url(self.request.uri)
            link_text = "Logout"
        else:
            log_in_out_url = users.create_login_url(self.request.uri)
            link_text = "Login"
            
        msgs = db.GqlQuery("SELECT * FROM Msg ORDER BY time LIMIT 100")

        template_values = {
            'user': user,
            'log_in_out_url': log_in_out_url,
            'link_text': link_text,
            'msgs': msgs, 
        }

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'index.html')
        self.response.write(template.render(path, template_values))
        

class ChatsHandler(webapp2.RequestHandler):
    def get(self):
        lastest_message_time = datetime.datetime.now()+datetime.timedelta(seconds = -5)         # five seconds before
        msg_query = db.GqlQuery("SELECT * FROM Msg WHERE time >= :last_get_message ORDER BY time")
        msg_query.bind(last_get_message = lastest_message_time)
            
        msgs = [{'user': str(msg.user), 'time': str(msg.time), 'message': msg.message} for msg in msg_query]
        data = json.dumps(msgs)
        
        self.response.write(data)

    def post(self):
        ms = Msg()
        ms.message = self.request.get('data')
        ms.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getchats', ChatsHandler),
], debug=True)
