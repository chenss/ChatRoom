MainHandler由在template中添加100条记录改为appendchild 100条记录

优点：	统一数据传递格式（Json）
	优化响应时间 先显示界面，再显示聊天记录

添加BaseHandler类，处理上述功能。MainHandler和ChatsHandler继承此类


GAE：技术成熟 文档，书籍较多 SDK功能完整 国内能够访问，但速度较慢
python: GAE默认语言 文档丰富 示例程序较多
webapp2: 功能简单易学 GAE自带框架 文档丰富
json: javascript/python中使用方便，减少网络传输。


体会：勤于测试，每做一项修改就测试一次，早测试早发现BUG。

问题：前台后台数据格式不统一
数据库中：   2013-11-16 01:22:21.568030   datetime.datetime类型    datetime.datetime(2013, 11, 16, 01, 22, 21, 568030)
网页中显示： 2013-11-20 08:15:47.585000   string类型		   '2013-11-20 08:15:47.585000'
解决方法： str(数据库）=== 网页中显示
