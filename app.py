from flask import Flask, request, make_response, render_template, redirect, current_app
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask_mail import Mail, Message
from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired
from threading import Thread

import os

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "WHO"
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')
app.config["ME_MAIL_SUBJECT_PREFIX"] = '[Flasky]'
app.config["ME_MAIL_SENDER"] = 'OWASPDE Admin <gi0stratus@gmail.com>'
app.config["ME_ADMIN"] = os.environ.get('OWASPDE_ADMIN')

bootstrap = Bootstrap(app)
manager = Manager(app)
mail = Mail(app)


class ResetForm(Form):
    email = EmailField('Email', validators=[DataRequired()])


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, body, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config["ME_MAIL_SENDER"],
                  recipients=[to])
    msg.body = body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        token = "jbuiepak0934800jd;adkj0134(&$)"
        link = request.url_root + "recover/" + token
        print link
        recipient = form.email.data
        body = link
        subject = "OWASPDE Host Header injection Password Reset"
        send_email(recipient, subject, body)
        return redirect('/')
    return render_template('reset.html', form=form)


@app.route('/recover/<token>', methods=["GET"])
def recover(token):
    if token == "jbuiepak0934800jd;adkj0134(&$)":
        return render_template("success.html")
    return render_template("failure.html")


if __name__ == '__main__':
    manager.run()
