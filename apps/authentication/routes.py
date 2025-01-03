from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ResetRequestForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, hash_pass


#login
from sqlalchemy.orm.exc import NoResultFound

import json
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from oauthlib.oauth2 import WebApplicationClient
import requests

GOOGLE_CLIENT_ID = '1000259324040-5tk14re9d5caps1c1bf1h7r3vosk8rvj.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@blueprint.route('/google_login')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return '<a class="button" href="/google">Login with Google</a>'

@blueprint.route('/google')
def google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@blueprint.route('/google/callback')
def callback():
    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()

    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )    

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']

    uri,headers,body = client.add_token(userinfo_endpoint)

    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response.json())

    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        users_name = userinfo_response.json()['given_name']
        family_name = userinfo_response.json()['family_name']
    else:
        return "User email not available or not verified by Google.", 400
 
    query = Users.query.filter_by(oauth_github=unique_id)
    try:
        user = query.one()
        login_user(user)

    except NoResultFound:
        usernm = users_name + '_' + family_name
        user = Users(username=usernm, email=users_email, password=unique_id, oauth_github=unique_id)
        db.session.add(user)
        db.session.commit()
        login_user(user)
    
    return redirect(url_for('home_blueprint.index'))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# Akhir

@blueprint.route('/')
def route_default():
    return render_template('home/homepage.html')

@blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    if ("email" in request.args) and ("id" in request.args):
        email = request.args.get('email', None)
        user = Users.query.filter_by(email=email).first() 
        id = request.args.get('id', None)
        if (id is None) or (email is None):
            req_form = ResetRequestForm(request.form)
            return render_template('accounts/req_reset.html', form=req_form, msg='Link tidak valid')
        elif user:
            if user.id == int(id):
                return render_template('accounts/reset.html', email=email)
            else:
                req_form = ResetRequestForm(request.form)
                return render_template('accounts/req_reset.html', form=req_form, msg='Link tidak valid')
        else:
            req_form = ResetRequestForm(request.form)
            return render_template('accounts/reset.html', form=req_form, msg='Email tidak terdaftar')
    req_form = ResetRequestForm(request.form)
    return render_template('accounts/req_reset.html', form=req_form, msg='Silahkan ajukan permintaan ganti password')

@blueprint.route('/req_reset', methods=['GET', 'POST'])
def req_reset():
    req_form = ResetRequestForm(request.form)
    if 'req_reset' in request.form:
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        if user:
            id = user.id
            return redirect(f'https://info.ergocust.com/?email={email}&id={id}')
        else:
            return render_template('accounts/req_reset.html', form=req_form, msg='Email tidak terdaftar')
    return render_template('accounts/req_reset.html', form=req_form)

@blueprint.route('/reset_g', methods=['GET', 'POST'])
def reset_g():
    if ("email" in request.args) and ("id" in request.args):
        email = request.args.get('email', None)
        user = Users.query.filter_by(email=email).first() 
        id = request.args.get('id', None)
        if (id is None) or (email is None):
            req_form = ResetRequestForm(request.form)
            return render_template('accounts/req_reset.html', form=req_form, msg='Link tidak valid')
        elif user:
            if user.id == int(id):
                return render_template('accounts/reset.html', email=email)
            else:
                req_form = ResetRequestForm(request.form)
                return render_template('accounts/req_reset_g.html', form=req_form, msg='Link tidak valid')
        else:
            req_form = ResetRequestForm(request.form)
            return render_template('accounts/reset_g.html', form=req_form, msg='Email tidak terdaftar')
    req_form = ResetRequestForm(request.form)
    return render_template('accounts/req_reset_g.html', form=req_form, msg='Silahkan ajukan permintaan ganti password')

@blueprint.route('/req_reset_g', methods=['GET', 'POST'])
def req_reset_g():
    req_form = ResetRequestForm(request.form)
    if 'req_reset' in request.form:
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        if user:
            id = user.id
            return redirect(f'https://info.ergocust.com/?email={email}&id={id}')
        else:
            return render_template('accounts/req_reset_g.html', form=req_form, msg='Email tidak terdaftar')
    return render_template('accounts/req_reset_g.html', form=req_form)

@blueprint.route('/gantips', methods=['GET', 'POST'])
def gantips():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).one()
        password = hash_pass(password)
        user.password = password
        db.session.commit()
        return render_template('home/berhasil.html')
    else:
        return render_template('accounts/req_reset.html')

@blueprint.route('/berhasil')
def berhasil():
    return render_template('home/berhasil.html')

# Login & Registration


@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        # we can have here username OR email
        user_id = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.find_by_username(user_id)

        # if user not found
        if not user:

            user = Users.find_by_email(user_id)

            if not user:
                return render_template('accounts/login.html',
                                       msg='Username atau Email tidak diketahui',
                                       form=login_form)

        # Check the password
        if verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Username atau password salah',
                               form=login_form)

    elif current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('accounts/login.html',
                               form=login_form)
        


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username sudah terdaftar',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email sudah terdaftar',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='Akun berhasil dibuat. Silahkan masuk',
                               success=True,
                               form=create_account_form)
    elif current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('accounts/register.html',
                               form=create_account_form)
    

@blueprint.route('/masuk', methods=['GET', 'POST'])
def masuk():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        # we can have here username OR email
        user_id = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.find_by_username(user_id)

        # if user not found
        if not user:

            user = Users.find_by_email(user_id)

            if not user:
                return render_template('accounts/masuk.html',
                                       msg='Username atau Email tidak diketahui',
                                       form=login_form)

        # Check the password
        if verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/masuk.html',
                               msg='Username atau password salah',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/masuk.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/daftar', methods=['GET', 'POST'])
def daftar():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/daftar.html',
                                   msg='Username sudah terdaftar',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/daftar.html',
                                   msg='Email sudah terdaftar',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/daftar.html',
                               msg='Akun berhasil dibuat. Silahkan masuk',
                               success=True,
                               form=create_account_form)
    if not current_user.is_authenticated:
        return render_template('accounts/daftar.html',
                               form=create_account_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
