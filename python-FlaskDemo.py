from flask import Flask, render_template
from flask_script import Manager

from livereload import Server
from flask.ext.bootstrap import Bootstrap
# 日期和时间-3.6
from flask_moment import Moment
from datetime import datetime

# 表单类-4-2
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# 重定向和用户会话-4-5
from flask import redirect, session,url_for

# Flash消息-4-6
from flask import flash

app = Flask(__name__)
app.debug = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# 表单类class
class NameForm(Form):
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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('好像你修改了你的名字呢！')
        session['name'] = form.name.data
        return redirect(url_for('index'))

    return render_template('index.html',form = form, name = session.get('name'),
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
