# FlaskDemo
[TOC]

# 资源

作者的github主页
https://github.com/miguelgrinberg/flasky/tree/3d

写的不错的总结
https://github.com/Junctionzc/flask-blog

# 第一章 virtualenv
没什么可说的，就是virtualenv，不过没必要，我就没用这个了。

 git，关联，倒是费了点时间

http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013752340242354807e192f02a44359908df8a5643103a000
http://rogerdudler.github.io/git-guide/index.zh.html

 简单来说， 先在github新建一个repo。
 然后本地目录，新建一个文件夹。
 git init
然后remote，关联起来。
然后pull 把文件复制过来。
这里有个强制性问题存在，stackoverflow 有。
然后push origin master。

为啥呢，因为pycharm新建一个flask的时候，不知道为啥新建一堆 idea文件夹。

# 第二章 程序的基本结构

程序最开始只有一个py文件。
引用。程序名称。路由，加上启动。就这四个最基本的结构。

## 2.2 路由和视图函数

蛮简单的。看看就可以了。看看从地址传入参数的格式

```python
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name
```

## 2.3 启动服务器

话说，修改代码，然后手动重启，很烦人，debug模式就是自动重启。
很简单

```python
    app.run(debug=True)
```

## 2.5.1 程序和请求上下文
比如说request，多线程的话，request不可能是全局变量。
类似有4个上下文全局变量。
current_app g(临时存储对象)request session

### 2.5.3 请求钩子（不太理解）
有4个
before_first_request 注册一个函数，在处理第一个请求之前进行
before_request 注册一个函数，在每次请求之前运行
after_request 如果没有未处理的异常抛出，在每次请求之后运行。
teardown_request 即使有未处理的异常抛出，也在每次请求之后运行

## 2.6 Flask 扩展
### 2.6.1 Flask-script
这是个命令行解析器。

代码改成了这样子,要主意，app的debug模式还是需要的。



```python
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)
app.debug= True
manager = Manager(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
```

运行命令要改一下。
run-edit configuration -script parameter 里添加
runserver --host 0.0.0.0

这样的话启动命令是
python hello.py runserver --host 0.0.0.0

这里需要注意，0.0.0.0 并不是访问地址，而是任意ip。
也就是说，外网电脑可以使用 a.b.c.d:5000 abcd是本机外网地址。

本机要连接，是用这两个地址
http://localhost:5000/
http://127.0.0.1:5000/

第二章到这里就结束了。

## livereload
但是debug模式，只有重启服务器，并不会刷新浏览器。
查看之后发现livereload 这个东西。

试一下。
暂时获得了成功。但是效果不太好。
举个例子，这个只会刷新主页，而不是其他/user/lll什么的链接。
那这个和手动有什么区别？

姑且算是有用，先记录下吧。

```python
from flask import Flask
from flask_script import Manager

from livereload import Server

app = Flask(__name__)
app.debug= True
manager = Manager(app)

@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*') # 可用正则表达式
    live_server.serve(open_url_delay=True)

@app.route('/')
def hello_world():
    return 'Helloss,World!'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hellos,%s!</h1>' % name


if __name__ == '__main__':
    dev()
    manager.run()
```

# 第三章 模板

业务逻辑和表现逻辑。
表现逻辑放到模板。

## 3.1 jinja2模板引擎
就在templates文件夹里，写html
然后route里传递html名字和变量名

变量名 左边是html占位符，右边是变量

用的是render_template 来return

### 3.1.2 变量

变量可以添加过滤器 比如：
safe这个就不会转义 capitalize 首字母大写 等等

### 3.1.3 控制结构

一共有三种=if else -macro - 继承

第一个很简单：

1. if else

```jinja2
{% if user %}
    Hello， {{user}}
{% else %}
    Hello， stranger！
{% endif %}
```

2. macro

```html
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>

为了重复使用宏，可以保存在单独的文件中，然后在需要使用的模板上导入

{% import 'macro.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>

需要多次重复的模板代码可以写入单独的文件，再包含在所有的片段里，
{% include 'common.html' %}
```

3. 继承
base.html

```python
{% block head %}
    这里添加内容
{% endblock %}

{% extends "base.html" %}
{% block head %}
    可以使用了，如果原来的模板不是空的,那么可以使用
    {{ super }}
{% endblock %}
```


## 3.2 使用flask-bootstrap集成
pip install flask-bootstrap

先去 hello.py 初始化app
from flask.ext.bootstrap import Bootstrap

bootstrap = Bootstrap(app)

再去user.html使用

flask-bootstrap已经定义了模板
所以
{% extends "bootstrap/base.html" %}就可以了
不过如果想在已经有的块里添加东西，比如javascript
就依然用super函数

```html
{% block script %}
{{ super }}
要添加的script
{%end block %}
```

## 3.3 自定义错误页面
404 和500 编写自定义页面

路由先写上，然后html

很简单。就不写了

## 3.4 链接
动态路由-url_for()函数

url_for('index',_external=True)external就是绝对地址
可以传入关键字参数
url_for('index', name='john',_external=True)

## 3.5 静态文件
都在static文件夹里
url_for('static', filename='css/styles.css',_external=True)
这里添加了个浏览器里项目图标。
去作者github里，下图。吓到static文件夹里。
https://github.com/miguelgrinberg/flasky/tree/3d

## 3.6 使用flask-moment 本地化日期和时间
第一步：安装
pip install flask-moment
然后去app注册。
然后在base里，script block引用。这里想要中文的话，添加
{{ moment.lang("zh-CN") }}
然后去index函数。传入data变量
最后去修改index template

第三章结束


# 第四章 Web 表单
pip install flask-wtf

## 4.1 跨站请求伪造保护

为了csrf，需要个秘锁，wtf用这个生成加密令牌，然后用这个判断表单数据的真伪。
这里在hello.py 里app.config['SECRET_KEY'] 来生成。不过不该放在源代码就是了。


## 4.2 表单类
需要先建一个表单类。
引用，然后新建一个NameForm

这里需要注意一下，Required wtforms 3.0里就不用了，使用DataRequired.
还有一些比如email,url等等

## 4.3 把表单渲染成HTML
没什么可说的，bootstrap已经有了自定义的表。
base里引用就是了。

## 4.4 在视图函数中处理表单
这个也很简单，就是修改下路由index函数就是了。
不过让我意外的是，空submit的时候的提示，请填写，这个居然是中文。
在哪里设定的？

## 4.5 重定向和用户会话
如果最后一个是post，那么用户刷新的时候会有问题。
所以后面加一个重定向。
但是这样，表单数据也会消失，所以要把数据保存在session里。

## 4.6 Flash消息
现在route里，添加flash逻辑
然后在base里，渲染flash消息

# 第五章 数据库
这里就需要一个orm了。
之前在廖雪峰的教程里，花了300行代码写过一个orm。
就是把指令换算成数据库语言。

这里使用了Flask-SQLAlchemy
pip install flask-sqlalchemy

使用什么数据库是个问题
mac下没有问题，但是windows下可能会有问题。
而且原来使用的是sqlite。但是实际上肯定要用mysql
试一下吧。
不用sqlite。
windows下，用mysql

## 5.5 配置数据库
首先需要pymysql
然后app config 修改。
命令行启动mysql的办法是
进入mysql/bin目录 cd C:\Program Files\MySQL\MySQL Server 5.7\bin

mysql -u root -p

他妈的，密码居然是www-data

重新安装了mysql。
整个安装过程并没有看到任何设置utf-8的选项。
就此跳过去。

安装的时候，让设置密码。我直接设置了root
安装后，出现两个mysql-还有一个是mysql57。
这都是数据库。
一个是服务器，另一个是客户端。
进入 上面写的57目录，然后启动。就是57客户端。

这里有比较简单的数据库教程。
http://www.runoob.com/mysql/mysql-administration.html

教程里是使用了sqlite，这个会自动创建数据库。
而mysql链接的时候是要提供数据库名字的。
所以必须先见一个数据库。
create database flasky;

show databases;
show tables;



## 5.6 定义模型

这里就是建数据模型了


## 5.7 关系

## 5.8 数据库操作
实际操作试一下。
C:\Users\chn_t\Desktop\coding\python-FlaskDemo>C:\Users\chn_t\AppData\Local\Programs\Python\Python35\python.exe C:\Users\chn_t\Desktop\coding\python-FlaskDemo\Hello.py shell

from Hello import db
db.create_all()
结果出来一个warning
C:\Users\chn_t\AppData\Local\Programs\Python\Python35\lib\site-packages\pymysql\cursors.py:166: Warning: (1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 480")
  result = self._query(query)

应该是utf-8编码问题，不过数据库倒是顺利连接上了。

但是当我db.drop_all()之后，重新createall就没有这个warning了。怪了。
stackoverflow说，是因为mysql的utf8只允许3字节。
而有些字母需要4个字节。
解决办法是修改character_set_server=utf8mb4
这里比较详细
https://mathiasbynens.be/notes/mysql-utf8mb4


```mysql
>>> db.create_all()
>>> admin_role = Role(name='Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name='User')
>>> db.session.add(admin_role)
>>> db.session.commit()
```

赋值之后，添加session，最后commit才算写进去了。

数据库操作无非就是增删改查

**数据库操作**

1.创建表：
```
启动python shell：
(venv) $ python hello.py shell
>>> from hello import db
>>> db.create_all()
```
2.添加一些角色和用户：
```
>>> from hello import Role, User
>>> admin_role = Role(name = 'Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name = 'User')
>>> user_john = User(username='john', role=admin_role)
>>> user_susan = User(username='susan', role=user_role)
>>> user_david = User(username='david', role=user_role)
db.session
```
3.添加到会话并提交会话以把对象写入数据库：
```
>>> db.session.add(admin_role)
>>> db.session.add(user_role)
>>> db.session.add(user_john)

>>> db.session.commit()
也可以一次全部加
>>> db.session.add_all([user_role,user_john,user_susan,user_david])

```

4.查询行：
```
>>> Role.query.all()
>>> User.query.all()
```
5.通过过滤器更精确查询行：
```
>>> User.query.filter_by(role=user_role).all()
```

关于查询的另外一个示例：
```
>>> user_role = Role.query.filter_by(name = 'User').first()
```
以上返回一个更精确的query对象。
```
>>> users = user_role.users
```
`user_role.users`表达式隐含的查询会调用all()返回一个用户列表，但无法指定更精确的查询过滤器。解决方法：修改关系设置，加入`lazy='dynamic'`参数，从而禁止自动查询：
```
class Role(db.Model):
    # ...
    users = db.realtionship('User', backref = 'role', lazy = 'dynamic')
    # ...
```
配置之后，user_role.users会返回一个尚未执行的查询，因此可以在其上添加过滤器：
```
>>> user_role.users.order_by(User.username).all()
```

## 5.9 在视图函数中操作数据库

修改下原来的index函数。
首先查询form里的名字，在数据库里有没有。
如果有，那么session-known设定为知道。
如果没有，那么session里添加名字，并且known设定为假。
然后form名字赋值给session-name。

传递给html模板的是 session name和known参数。

修改html模板
只是增加了一个if else。
如果known那么欢迎再见到，如果不是，欢迎。

## 5.10 集成python shell
每次启动shell，都要导入一遍db什么的太麻烦了。

写个script，其实就是简单的返回一个dict,就是个回掉函数。
为shell 命令注册一个回掉函数

## 5.11 flask-migrate 实现数据迁移
数据迁移的目的是为了当模型改变的时候，保留原来的数据，增量迁移。
到第九章才会变更。现在其实没太大必要。

先安装flask-migrate

然后在Hello里，配置

```python
from flask.ext.migrate import Migrate,MigrateCommand

migrate = Migrate(app)
manager.add_command('db', MigrateCommand)
```

迁移之前，用 python hello.py db init 命令 创建仓库。
会新建一个migrations文件夹
windows里，python和py文件都要写上绝对路径。

创建迁移脚本


1.创建迁移仓库：
```
(venv) $ python hello.py db init
```

2.创建迁移脚本：
```
(venv) $ python hello.py db migrate -m "initial migration"
```
以上会报一个warning：
```
UserWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True to suppress this warning.
```
消除warning的方法：修改`venv/lib/python2.7/site-packages/flask_sqlalchemy/__inin__.py`第797行，将`track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', None)`中的`None`改成`True`。

3.更新数据库：
```
(venv) $ python hello.py db upgrade
```

# 第六章 电子邮件

pip install flask-mail

配置mail参数。



然后配置一下邮件的函数

```python
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = 'qq号码'
app.config['MAIL_PASSWORD'] = '这个就是坑，qq邮箱改了安全设置，第三方客户端，登陆要授权码，而不是密码。'
```

不应该把密码和邮件地址放在自己的文件里,应该在环境里设置才对.

然后注册mail模块

```python
from flask.ext.mail import Mail

mail = Mail(app)
```

测试一下:

```python
from flask_mail import Message
from Hello import mail
msg = Message('test sybhect', sender='267222987@qq.com', recipients=['267222987@qq.com'])
msg.body='text bioy'
msg.html='<b>HTML</b>'
with app.app_context():
    mail.send(msg)


```

一开始总是提示拒绝,代码为mail ConnectionRefusedError: [Errno 61] Connection refused.
死活不行,我突然看到一个答案.
mail = Mail(app)

我把app的config设置在了这一句的前面.
设置后,再放进去.结果就可以了.
就是初始化有问题.

变量如何传递?
原文里是在venv环境下设置的全局变量-储存了用户名和密码.

我首先设置了全局变量.
发现无论在term里还是在console,还是在哪里都是None.

现在有两个思路:

一个是启动的时候,传递variable进去.

还是寻找全局变量呢?

不知道发布的时候会不会有影响.

pycharm里添加变量后,用法是:

```python

app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
```

## 程序中集成发送电子邮件功能

要把send email的功能写成一个函数
在Hello.py里写

```python
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]' # 前缀
app.config['FLASKY_MAIL_SENDER'] = os.environ['MAIL_SENDER'] # 发送人
app.config['FLASKY_ADMIN'] = os.environ['FLASKY_ADMIN']  # 管理员的邮箱

# 发邮件的函数-第六章
def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
```

再修改index函数，当表单接收新名字的时候，发送邮件给管理员邮箱
在index函数里添加这个

```python
            if app.config['FLASKY_ADMIN']:

                send_email(app.config['FLASKY_ADMIN'], 'New User',
                            'mail/new_user', user=user)
```

别忘了再templates里新建一个mail文件夹，再新建两个模板文件

## 异步发送电子邮件


```python
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=['267222987@qq.com'])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
```

发送邮件移到线程里面去执行，缺点是每一个邮件都要新建一个线程不太合适，
改进方法是将send_async_email()函数的操作发给Celery任务队列。
celeryproject.org


