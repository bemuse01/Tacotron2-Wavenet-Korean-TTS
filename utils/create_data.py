import os, glob, shutil
import pandas as pd
import json


root = '/content/'
git_clone = root + 'Tacotron2-Wavenet-Korean-TTS/'
kss_dir = root + 'kss'

text_dir = glob.glob(os.path.join(kss_dir, '*.txt'))[0]
dir_list = [name for name in os.listdir(kss_dir) if os.path.isdir(os.path.join(kss_dir, name))]

script = pd.read_csv(text_dir, dtype='object', sep='|', header=None)
names = script[0]
sounds = script[3]
script_slice_offset = 0

for dir in dir_list:
    audio_files_count = len(os.listdir(kss_dir + '/' + dir))

    start_idx = script_slice_offset
    end_idx = script_slice_offset + audio_files_count
    script_slice_offset += audio_files_count

    temp = {}
    voice_dir = git_clone + 'datasets/' + dir
    voice_audio_dir = voice_dir + '/audio'
    os.makedirs(voice_dir, exist_ok=True)
    os.makedirs(voice_audio_dir, exist_ok=True)

    for i in range(len(script)):
      name = names[i]
      sound = sounds[i]
      voice, file_name = name.split('/')

      if voice == dir:
        temp[git_clone + voice_dir + '/audio/' + file_name] = sound
        shutil.copy2(kss_dir + '/' + name, voice_audio_dir)

    with open(voice_dir + '/' + dir + '-recognition-All.json', 'w', encoding='UTF-8-sig') as file:
      file.write(json.dumps(temp, ensure_ascii=False))
