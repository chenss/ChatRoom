# -*- coding: utf-8 -*-
import json
class ComplexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):       #格式化日期时间型
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        
        elif isinstance(obj, date):         #格式化日期型
            return obj.strftime('%Y-%m-%d')
        
        else:
            return json.JSONEncoder.default(self, obj)
