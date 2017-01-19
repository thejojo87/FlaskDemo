from flask import Flask, render_template
from flask_script import Manager

from livereload import Server
from flask_bootstrap import Bootstrap
# 日期和时间-3.6
from flask_moment import Moment
from datetime import datetime

# 表单类-4-2
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# 重定向和用户会话-4-5
from flask import redirect, session,url_for

# Flash消息-4-6
from flask import flash

# 数据库-5-5
from flask_sqlalchemy import SQLAlchemy
import os

# 数据库-shell-5-10
from flask_script import Shell

# 数据库迁移-5-11
from flask.ext.migrate import Migrate,MigrateCommand


app = Flask(__name__)
app.debug = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# 数据库配置-不知道对不对
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:root@localhost/flasky'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app)
manager.add_command('db', MigrateCommand)


# 为shell命令注册个回调函数
def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role)
manager.add_command("shell", Shell(make_context = make_shell_context))


#数据库模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# 表单类class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')  # 可用正则表达式
    live_server.serve(open_url_delay=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    # return 'Hello,World!'
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))

    return render_template('index.html',form = form, name = session.get('name'),
                           known = session.get('known',False),current_time=datetime.utcnow())


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
