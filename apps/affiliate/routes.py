from apps.affiliate import blueprint
from flask import render_template


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
