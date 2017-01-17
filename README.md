# FlaskDemo
[TOC]

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