from apps.learningtoefl import blueprint
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from jinja2 import TemplateNotFound
import json
from datetime import datetime, timedelta


@blueprint.route('/')
def learningcentertoefl():
    return render_template('learning/toefl/dashboard.html', segment='toefl')


# TOEFL Listening Comprehension Quiz
with open('apps/templates/question/toefl/listening.json') as f:
    LISTENING = json.load(f)


@blueprint.route('/startlistening')
def starttoefllistening():
    # Set start time and end time in session
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")

    return redirect(url_for('learningtoefl_blueprint.toefllistening2'))


@blueprint.route('/listening')
def toefllistening2():
    # Retrieve end time and calculate remaining seconds
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningtoefl_blueprint.starttoefllistening'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        session.clear()  # Clear session to reset the test
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningtoefl_blueprint.hasiltoefllistening2'))

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


@blueprint.route('/listening-result', methods=['GET', 'POST'])
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

    return render_template('learning/toefl/listening-result.html', correctans=correctans, score=score, total=len(LISTENING), results=results, segment='listening')


# TOEFL Structure and Written Expression Quiz

with open('apps/templates/question/toefl/structure.json') as f:
    STRUCTURE = json.load(f)


@blueprint.route('/startstructure')
def starttoeflstructure():
    # Set start time and end time in session
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S")

    return redirect(url_for('learningtoefl_blueprint.toeflstructure2'))


@blueprint.route('/structure')
def toeflstructure2():
 # Retrieve end time and calculate remaining seconds
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningtoefl_blueprint.starttoeflstructure'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        session.clear()  # Clear session to reset the test
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningtoefl_blueprint.hasiltoeflstructure2'))

    return render_template('learning/toefl/structure.html', questions=STRUCTURE, remaining_seconds=remaining_seconds, segment='structure')


score_map = {
    0: 31, 1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31,
    9: 32, 10: 34, 11: 36, 12: 38, 13: 39, 14: 40, 15: 42,
    16: 43, 17: 44, 18: 45, 19: 46, 20: 47, 21: 48, 22: 48.5,
    23: 49, 24: 50, 25: 51, 26: 52, 27: 53, 28: 54, 29: 55,
    30: 56, 31: 57, 32: 58, 33: 59, 34: 60, 35: 61, 36: 63,
    37: 65.5, 38: 68, 39: 68, 40: 68
}


@blueprint.route('/structure-result', methods=['GET', 'POST'])
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


@blueprint.route('/reading')
def toeflreading2():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningtoefl_blueprint.toefl_reading2', passage_id=0))


@blueprint.route('/reading/<int:passage_id>', methods=['GET', 'POST'])
def toefl_reading2(passage_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningtoefl_blueprint.toeflreading2'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningtoefl_blueprint.hasiltoeflreading2'))

    if passage_id < 0 or passage_id >= len(passages):
        return render_template('learningtoefl_blueprint.toefl_reading2', passage_id=0)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)

        # Navigate forward
        if 'next' in request.form and passage_id < 4:
            return redirect(url_for('learningtoefl_blueprint.toefl_reading2', passage_id=passage_id + 1))
        elif 'prev' in request.form and passage_id > 0:
            return redirect(url_for('learningtoefl_blueprint.toefl_reading2', passage_id=passage_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningtoefl_blueprint.hasiltoeflreading2'))

    passage = passages[passage_id]
    saved_answers = [session.get(f'p{passage_id}_q{i}') for i in range(10)]

    return render_template(
        'learning/toefl/reading.html',
        passage_id=passage_id,
        total=len(passages),
        passage=passage,
        saved_answers=saved_answers, segment='reading', remaining_seconds=remaining_seconds
    )


@blueprint.route('/reading-result')
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

# TOEFL READING Mobile Version


@blueprint.route('/readingmobile')
def toeflreadingmobile():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningtoefl_blueprint.toefl_readingmobile', passage_id=0))


@blueprint.route('/readingmobile/<int:passage_id>', methods=['GET', 'POST'])
def toefl_readingmobile(passage_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningtoefl_blueprint.toeflreadingmobile'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningtoefl_blueprint.hasiltoeflreading2'))

    if passage_id < 0 or passage_id >= len(passages):
        return render_template('home/learningtoefl_blueprint.toefl_readingmobile.html', passage_id=0)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(10):
            q_key = f'p{passage_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)

        # Navigate forward
        if 'next' in request.form and passage_id < 4:
            return redirect(url_for('learningtoefl_blueprint.toefl_readingmobile', passage_id=passage_id + 1))
        elif 'prev' in request.form and passage_id > 0:
            return redirect(url_for('learningtoefl_blueprint.toefl_readingmobile', passage_id=passage_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningtoefl_blueprint.hasiltoeflreading2'))

    passage = passages[passage_id]
    saved_answers = [session.get(f'p{passage_id}_q{i}') for i in range(10)]

    return render_template(
        'learning/toefl/readingmobile.html',
        passage_id=passage_id,
        total=len(passages),
        passage=passage,
        saved_answers=saved_answers, segment='reading', remaining_seconds=remaining_seconds
    )


@blueprint.route('/<template>')
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
