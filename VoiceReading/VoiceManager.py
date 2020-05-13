import os
import shutil


class VoiceManager(object):
    def __init__(self, voice_root_dir, voice_out_dir):
        self.voice_root_dir = voice_root_dir
        self.voice_out_dir = voice_out_dir
        self._create_root_dir()

    def _create_root_dir(self):
        assert len(self.voice_root_dir)
        assert len(self.voice_out_dir)
        os.makedirs(self.voice_root_dir, exist_ok=True)
        os.makedirs(self.voice_out_dir, exist_ok=True)

    def get_voice_names(self):
        return os.listdir(self.voice_root_dir)

    def existing_voice_name(self, voice_name):
        voice_names = self.get_voice_names()
        return voice_name in voice_names

    def create_voice(self, voice_name, audio_files):
        if self.existing_voice_name(voice_name):
            return False
        os.mkdir(os.path.join(self.voice_root_dir, voice_name))
        for idx, audio_file in enumerate(audio_files):
            shutil.copy(audio_file, os.path.join(self.voice_root_dir, voice_name, "{}.wav".format(idx)))
        return True

    def remove_voice(self, voice_name):
        voice_path = os.path.join(self.voice_root_dir, voice_name)
        if os.path.exists(voice_path):
            shutil.rmtree(voice_path)


if __name__ == "__main__":
    voice_root="data/voice_root"
    voice_out = "data/voice_out"
    vm = VoiceManager(voice_root, voice_out)
    audio_dir = "data/LibriSpeech/train-clean-100/19/227"
    audio_list = ["19-227-0000.flac", "19-227-0003.flac", "19-227-0005.flac"]
    audio_list = [os.path.join(audio_dir, audio_file) for audio_file in audio_list]
    # vm.create_voice("test1", audio_list)
    voice_names = vm.get_voice_names()
    print(voice_names)
    for voice_name in voice_names:
        vm.remove_voice(voice_name)
