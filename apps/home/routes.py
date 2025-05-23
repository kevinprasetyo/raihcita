from apps.home import blueprint
from flask import render_template, request, flash, redirect, session, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.home.models import Snisub, Janji, Profile
from apps.authentication.models import Users
from apps import db
import json


@blueprint.route('/index')
def index():
    return render_template('home/homepage.html', segment='index')


@blueprint.route('/choosetutor', methods=['GET', 'POST'])
def choosetutor():
    if "class" in request.args:
        class_name = request.args.get("class")
    else:
        class_name = "Raih Cita"
    return render_template('home/choose-tutor.html', tutor=class_name)


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
@login_required
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
@login_required
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


@blueprint.route('/privasi')
def privasi():
    return render_template('home/privasi.html', segment='privasi')


@blueprint.route('/<template>')
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


with open('apps/templates/toefl/questions.json') as f:
    QUESTIONS = json.load(f)


@blueprint.route('/learning/<template>')
def learning_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("learning/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/learning/toefl/listening')
def toefllistening2():
    return render_template('learning/toefl/listening.html', questions=QUESTIONS)


@blueprint.route('/learning/toefl/listening-result', methods=['POST'])
def hasiltoefllistening2():
    user_answers = request.form
    score = 0
    results = []

    for question in QUESTIONS:
        qid = str(question['id'])
        correct = question['answer']
        user_answer = int(user_answers.get(qid, -1))

        results.append({
            'question': question['question'],
            'choices': question['choices'],
            'correct_answer': question['choices'][correct],
            'your_answer': question['choices'][user_answer] if user_answer != -1 else "No answer",
            'is_correct': user_answer == correct
        })

        if user_answer == correct:
            score += 1

    return render_template('learning/toefl/listening-result.html', score=score, total=len(QUESTIONS), results=results)


@blueprint.route('/toefl-listening')
def toefllistening():
    return render_template('home/toefl-listening.html', questions=QUESTIONS)


@blueprint.route('/hasil-toefl-listening', methods=['POST'])
def hasiltoefllistening():
    user_answers = request.form
    score = 0
    results = []

    for question in QUESTIONS:
        qid = str(question['id'])
        correct = question['answer']
        user_answer = int(user_answers.get(qid, -1))

        results.append({
            'question': question['question'],
            'choices': question['choices'],
            'correct_answer': question['choices'][correct],
            'your_answer': question['choices'][user_answer] if user_answer != -1 else "No answer",
            'is_correct': user_answer == correct
        })

        if user_answer == correct:
            score += 1

    return render_template('home/hasil-toefl-listening.html', score=score, total=len(QUESTIONS), results=results)


with open('apps/templates/toefl/structure.json') as f:
    STRUCTURE = json.load(f)


@blueprint.route('/learning/toefl/structure')
def quiz2():
    return render_template('learning/toefl/structure.html', questions=STRUCTURE)


@blueprint.route('/learning/toefl/structure-result', methods=['POST'])
def submit2():
    user_answers = request.form
    score = 0
    results = []

    for question in STRUCTURE:
        qid = str(question['id'])
        correct = question['answer']
        user_answer = int(user_answers.get(qid, -1))

        results.append({
            'question': question['question'],
            'choices': question['choices'],
            'correct_answer': question['choices'][correct],
            'your_answer': question['choices'][user_answer] if user_answer != -1 else "No answer",
            'is_correct': user_answer == correct
        })

        if user_answer == correct:
            score += 1

    return render_template('/learning/toefl/structure-result.html', score=score, total=len(STRUCTURE), results=results)


@blueprint.route('/toefl-structure')
def quiz():
    return render_template('home/toefl-structure.html', questions=STRUCTURE)


@blueprint.route('/hasil-toefl-structure', methods=['POST'])
def submit():
    user_answers = request.form
    score = 0
    results = []

    for question in STRUCTURE:
        qid = str(question['id'])
        correct = question['answer']
        user_answer = int(user_answers.get(qid, -1))

        results.append({
            'question': question['question'],
            'choices': question['choices'],
            'correct_answer': question['choices'][correct],
            'your_answer': question['choices'][user_answer] if user_answer != -1 else "No answer",
            'is_correct': user_answer == correct
        })

        if user_answer == correct:
            score += 1

    return render_template('home/hasil-toefl-structure.html', score=score, total=len(STRUCTURE), results=results)


with open('apps/templates/toefl/reading.json') as f:
    passages = json.load(f)


@blueprint.route('/toefl-reading')
def toeflreading():
    session.clear()
    return redirect(url_for('home_blueprint.toefl_reading', passage_id=0))


@blueprint.route('/toefl-reading/<int:passage_id>', methods=['GET', 'POST'])
def toefl_reading(passage_id):
    if passage_id < 0 or passage_id >= len(passages):
        return render_template('home/home_blueprint.toefl_reading.html', passage_id=0)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)

        # Navigate forward
        if 'next' in request.form and passage_id < 4:
            return redirect(url_for('home_blueprint.toefl_reading', passage_id=passage_id + 1))
        elif 'prev' in request.form and passage_id > 0:
            return redirect(url_for('home_blueprint.toefl_reading', passage_id=passage_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('home_blueprint.hasiltoeflreading'))

    passage = passages[passage_id]
    saved_answers = [session.get(f'p{passage_id}_q{i}') for i in range(10)]

    return render_template(
        'home/toefl-reading.html',
        passage_id=passage_id,
        total=len(passages),
        passage=passage,
        saved_answers=saved_answers
    )


@blueprint.route('/hasil-toefl-reading')
def hasiltoeflreading():
    score = 0
    hasiltoeflreading = []

    for p_id, passage in enumerate(passages):
        for q_id, question in enumerate(passage["questions"]):
            user_answer = session.get(f'p{p_id}_q{q_id}')
            correct_answer = question["answer"]
            hasiltoeflreading.append({
                "passage": p_id + 1,
                "number": q_id + 1,
                "question": question["text"],
                "your_answer": user_answer or "No answer",
                "correct_answer": correct_answer,
                "is_correct": user_answer == correct_answer
            })

            if user_answer == correct_answer:
                score += 1

    return render_template('home/hasil-toefl-reading.html', score=score, total=50, incorrect=hasiltoeflreading)


@blueprint.route('/toefl-class')
def toefl():
    return render_template('home/toefl.html')

# Affiliate Marketing


@blueprint.route('/toeflmurah')
def toeflmurah():
    return render_template('home/toefl.html', ref="RC001")

# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
