"""Main routes."""
import os
from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, jsonify
from flask import current_app as app
from .assets import compile_assets
from werkzeug.utils import secure_filename
import time
import json
from .functions import get_voices, text_to_sv_speech, add_voice, play_voice, text_to_sv_speech_multi_speaker

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
compile_assets(app)


@main_bp.route('/', methods=['GET'])
def index():
    voices = get_voices()
    return render_template('index.jinja2',
                           refresh=str(int(round(time.time() * 1000))),
                           voices=voices)


@main_bp.route('/create', methods=['GET'])
def create():
    voices = get_voices()
    return render_template('create.jinja2',
                           refresh=str(int(round(time.time() * 1000))),
                           voices=voices)


@main_bp.route('/create_voice', methods=['POST'])
def create_voice():
    voice_name = request.form['voice_name']
    rand_pref = str(int(round(time.time() * 1000)))
    audio1 = request.files['audio1']
    if audio1:
        add_voice(audio1, voice_name, 1)
        #filename = rand_pref + '_file_1_' + voice_name + '.wav'
        #audio1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    audio2 = request.files['audio2']
    if audio2:
        add_voice(audio2, voice_name, 2)
        #filename = rand_pref + '_file_2_' + voice_name + '.wav'
        #audio2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    audio3 = request.files['audio3']
    if audio3:
        add_voice(audio3, voice_name, 3)
        # filename = rand_pref + '_file_3_' + voice_name + '.wav'
        # audio3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('main_bp.create'))


@main_bp.route('/upload_record', methods=['POST'])
def upload_record():
    file_audio = request.files['audio_data']

    # Upload
    filename = str(int(round(time.time() * 1000))) + '_record_' + request.form['index'] + '_' + secure_filename(file_audio.filename) + '.wav'
    file_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    res = {
        "success": True,
        "message": "Success."
    }
    return jsonify(res)


@main_bp.route('/speech_all', methods=['POST'])
def speech_all():
    print(request.form['sentence_data'])
    form_data = json.loads(request.form['sentence_data'])
    #out_fpath = text_to_sv_speech(form_data)
    out_fpath = text_to_sv_speech_multi_speaker(form_data)
    print("audio path: {}".format(out_fpath))

    return send_from_directory(app.config['TTS_FOLDER_URL']
                               , out_fpath
                               , attachment_filename=out_fpath
                               , as_attachment=True)


@main_bp.route('/speech_sentence', methods=['POST'])
def speech_sentence():
    print(request.form['sentence_data'])
    form_data = json.loads(request.form['sentence_data'])
    voice_name = form_data[0]["voice"]
    out_fpath = play_voice(voice_name)

    return app.config['SPEECH_FOLDER_URL'] + '/' + out_fpath
