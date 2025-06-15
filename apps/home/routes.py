from apps.home import blueprint
from flask import render_template, request, flash, redirect, session, url_for, send_from_directory
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.home.models import Snisub, Janji, Profile, Level
from apps.authentication.models import Users
from apps import db
import json
from datetime import datetime, timedelta


@blueprint.route('/index')
def index():
    return render_template('home/homepage.html', segment='index')


@blueprint.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')


@blueprint.route('/choosetutor', methods=['GET', 'POST'])
def choosetutor():
    if "class" in request.args and "ref" in request.args:
        class_name = request.args.get("class")
        ref_name = request.args.get("ref")
    elif "class" in request.args:
        class_name = request.args.get("class")
        ref_name = "RC"
    else:
        class_name = "Raih Cita"
        ref_name = "RC"
    return render_template('home/choose-tutor.html', tutor=class_name, ref=ref_name)


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


@blueprint.route('/learning/ielts/<template>')
def learningielts_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("learning/ielts/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/learning/toefl/<template>')
def learningtoefl_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("learning/toefl/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/learning/ielts')
def learningcenterielts():
    return render_template('learning/ielts/dashboard.html', segment='toefl')


@blueprint.route('/learning/toefl')
def learningcentertoefl():
    return render_template('learning/toefl/dashboard.html', segment='toefl')


@blueprint.route('/learning')
def learning():
    return render_template('learning/dashboard.html', segment='toefl')


# IELTS Listening Quiz
with open('apps/templates/question/ielts/listening.json') as f:
    LISTENINGIELTS = json.load(f)


@blueprint.route('/learning/ielts/listening')
def ieltslistening():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('home_blueprint.ielts_listening', section_id=1))


@blueprint.route('/learning/ielts/listening/<int:section_id>', methods=['GET', 'POST'])
def ielts_listening(section_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('home_blueprint.ieltslistening'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{section_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('home_blueprint.hasiltoeflreading2'))

    if section_id < 1 or section_id > 4:
        return render_template('home/home_blueprint.ielts_listening.html', section_id=1)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{section_id}_q{i}'
            answers = request.form.getlist(f'q{i}[]')
            if not answers:
                answers = request.form.get(f'q{i}', None)
            session[q_key] = answers

        # Navigate forward
        if 'next' in request.form and section_id < 4:
            return redirect(url_for('home_blueprint.ielts_listening', section_id=section_id + 1))
        elif 'prev' in request.form and section_id > 0:
            return redirect(url_for('home_blueprint.ielts_listening', section_id=section_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('home_blueprint.hasilieltslistening'))

    section_data = LISTENINGIELTS['sections'][section_id - 1]
    saved_answers = [session.get(f'p{section_id}_q{i}') for i in range(10)]

    return render_template(
        'learning/ielts/listening.html',
        section_id=section_id,
        section=section_data,
        saved_answers=saved_answers,
        segment='listening', remaining_seconds=remaining_seconds
    )


def get_band_score(correct_answers):
    bands = [
        (39, 40, 9),
        (37, 38, 8.5),
        (35, 36, 8),
        (32, 34, 7.5),
        (30, 31, 7),
        (26, 29, 6.5),
        (23, 25, 6),
        (18, 22, 5.5),
        (16, 17, 5),
        (13, 15, 4.5),
        (11, 12, 4),
        (9, 10, 3.5),
        (7, 8, 3),
        (5, 6, 2.5),
        (3, 4, 2),
        (1, 2, 1.5),
        (0, 0, 1),
    ]

    for low, high, band in bands:
        if low <= correct_answers <= high:
            return band


@blueprint.route('/learning/ielts/listening-result')
def hasilieltslistening():
    correctans = 0
    hasilieltslistening = []

    for p_id, section in enumerate(LISTENINGIELTS['sections']):
        for q_id, question in enumerate(section["questions"]):
            user_answer = session.get(f'p{p_id + 1}_q{q_id}')

            correct_answer_raw = question["answer"]

            if question.get("type") == "checkbox_two":
                # Ensure user_answer is a list
                if not isinstance(user_answer, list):
                    user_answer = [user_answer] if user_answer else []
                correct_answers = [ans.strip().lower()
                                   for ans in correct_answer_raw]

                # Count number of correct selections (can be 0, 1, 2)
                num_correct = sum(
                    1 for ans in user_answer if ans.strip().lower() in correct_answers)

                # Add points accordingly
                correctans += num_correct

                is_correct = False if num_correct == 0 else True

                hasilieltslistening.append({
                    "section": p_id + 1,
                    "number": q_id + 1,
                    "question": question.get("question", "No question text provided"),
                    "your_answer": ", ".join(user_answer) if user_answer else "No answer",
                    "correct_answer": ", ".join(correct_answers),
                    "is_correct": is_correct
                })
            else:
                # Handle normal single-answer questions
                user_answer_norm = user_answer.strip().lower() if user_answer else None
                if isinstance(correct_answer_raw, list):
                    correct_answers = [ans.strip().lower()
                                       for ans in correct_answer_raw]
                else:
                    correct_answers = [correct_answer_raw.strip().lower()]

                is_correct = user_answer_norm in correct_answers if user_answer_norm else False

                hasilieltslistening.append({
                    "section": p_id + 1,
                    "number": q_id + 1,
                    "question": question.get("question", "No question text provided"),
                    "your_answer": user_answer or "No answer",
                    "correct_answer": ", ".join(correct_answers),
                    "is_correct": is_correct
                })

                if is_correct:
                    correctans += 1

    score = get_band_score(correctans)

    return render_template('learning/ielts/listening-result.html', score=score, correctans=correctans, total=40, incorrect=hasilieltslistening, segment='listening')


# TOEFL Listening Comprehension Quiz
with open('apps/templates/question/toefl/listening.json') as f:
    LISTENING = json.load(f)


@blueprint.route('/learning/toefl/startlistening')
def starttoefllistening():
    # Set start time and end time in session
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")

    return redirect(url_for('home_blueprint.toefllistening2'))


@blueprint.route('/learning/toefl/listening')
def toefllistening2():
    # Retrieve end time and calculate remaining seconds
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('home_blueprint.starttoefllistening'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        session.clear()  # Clear session to reset the test
        flash("Time's up! Please start the test again.")
        return redirect(url_for('home_blueprint.hasiltoefllistening2'))

    return render_template('learning/toefl/listening.html', questions=LISTENING, remaining_seconds=remaining_seconds, segment='listening')


score_map = {
    0: 31, 1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31,
    9: 32, 10: 32.5, 11: 33, 12: 36, 13: 37.5, 14: 39, 15: 40,
    16: 41, 17: 42, 18: 43, 19: 43.5, 20: 44, 21: 45, 22: 45.5,
    23: 46, 24: 46, 25: 46.5, 26: 47, 27: 48, 28: 48.5, 29: 49,
    30: 49, 31: 49.5, 32: 50, 33: 51, 34: 51.5, 35: 52, 36: 52,
    37: 53, 38: 54, 39: 54, 40: 55, 41: 56, 42: 56, 43: 57,
    44: 58, 45: 59, 46: 60.5, 47: 62, 48: 64, 49: 66, 50: 68
}


@blueprint.route('/learning/toefl/listening-result', methods=['GET', 'POST'])
def hasiltoefllistening2():
    user_answers = request.form
    correctans = 0
    results = []

    for question in LISTENING:
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
            correctans += 1

    score = score_map.get(correctans, "Invalid input")
    score = score*10

    level = Level(correct=correctans, score=score)
    db.session.add(level)
    db.session.commit()

    return render_template('learning/toefl/listening-result.html', correctans=correctans, score=score, total=len(LISTENING), results=results, segment='listening')


@blueprint.route('/cekdb', methods=['GET', 'POST'])
def cekdb():
    list = Level.query.all()
    return render_template('home/cekdb.html', list=list)

# TOEFL Structure and Written Expression Quiz


with open('apps/templates/question/toefl/structure.json') as f:
    STRUCTURE = json.load(f)


@blueprint.route('/learning/toefl/startstructure')
def starttoeflstructure():
    # Set start time and end time in session
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S")

    return redirect(url_for('home_blueprint.toeflstructure2'))


@blueprint.route('/learning/toefl/structure')
def toeflstructure2():
 # Retrieve end time and calculate remaining seconds
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('home_blueprint.starttoeflstructure'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        session.clear()  # Clear session to reset the test
        flash("Time's up! Please start the test again.")
        return redirect(url_for('home_blueprint.hasiltoeflstructure2'))

    return render_template('learning/toefl/structure.html', questions=STRUCTURE, remaining_seconds=remaining_seconds, segment='structure')


score_map = {
    0: 31, 1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31,
    9: 32, 10: 34, 11: 36, 12: 38, 13: 39, 14: 40, 15: 42,
    16: 43, 17: 44, 18: 45, 19: 46, 20: 47, 21: 48, 22: 48.5,
    23: 49, 24: 50, 25: 51, 26: 52, 27: 53, 28: 54, 29: 55,
    30: 56, 31: 57, 32: 58, 33: 59, 34: 60, 35: 61, 36: 63,
    37: 65.5, 38: 68, 39: 68, 40: 68
}


@blueprint.route('/learning/toefl/structure-result', methods=['GET', 'POST'])
def hasiltoeflstructure2():
    user_answers = request.form
    correctans = 0
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
            correctans += 1

    score = score_map.get(correctans, "Invalid input")
    score = score * 10

    return render_template('/learning/toefl/structure-result.html', correctans=correctans, score=score, total=len(STRUCTURE), results=results)


# TOEFL Reading Comprehension Quiz

# Score mapping: correct answers → reading score
score_map = {
    0: 31, 1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31,
    9: 31, 10: 31, 11: 31, 12: 31, 13: 33, 14: 35, 15: 37,
    16: 38, 17: 40, 18: 41, 19: 42, 20: 43, 21: 44, 22: 45,
    23: 46, 24: 47, 25: 48, 26: 48, 27: 49, 28: 50, 29: 50,
    30: 51, 31: 52, 32: 52, 33: 53, 34: 54, 35: 54, 36: 55,
    37: 56, 38: 56, 39: 57, 40: 58, 41: 58, 42: 59, 43: 60,
    44: 61, 45: 62, 46: 63, 47: 64, 48: 65, 49: 66, 50: 67
}


with open('apps/templates/question/toefl/reading.json') as f:
    passages = json.load(f)


@blueprint.route('/learning/toefl/reading')
def toeflreading2():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('home_blueprint.toefl_reading2', passage_id=0))


@blueprint.route('/learning/toefl/reading/<int:passage_id>', methods=['GET', 'POST'])
def toefl_reading2(passage_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('home_blueprint.toeflreading2'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('home_blueprint.hasiltoeflreading2'))

    if passage_id < 0 or passage_id >= len(passages):
        return render_template('home/home_blueprint.toefl_reading2.html', passage_id=0)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)

        # Navigate forward
        if 'next' in request.form and passage_id < 4:
            return redirect(url_for('home_blueprint.toefl_reading2', passage_id=passage_id + 1))
        elif 'prev' in request.form and passage_id > 0:
            return redirect(url_for('home_blueprint.toefl_reading2', passage_id=passage_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('home_blueprint.hasiltoeflreading2'))

    passage = passages[passage_id]
    saved_answers = [session.get(f'p{passage_id}_q{i}') for i in range(10)]

    return render_template(
        'learning/toefl/reading.html',
        passage_id=passage_id,
        total=len(passages),
        passage=passage,
        saved_answers=saved_answers, segment='reading', remaining_seconds=remaining_seconds
    )


@blueprint.route('/learning/toefl/reading-result')
def hasiltoeflreading2():
    correctans = 0
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
                correctans += 1

        score = score_map.get(correctans, "Invalid input")
        score = score * 10

    return render_template('learning/toefl/reading-result.html', score=score, correctans=correctans, total=50, incorrect=hasiltoeflreading, segment='reading')

# READING Mobile Version


@blueprint.route('/learning/toefl/readingmobile')
def toeflreadingmobile():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('home_blueprint.toefl_readingmobile', passage_id=0))


@blueprint.route('/learning/toefl/readingmobile/<int:passage_id>', methods=['GET', 'POST'])
def toefl_readingmobile(passage_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('home_blueprint.toeflreadingmobile'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('home_blueprint.hasiltoeflreading2'))

    if passage_id < 0 or passage_id >= len(passages):
        return render_template('home/home_blueprint.toefl_readingmobile.html', passage_id=0)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)

        # Navigate forward
        if 'next' in request.form and passage_id < 4:
            return redirect(url_for('home_blueprint.toefl_readingmobile', passage_id=passage_id + 1))
        elif 'prev' in request.form and passage_id > 0:
            return redirect(url_for('home_blueprint.toefl_readingmobile', passage_id=passage_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('home_blueprint.hasiltoeflreading2'))

    passage = passages[passage_id]
    saved_answers = [session.get(f'p{passage_id}_q{i}') for i in range(10)]

    return render_template(
        'learning/toefl/readingmobile.html',
        passage_id=passage_id,
        total=len(passages),
        passage=passage,
        saved_answers=saved_answers, segment='reading', remaining_seconds=remaining_seconds
    )


# OLD

@blueprint.route('/toefl-listening')
def toefllistening():
    return render_template('home/toefl-listening.html', questions=LISTENING)


@blueprint.route('/hasil-toefl-listening', methods=['GET', 'POST'])
def hasiltoefllistening():
    user_answers = request.form
    score = 0
    results = []

    for question in LISTENING:
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

    return render_template('home/hasil-toefl-listening.html', score=score, total=len(LISTENING), results=results)


@blueprint.route('/toefl-structure')
def quiz():
    return render_template('home/toefl-structure.html', questions=STRUCTURE)


@blueprint.route('/hasil-toefl-structure', methods=['GET', 'POST'])
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


# BEST URL FROM AFFILIATE MARKETING


@blueprint.route('/toefl-class')
def toefl():
    return render_template('home/toefl.html')


@blueprint.route('/toeflclass')
def toeflclass():
    return render_template('home/toefl.html')


@blueprint.route('/ieltsacademicprivate')
def ieltsacademicprivate():
    return render_template('home/ieltsacprivate.html', ref="RC")


@blueprint.route('/raihbeasiswa')
def raihbeasiswa():
    return render_template('home/mentoringprivate.html', ref="RC")


# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


# Affiliate Marketing

@blueprint.route('/toeflmurah')
def toeflmurah():
    return render_template('home/toefl.html', ref="RC001")


@blueprint.route('/toeflprivateclassmurce')
def toeflprivateclassmurce():
    return render_template('home/toeflprivate.html', ref="RC002")


@blueprint.route('/toeflprepclassdaa')
def toeflprepclassdaa():
    return render_template('home/toefl.html', ref="RC003")


@blueprint.route('/toeflprepclass')
def toeflprepclass():
    return render_template('home/toefl.html', ref="RC004")


@blueprint.route('/toeflprivatemurah')
def toeflprivatemurah():
    return render_template('home/toeflprivate.html', ref="RC005")


@blueprint.route('/ieltsforwhv')
def ieltsforwhv():
    return render_template('home/ieltswhvprivate.html', ref="RC006")


@blueprint.route('/getscholarship')
def getscholarship():
    return render_template('home/mentoringprivate.html', ref="RC007")


@blueprint.route('/raihbeasiswow')
def raihbeasiswow():
    return render_template('home/mentoringprivate.html', ref="RC008")


@blueprint.route('/ieltsacademicpriv')
def ieltsacademicpriv():
    return render_template('home/ieltsacprivate.html', ref="RC009")


@blueprint.route('/toeflprivclass')
def toeflprivclass():
    return render_template('home/toeflprivate.html', ref="RC010")


@blueprint.route('/grammarprivv')
def grammarprivv():
    return render_template('home/grammarprivate.html', ref="RC011")


@blueprint.route('/speakingprivclasss')
def speakingprivclasss():
    return render_template('home/speakingprivate.html', ref="RC012")


@blueprint.route('/ieltswhvprivv')
def ieltswhvprivv():
    return render_template('home/ieltswhvprivate.html', ref="RC013")


@blueprint.route('/kelasprivatielts')
def kelasprivatielts():
    return render_template('home/ieltsacprivate.html', ref="RC014")


@blueprint.route('/grammarprivclass')
def grammarprivclass():
    return render_template('home/grammarprivate.html', ref="RC015")


@blueprint.route('/speakingprivclass')
def speakingprivclass():
    return render_template('home/speakingprivate.html', ref="RC016")


@blueprint.route('/toeflsmumerr')
def toeflsmumerr():
    return render_template('home/toefl.html', ref='RC017')


@blueprint.route('/toeflprepclasz')
def toeflprepclasz():
    return render_template('home/toefl.html', ref='RC018')


@blueprint.route('/privattoeflmurah')
def privattoeflmurah():
    return render_template('home/toeflprivate.html', ref='RC019')


@blueprint.route('/ieltacademicprivateclass')
def ieltacademicprivateclass():
    return render_template('home/ieltsacprivate.html', ref='RC020')


@blueprint.route('/academickelastoefl')
def academickelastoefl():
    return render_template('home/ieltsacprivate.html', ref='RC021')


@blueprint.route('/ieltsacademicprivateclassdaa')
def ieltsacademicprivateclassdaa():
    return render_template('home/ieltsacprivate.html', ref='RC022')


@blueprint.route('/clsprivatemurah')
def clsprivatemurah():
    return render_template('home/toeflprivate.html', ref='RC023')


@blueprint.route('/toeflprepclassmurah')
def toeflprepclassmurah():
    return render_template('home/toefl.html', ref='RC024')


@blueprint.route('/theeliteglobaltoefl')
def theeliteglobaltoefl():
    return render_template('home/toeflprivate.html', ref='RC025')


@blueprint.route('/speakingwithtari')
def speakingwithtari():
    return render_template('home/speakingprivate.html', ref='RC026')


@blueprint.route('/siaptoefl')
def siaptoefl():
    return render_template('home/toeflprivate.html', ref='RC027')


@blueprint.route('/teoflprepwithtari')
def teoflprepwithtari():
    return render_template('home/toefl.html', ref='RC028')


@blueprint.route('/toeflprepwithtari')
def toeflprepwithtari():
    return render_template('home/toefl.html', ref='RC029')


@blueprint.route('/kelastoeflpromo')
def kelastoeflpromo():
    return render_template('home/toefl.html', ref='RC030')


@blueprint.route('/prepclasstoefl')
def prepclasstoefl():
    return render_template('home/toefl.html', ref='RC031')


@blueprint.route('/ieltsprivatclass1')
def ieltsprivatclass1():
    return render_template('home/ieltswhvprivate.html', ref='RC032')


@blueprint.route('/speakingprivateclassNina')
def speakingprivateclassNina():
    return render_template('home/speakingprivate.html', ref='RC033')


@blueprint.route('/toeflprepterjangkau')
def toeflprepterjangkau():
    return render_template('home/toefl.html', ref='RC034')


@blueprint.route('/grammarprvtcls')
def grammarprvtcls():
    return render_template('home/grammarprivate.html', ref='RC035')


@blueprint.route('/grammarprivateclassdaa')
def grammarprivateclassdaa():
    return render_template('home/grammarprivate.html', ref='RC036')


@blueprint.route('/speakingprivateclassdaa')
def speakingprivateclassdaa():
    return render_template('home/speakingprivate.html', ref='RC037')


@blueprint.route('/profesional')
def profesional():
    return render_template('home/speakingprivate.html', ref='')


@blueprint.route('/toeflprepmurah')
def toeflprepmurah():
    return render_template('home/toefl.html', ref='RC038')


@blueprint.route('/toeflkursusprivatemurah')
def toeflkursusprivatemurah():
    return render_template('home/toeflprivate.html', ref='RC039')


@blueprint.route('/ieltsakademikprivate')
def ieltsakademikprivate():
    return render_template('home/ieltsacprivate.html', ref='RC040')


@blueprint.route('/toeflpreperationkursus')
def toeflpreperationkursus():
    return render_template('home/toefl.html', ref='RC041')


@blueprint.route('/academicprivateclass')
def academicprivateclass():
    return render_template('home/ieltsacprivate.html', ref='RC042')


@blueprint.route('/easylearntoefl')
def easylearntoefl():
    return render_template('home/toefl.html', ref='RC043')
