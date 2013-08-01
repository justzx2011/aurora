from __future__ import absolute_import

from flask import Flask, render_template, url_for, g, request, redirect
from flask.ext.login import LoginManager, current_user
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.gravatar import Gravatar

app = Flask(__name__)
app.config.from_object('settings')

# Enable login manager extension
login_manager = LoginManager()
login_manager.setup_app(app)

# Enable debug toolbar
toolbar = DebugToolbarExtension(app)

# Enable gravatar
gravatar = Gravatar(app, default='identicon', rating='g')

# Make Aurora folders if not exists
from aurora_app.helpers import create_folder
create_folder(app.config['AURORA_PATH'])
create_folder(app.config['AURORA_PROJECTS_PATH'])
create_folder(app.config['AURORA_TMP_DEPLOYMENTS_PATH'])


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    from aurora_app.database import db
    db.session.rollback()
    return render_template('500.html'), 500


@app.before_request
def check_login():
    g.user = current_user if current_user.is_authenticated() else None

    if (request.endpoint and request.endpoint != 'static' and
       (not getattr(app.view_functions[request.endpoint], 'is_public', False)
       and g.user is None)):
        return redirect(url_for('main.login', next=request.path))

from aurora_app.views import (main, projects, stages, tasks, notifications,
                              deployments, users)

app.register_blueprint(main.mod)
app.register_blueprint(projects.mod)
app.register_blueprint(stages.mod)
app.register_blueprint(tasks.mod)
app.register_blueprint(notifications.mod)
app.register_blueprint(deployments.mod)
app.register_blueprint(users.mod)


# Enable context processors
import aurora_app.context_processors
