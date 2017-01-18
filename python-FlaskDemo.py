from flask import Flask, render_template
from flask_script import Manager

from livereload import Server
from flask.ext.bootstrap import Bootstrap
# 日期和时间-3.6
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
app.debug = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')  # 可用正则表达式
    live_server.serve(open_url_delay=True)


@app.route('/')
def index():
    # return 'Hello,World!'
    return render_template('index.html',
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello,%s!</h1>' % name
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    # dev()
    manager.run()
