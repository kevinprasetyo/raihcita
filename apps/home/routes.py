from apps.home import blueprint
from flask import render_template, request, flash, redirect, session, url_for, send_from_directory
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.home.models import Snisub, Janji, Profile, Level
from apps.authentication.models import Users
from apps import db
import json


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


@blueprint.route('/get-quick-result', methods=['GET', 'POST'])
def get_quick_result():
    correct_answers = [
        "wants", "are", "has", "bought", "She visited her grandmother in Yogyakarta",
        "do not", "on", "rains", "She sings beautifully.", "He enjoys reading, jogging, and cooking."
    ]

    # Get user's answers
    data = request.form.get('answers')
    user_answers = json.loads(data)

    # Calculate score
    score = sum(1 for user, correct in zip(
        user_answers, correct_answers) if user == correct)

    session['score'] = score  # Store score in session for later use

    return redirect(url_for('home_blueprint.quick_result'))


@blueprint.route('/quick-result')
def quick_result():
    # Retrieve score from session
    score = session.get('score')

    if score is None:
        return redirect('/quick')

    # Placement table with full descriptors
    placement_levels = [
        {
            "min": 0, "max": 2, "level": "Seeker",
            "desc_en": "<b>You are a Seeker!</b><br>Every expert was once a beginner, and guess what? You’re just getting started — and that’s exciting!<br><br><b>What You Can Do Next:</b><br>- Learn grammar basics with simple, clear examples.<br>- Practice daily with short, guided exercises.<br>- Join Raihcita Basic English. Contact admin for more info.<br>",
            "desc_id": "<b>Kamu adalah seorang Seeker!</b><br>Setiap ahli dulunya juga seorang pemula, dan tebak apa? Kamu baru saja memulai — dan itu luar biasa!<br><br><b>Yang Bisa Kamu Lakukan Selanjutnya:</b><br>- Pelajari dasar-dasar grammar dengan contoh yang simpel dan jelas.<br>- Latihan setiap hari dengan soal-soal singkat dan terarah.<br>- Gabung di Raihcita Basic English! Hubungi admin untuk info selengkapnya.<br>"
        },
        {
            "min": 3, "max": 5, "level": "Starter",
            "desc_en": "<b>You Are a Starter!</b><br>Welcome to the journey! You’ve learned the basics, and now it’s time to strengthen your core grammar skills.<br><br><b>What You Can Do Next:</b><br>- Watch videos or use visuals to understand grammar better.<br>- Repeat key structures until they feel natural.<br>- Join Raihcita Basic English. Contact admin for more info.<br>",
            "desc_id": "<b>Kamu adalah seorang Starter!</b><br>Selamat datang di perjalanan ini! Kamu sudah memahami dasar-dasarnya, dan sekarang saatnya memperkuat kemampuan Bahasa Inggris-mu.<br><br><b>Yang Bisa Kamu Lakukan Selanjutnya:</b><br>- Berlatih dengan contoh-contoh soal dan mencari pembahasannya.<br>- Pahami pola dan struktur kalimat.<br>- Mulailah mencoba membuat kalimat sederhana.<br>- Gabung di Raihcita Basic English! Hubungi admin untuk info selengkapnya.<br>"
        },
        {
            "min": 6, "max": 7, "level": "Explorer",
            "desc_en": "<b>You Are an Explorer!</b><br>You’re making great progress! You understand the key grammar patterns and are ready to take things to the next level.<br><br><b>What’s Next for You:</b><br>- Join our TOEFL Preparation Class (Beginner Track)!<br>- Strengthen your grammar through guided lessons and practice.<br>- Get personalized feedback to help you improve faster.<br>",
            "desc_id": "<b>Kamu adalah seorang Explorer!</b><br>Progress-mu sudah keren! Kamu sudah memahami pola grammar dasar dan siap naik ke level berikutnya dengan lebih banyak latihan dan bimbingan terstruktur.<br><br><b>Langkah Selanjutnya untuk Kamu:</b><br>- Sekarang kamu bisa bergabung di TOEFL Preparation Class (Beginner Track) di Raihcita!<br>- Perkuat grammar-mu melalui pelajaran yang terarah dan latihan rutin.<br>- Dapatkan feedback personal untuk membantumu berkembang lebih cepat.<br>- Kamu siap naik level — dan Raihcita akan selalu mendampingi!<br>"
        },
        {
            "min": 8, "max": 9, "level": "Visionary",
            "desc_en": "<b>You Are a Visionary!</b><br>Great job! You’ve built a strong foundation and are just a few steps away from advanced fluency.<br><br><b>What’s Next for You:</b><br>- You're eligible for our TOEFL or IELTS Preparation Class!<br>- Polish your grammar accuracy and expand your vocabulary.<br>- Join interactive sessions to boost your confidence.<br>",
            "desc_id": "<b>Kamu adalah seorang Visionary!</b><br>Keren banget! Kamu sudah punya dasar yang kuat dan sekarang tinggal selangkah lagi menuju kefasihan tingkat lanjut.<br><br><b>Langkah Seru Selanjutnya:</b><br>- Kamu sudah bisa ikut TOEFL atau IELTS Preparation Class dari kami!<br>- Asah ketepatan grammar dan tambah perbendaharaan kata.<br>- Ikut sesi interaktif yang bikin kamu makin percaya diri dan lancar ngomong.<br>- Perjalananmu sudah oke — dan kami siap bantu kamu sampai tujuan!<br>"
        },
        {
            "min": 10, "max": 10, "level": "Achiever",
            "desc_en": "<b>You Are an Achiever!</b><br>Wow — you nailed it! You’ve shown excellent control of English grammar.<br><br><b>What’s Next for You:</b><br>- Join our TOEFL or IELTS Preparation Class.<br>- Practice advanced grammar and real-world communication.<br>- Get personalized feedback to refine your speaking and writing.<br>",
            "desc_id": "<b>Kamu adalah seorang Achiever!</b><br>Wow — keren banget, kamu berhasil sampai di tahap ini! Penguasaan grammarmu udah keren, dan sekarang kamu siap banget buat ngulik topik-topik yang lebih kompleks dengan percaya diri.<br><br><b>Langkah Seru Berikutnya:</b><br>- Gabung di TOEFL atau IELTS Preparation Class buat ningkatin skill ke level selanjutnya.<br>- Latihan grammar yang lebih kompleks dan belajar menyusun kalimat yang bisa diaplikasikan di kehidupan sehari-hari maupun akademik.<br>- Dapatkan bimbingan terstruktur dan feedback personal supaya kemampuan grammar dan pemahaman bacaanmu makin tepat.<br>- Kamu udah di level atas — dan kami siap bantu kamu bersinar lebih terang lagi! ✨<br>"
        }
    ]

    # Find matching placement level
    result = next(
        (item for item in placement_levels if item['min'] <= score <= item['max']), None)

    return render_template("home/quick-result.html", score=score, result=result)


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


@blueprint.route('/learning')
def learning():
    return render_template('learning/dashboard.html', segment='toefl')


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
