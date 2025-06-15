from apps.learningielts import blueprint
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from jinja2 import TemplateNotFound
import json
from datetime import datetime, timedelta


@blueprint.route('/')
def learningcenterielts():
    return render_template('learning/ielts/dashboard.html', segment='toefl')


# IELTS Listening Quiz
with open('apps/templates/question/ielts/listening.json') as f:
    LISTENINGIELTS = json.load(f)


@blueprint.route('/listening')
def ieltslistening():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningielts_blueprint.ielts_listening', section_id=1))


@blueprint.route('/listening/<int:section_id>', methods=['GET', 'POST'])
def ielts_listening(section_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningielts_blueprint.ieltslistening'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(10):
            q_key = f'p{section_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningielts_blueprint.hasiltoeflreading2'))

    if section_id < 1 or section_id > 4:
        return render_template('home/learningielts_blueprint.ielts_listening.html', section_id=1)

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
            return redirect(url_for('learningielts_blueprint.ielts_listening', section_id=section_id + 1))
        elif 'prev' in request.form and section_id > 0:
            return redirect(url_for('learningielts_blueprint.ielts_listening', section_id=section_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningielts_blueprint.hasilieltslistening'))

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


@blueprint.route('/listening-result')
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


# IELTS Reading Quiz
with open('apps/templates/question/ielts/reading.json') as f:
    READINGIELTS = json.load(f)


@blueprint.route('/reading')
def ieltsreading():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningielts_blueprint.ielts_reading', section_id=1))


@blueprint.route('/reading/<int:section_id>', methods=['GET', 'POST'])
def ielts_reading(section_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningielts_blueprint.ieltsreading'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningielts_blueprint.hasilieltsreading'))

    if section_id < 1 or section_id > 3:
        return render_template('home/learningielts_blueprint.ielts_reading.html', section_id=1)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            answers = request.form.getlist(f'q{i}[]')
            if not answers:
                answers = request.form.get(f'q{i}', None)
            session[q_key] = answers

        # Navigate forward
        if 'next' in request.form and section_id < 3:
            return redirect(url_for('learningielts_blueprint.ielts_reading', section_id=section_id + 1))
        elif 'prev' in request.form and section_id > 0:
            return redirect(url_for('learningielts_blueprint.ielts_reading', section_id=section_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningielts_blueprint.hasilieltsreading'))

    section_data = READINGIELTS['sections'][section_id - 1]
    saved_answers = [session.get(f'p{section_id}_q{i}') for i in range(13)]

    return render_template(
        'learning/ielts/reading.html',
        section_id=section_id,
        section=section_data,
        saved_answers=saved_answers,
        segment='reading', remaining_seconds=remaining_seconds
    )


def reading_bandscore(correct_answers):
    bands = [
        (39, 40, 9),
        (37, 38, 8.5),
        (35, 36, 8),
        (33, 34, 7.5),
        (30, 32, 7),
        (27, 29, 6.5),
        (23, 26, 6),
        (19, 22, 5.5),
        (15, 18, 5),
        (13, 14, 4.5),
        (10, 12, 4),
        (8, 9, 3.5),
        (6, 7, 3),
        (4, 5, 2.5),
        (2, 3, 2),
        (1, 1, 1.5),
        (0, 0, 1),
    ]

    for lower, upper, band in bands:
        if lower <= correct_answers <= upper:
            return band
    return 0  # fallback if input is out of expected range


@blueprint.route('/reading-result')
def hasilieltsreading():
    correctans = 0
    hasilieltsreading = []

    for p_id, section in enumerate(READINGIELTS['sections']):
        for q_id, question in enumerate(section["questions"]):
            user_answer = session.get(f'p{p_id + 1}_q{q_id}')
            user_answer = user_answer.strip().lower() if user_answer else None  # Normalize input
            correct_answer_raw = question["answer"]

            # Normalize correct answer(s)
            if isinstance(correct_answer_raw, list):
                correct_answers = [ans.strip().lower()
                                   for ans in correct_answer_raw]
            else:
                correct_answers = [correct_answer_raw.strip().lower()]

            is_correct = user_answer in correct_answers if user_answer else False

            hasilieltsreading.append({
                "section": p_id + 1,
                "number": q_id + 1,
                "question": question.get("question", "No question text provided"),
                "your_answer": user_answer or "No answer",
                "correct_answer": ", ".join(correct_answers),
                "is_correct": is_correct
            })

            if is_correct:
                correctans += 1

    score = reading_bandscore(correctans)

    return render_template('learning/ielts/reading-result.html', score=score, correctans=correctans, total=40, incorrect=hasilieltsreading, segment='reading')

# IELTS Reading Mobile Version


@blueprint.route('/readingmobile')
def ieltsreadingmobile():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningielts_blueprint.ielts_readingmobile', section_id=1))


@blueprint.route('/readingmobile/<int:section_id>', methods=['GET', 'POST'])
def ielts_readingmobile(section_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningielts_blueprint.ieltsreadingmobile'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningielts_blueprint.hasilieltsreadingmobile'))

    if section_id < 1 or section_id > 3:
        return render_template('home/learningielts_blueprint.ielts_readingmobile.html', section_id=1)

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            answers = request.form.getlist(f'q{i}[]')
            if not answers:
                answers = request.form.get(f'q{i}', None)
            session[q_key] = answers

        # Navigate forward
        if 'next' in request.form and section_id < 3:
            return redirect(url_for('learningielts_blueprint.ielts_readingmobile', section_id=section_id + 1))
        elif 'prev' in request.form and section_id > 0:
            return redirect(url_for('learningielts_blueprint.ielts_readingmobile', section_id=section_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningielts_blueprint.hasilieltsreading'))

    section_data = READINGIELTS['sections'][section_id - 1]
    saved_answers = [session.get(f'p{section_id}_q{i}') for i in range(13)]

    return render_template(
        'learning/ielts/readingmobile.html',
        section_id=section_id,
        section=section_data,
        saved_answers=saved_answers,
        segment='reading', remaining_seconds=remaining_seconds
    )


# IELTS WRITING Quiz
with open('apps/templates/question/ielts/writing.json') as f:
    WRITINGIELTS = json.load(f)


@blueprint.route('/writing')
def ieltswriting():
    session.clear()
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session['end_time'] = (
        datetime.now() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('learningielts_blueprint.ielts_writing', section_id=1))


@blueprint.route('/writing/<int:section_id>', methods=['GET', 'POST'])
def ielts_writing(section_id):
    if 'end_time' not in session or 'start_time' not in session:
        flash("Please start the test first.")
        return redirect(url_for('learningielts_blueprint.ieltswriting'))

    end_time = datetime.strptime(session['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining_seconds = int((end_time - now).total_seconds())

    if remaining_seconds <= 0:
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            session[q_key] = request.form.get(f'q{i}', None)
        flash("Time's up! Please start the test again.")
        return redirect(url_for('learningielts_blueprint.hasiltoeflwriting'))

    if request.method == 'POST':
        # Save user's answers to session
        for i in range(13):
            q_key = f'p{section_id}_q{i}'
            answers = request.form.getlist(f'q{i}[]')
            if not answers:
                answers = request.form.get(f'q{i}', None)
            session[q_key] = answers

        # ✅ SAVE the writing input
        writing_input = request.form.get("writing", None)
        if writing_input:
            session[f'p{section_id}_writing'] = writing_input

        # Navigate forward
        if 'next' in request.form and section_id < 2:
            return redirect(url_for('learningielts_blueprint.ielts_writing', section_id=section_id + 1))
        elif 'prev' in request.form and section_id > 0:
            return redirect(url_for('learningielts_blueprint.ielts_writing', section_id=section_id - 1))
        elif 'submit_all' in request.form:
            return redirect(url_for('learningielts_blueprint.hasilieltswriting'))

    section_data = WRITINGIELTS['sections'][section_id - 1]
    saved_answers = [session.get(f'p{section_id}_q{i}') for i in range(13)]

    return render_template(
        'learning/ielts/writing.html',
        section_id=section_id,
        section=section_data,
        saved_answers=saved_answers,
        segment='writing', remaining_seconds=remaining_seconds
    )


def get_gpt_feedback(prompt_text, user_writing, task_number, task_type):
    """Send prompt + user writing to GPT for feedback"""
    system_prompt = f"""
You are an IELTS Writing Examiner. Evaluate the following Task {task_number} ({task_type}) response.
Score it on the IELTS band scale (0–9), and give detailed feedback.

Return your response in this format:

Band Score: [score]
Strengths: [list of strengths]
Weaknesses: [list of weaknesses]
Model Answer: [a full model answer for this prompt]
Improvement Tips: [tips for improvement]
Resources: [suggest 2–3 useful websites/books for IELTS writing]

User Prompt: {prompt_text}
User Writing: {user_writing}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error getting feedback: {str(e)}"


@blueprint.route('/writing-result', methods=['GET', 'POST'])
def hasilieltswriting():
    for section in WRITINGIELTS['sections']:
        section_id = section['id']
        user_writing = request.form.get("writing", "")
        if user_writing:
            session[f'p{section_id}_writing'] = user_writing
        task_type = "Academic"
        task_number = 1
        prompt_text = section['text']

    result = "The result is coming soon."

    return render_template('learning/ielts/writing-result.html', segment='writing',
                           writing=user_writing,
                           task_type=task_type,
                           task_number=task_number,
                           prompt_text=prompt_text,
                           result=result)


@blueprint.route('/<template>')
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
