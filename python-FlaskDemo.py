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
