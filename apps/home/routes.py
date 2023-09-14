# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.home.models import Snisub, Janji, Profile
from apps.authentication.models import Users
from apps import db


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            nama = request.form.get('nama')
            pekerjaan = request.form.get('pekerjaan')

            profile = Profile(username=username, email=email,
                              nama=nama, pekerjaan=pekerjaan)
            db.session.add(profile)
            db.session.commit()
            flash("Berhasil tersimpan")
            return render_template('home/profile.html', segment='profile', profile=profile)
        else:
            profile = Profile.query.filter_by(
                email=current_user.email).order_by(Profile.id.desc()).first()
            return render_template('home/profile.html', segment='profile', profile=profile)
    except:
        return render_template('home/profile.html', segment='profile')


@blueprint.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def hapusakun(username):
    try:
        if request.method == 'POST':
            konfirmasi = request.form.get('konfirmasi')
            konfirmasi = konfirmasi.lower()
            if konfirmasi == "hapus akun":
                hapus = Users.query.filter_by(username=username).one()
                db.session.delete(hapus)
                db.session.commit()
                flash("Akun berhasil dihapus!")
                return redirect('/logout')
            else:
                profile = Profile.query.filter_by(
                    email=current_user.email).order_by(Profile.id.desc()).first()
                return render_template('home/profile.html', segment='profile', profile=profile)
    except:
        return render_template('home/profile.html', segment='profile')


@blueprint.route('/snisub', methods=['GET', 'POST'])
@login_required
def snisub():
    if request.method == 'POST':
        perusahaan = request.form.get('perusahaan')
        nama = request.form.get('nama')
        posisi = request.form.get('posisi')
        email = request.form.get('email')
        n1 = request.form.get('1')
        n2 = request.form.get('2')
        n3 = request.form.get('3')
        n4 = request.form.get('4')
        n5 = request.form.get('5')
        n6 = request.form.get('6')
        n6 = request.form.get('6')
        n7 = request.form.get('7')
        n8 = request.form.get('8')
        n9 = request.form.get('9')
        n10 = request.form.get('10')
        n11 = request.form.get('11')
        n12 = request.form.get('12')
        n13 = request.form.get('13')
        n14 = request.form.get('14')
        n15 = request.form.get('15')
        n16 = request.form.get('16')
        n17 = request.form.get('17')
        n18 = request.form.get('18')
        n19 = request.form.get('19')
        n20 = request.form.get('20')
        n21 = request.form.get('21')
        n22 = request.form.get('22')
        n23 = request.form.get('23')

        sni = Snisub(perusahaan=perusahaan, nama=nama, posisi=posisi, email=email, n1=n1, n2=n2, n3=n3, n4=n4, n5=n5, n6=n6, n7=n7, n8=n8, n9=n9,
                     n10=n10, n11=n11, n12=n12, n13=n13, n14=n14, n15=n15, n16=n16, n17=n17, n18=n18, n19=n19, n20=n20, n21=n21, n22=n22, n23=n23)
        db.session.add(sni)
        db.session.commit()
        flash("Berhasil tersimpan")
        return render_template('home/snisub.html', segment='snisub', sni=sni)
    elif "lihat" in request.args:
        id = request.args.get("lihat")
        lihat = Snisub.query.filter_by(id=id).one()
        return render_template('home/snisub.html', segment='snisub', sni=lihat)
    return render_template('home/sni.html', segment='sni')


@blueprint.route('/hasil', methods=['GET', 'POST'])
@login_required
def hasil():
    if "email" in request.args:
        email = request.args.get("email")
        list = Snisub.query.filter_by(email=email).all()
    elif "hapus" in request.args:
        hapus = request.args.get("hapus")
        hapus_sni = Snisub.query.filter_by(id=hapus).one()
        email = hapus_sni.email
        db.session.delete(hapus_sni)
        db.session.commit()
        flash("Berhasil dihapus")
        return redirect(f'/hasil?email={email}')
    else:
        list = Snisub.query.all()
    return render_template('home/hasil.html', segment='hasil', sni=list)


@blueprint.route('/janji', methods=['GET', 'POST'])
@login_required
def janji():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        hp = request.form.get('hp')
        tgl = request.form.get('tgl')

        janji = Janji(nama=nama, email=email, hp=hp, tgl=tgl)
        db.session.add(janji)
        db.session.commit()
        flash("Berhasil tersimpan. Akan dihubungi dalam waktu 24 jam")

        return render_template('home/janji.html', segment='janji', janji=janji)
    return render_template('home/konsultasi.html', segment='konsultasi')


@blueprint.route('/jadwal', methods=['GET', 'POST'])
def jadwal():
    if "email" in request.args:
        email = request.args.get("email")
        list = Janji.query.filter_by(email=email).all()
    elif "hapus" in request.args:
        hapus = request.args.get("hapus")
        hapus_konsultasi = Janji.query.filter_by(id=hapus).one()
        email = hapus_konsultasi.email
        db.session.delete(hapus_konsultasi)
        db.session.commit()
        flash("Berhasil dihapus")
        return redirect(f'/jadwal?email={email}')
    else:
        list = Janji.query.all()
    return render_template('home/jadwal.html', segment='jadwal', janji=list)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit = Janji.query.filter_by(id=id).one()
    if request.method == 'POST':
        edit.nama = request.form.get('nama')
        edit.hp = request.form.get('hp')
        edit.tgl = request.form.get('tgl')
        db.session.commit()
        flash("Berhasil diubah")
        return redirect(f'/jadwal?email={edit.email}')
    return render_template('home/edit_konsultasi.html', segment='edit_konsultasi', edit=edit)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
