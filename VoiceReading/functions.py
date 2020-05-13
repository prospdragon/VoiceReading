import os
from flask import current_app as app
from VoiceReading.make_voice_cloning import ClonedVoice, enc_model_fpath, syn_model_dir, voc_model_fpath, \
                                            low_mem, no_sound


cloned_voice = ClonedVoice(enc_model_fpath, syn_model_dir, voc_model_fpath, low_mem, no_sound)


def get_voices():
    return os.listdir(app.config["SPEECH_FOLDER"])


def add_voice(audio, voice_name, idx):
    voice_path = os.path.join(app.config["SPEECH_FOLDER"], voice_name)
    if not os.path.exists(voice_path):
        os.mkdir(voice_path)
    audio.save(os.path.join(voice_path, "{}.wav".format(idx)))


def text_to_sv_speech(tts_data):
    # get `out_file` from in_fpath and text
    # out_file = os.path.join(app.config['SPEECH_FOLDER_URL'], "speech1.wav")
    tts_dir = app.config['TTS_FOLDER']
    out_file = 'speech1.wav'
    out_file = 'tts_res.wav'
    file_list = []
    for idx, sent_info in enumerate(tts_data):
        voice_name = sent_info['voice']
        text = sent_info["sentence"]
        if len(text) < 2:
            continue
        in_audio_path = os.path.join(app.config["SPEECH_FOLDER"], voice_name, "3.wav")
        out_path = os.path.join(tts_dir, "temp{}.wav".format(idx))
        if os.path.exists(out_path):
            os.remove(out_path)
        cloned_voice.text_to_sv_speech(in_audio_path, text, out_path)
        file_list.append(out_path)

    if file_list:
        cmd = "sox {} {}".format(" ".join(file_list), os.path.join(tts_dir, out_file))
        os.system(cmd)

    return out_file


def text_to_sv_speech_multi_speaker(tts_data):
    # get `out_file` from in_fpath and text
    # out_file = os.path.join(app.config['SPEECH_FOLDER_URL'], "speech1.wav")
    tts_dir = app.config['TTS_FOLDER']
    out_file = 'speech1.wav'
    out_file = 'tts_res.wav'
    file_list = []
    for idx, sent_info in enumerate(tts_data):
        voice_name = sent_info['voice']
        text = sent_info["sentence"]
        if len(text) < 2:
            continue
        voice_files = []
        for voice_idx in range(1, 4):
            in_audio_path = os.path.join(app.config["SPEECH_FOLDER"], voice_name, "{}.wav".format(voice_idx))
            if os.path.exists(in_audio_path):
                voice_files.append(in_audio_path)

        out_path = os.path.join(tts_dir, "temp{}.wav".format(idx))
        if os.path.exists(out_path):
            os.remove(out_path)
        cloned_voice.text_to_sv_speech_multi_speaker(voice_files, text, out_path)
        file_list.append(out_path)

    if os.path.exists(out_file):
        os.remove(out_file)

    if file_list:
        cmd = "sox {} {}".format(" ".join(file_list), os.path.join(tts_dir, out_file))
        os.system(cmd)

    return out_file


def play_voice(voice_name):
    out_file = os.path.join(voice_name, "1.wav")
    # out_file = 'speech1.wav'

    return out_file
