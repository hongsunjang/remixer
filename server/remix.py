# -*- coding: utf-8 -*-
"""py_최종_영주.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HVJrIUVfCpaASEP6F5j8kFxIHBGpspSV
"""
#필요한 패키지 모두 다운: 미리 해놓기
#pip install pydub
#apt install ffmpeg
#pip install spleeter
#git clone https://github.com/cwoodall/pitch-shifter-py.git
#pip install pydub


#모두 import
import os
import IPython.display as ipd
from IPython.display import Audio
import soundfile as sf
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.effects import normalize

#################################################################
####REMIXER: 인풋 곡(30초)의 보컬'파일'의 경로, 인풋 곡의 보컬이 포함된 '폴더'의 경로(피치쉬프터 써야함, 중간과정에 생기는 파일도 여기에 저장해야 함, 
####         추천된 inst(마디반복과 볼륨조절이 완료된) '파일'의 경로, 인풋곡과 추천된곡의 key와 bpm


####인풋 곡 보컬 파일명: input.wav 받아온다고 가정
##################################################################


#4. 보컬 튜닝 - 보컬 자르기

#해야 할 것: 스플릿된 inst와 vocal의 경로를 일정한 규칙에 따라 이름붙여야 함...!!!!!! input.wav로 받아온다고 가정
def get_trimmed_vocal(tempo_vocal, tepmo_inst, path):
  bpm = tempo_vocal
  bar_1_seconds = 1/bpm * 4 * 60
  beat_1_seconds = 1/bpm * 60
  sound = AudioSegment.from_file(path+'/input.wav', format="wav") 
  new_sound = sound[beat_1_seconds*2*1000:]

  new_sound.export(path+'/잘린보컬.wav', format="wav")


#5. 보컬 튜닝 - 보컬 템포 변환: 아까 분리된 30초짜리 보컬 파일을 불러옴


def get_stretched_vocal(tempo_vocal, tempo_inst, path, inst_path): #추천될 곡을 이름을 이용해서 검색해서 가져와야 함. inst_path 예시: /saaaa/사랑의배터리-accompaniment.wav
  y, sr = librosa.load(path+'/잘린보컬.wav')
  vocal_stretch = librosa.effects.time_stretch(y, tempo_inst/tempo_vocal)

  global y_inst
  global sr_inst
  y_inst, sr_inst = librosa.load(inst_path)

#6. 보컬 튜닝 - 길이 맞추기

  global ny2
  if len(vocal_stretch)>len(y_inst):
    vocal_stretch = vocal_stretch[:len(y_inst)]
    ny2 = y_inst
  else:
    ny2 = y_inst[:len(vocal_stretch)]

  sf.write(path+'/tempo조절.wav',vocal_stretch , sr_inst, format='WAV', endian='LITTLE', subtype='PCM_16') # 깨지지 않음


#7. 보컬 튜닝 - 키 조절

def key_changer(key_vocal, key_inst, path):
  change = key_inst - key_vocal
  source = path + '/tempo조절.wav'
  output = path + '/tempo_key_조절.wav'

  ####만약에 key 차이가 너무 많이 난다면???
  # 예를 들면 inst가 11, vocal이 2 : change=9이니까 차라리 3키를 낮추는게 나음! -3
  if change > 6:
    change = change - 12

  # 예를 들면 inst가 2, vocal이 11: change=-9이니까 3키를 높이는게 나음
  elif change < -6:
    change = change + 12

  !pitchshifter -s '{source}' -o '{output}' -p '{change}' -b 1


#8. 합치기 - 일단 합치기

def merge_and_normalize(path):
  
  #방금 저장한 파일을 불러옴
  y3, sr3 = librosa.load(path+'/tempo_key_조절.wav')
  sf.write(path+'/before_normalized.wav',y3+ny2 , sr_inst, format='WAV', endian='LITTLE', subtype='PCM_16') # 깨지지 않음


  #9. 합치기 - normalize
  # Import target audio file
  before_normalize = AudioSegment.from_file(path+"/before_normalized.wav")

  # Normalize target audio file
  normalized = normalize(before_normalize)

  normalized.export(path+'/result.wav', format='wav')







################################################################
def REMIXXX(input_path, inst_path,tempo_vocal, tempo_inst, key_vocal, key_inst):

  get_trimmed_vocal(tempo_vocal=tempo_vocal, tepmo_inst=tempo_inst, path=input_path)

  get_stretched_vocal(tempo_vocal=tempo_vocal, tempo_inst=tempo_inst, path=input_path, inst_path=inst_path)

  key_changer(key_vocal=key_vocal, key_inst=key_inst, path=input_path)

  merge_and_normalize(path=input_path)
  #############################################################
  #input_path는 폴더
  #inst_path는 파일(추천된 곡)



  #추가해야 하는 것: 프리뷰 15초 길이로 자르기, 추천시스템이용\
  #만약에 mp3만 가능하다면 wav를 mp3로 바꿔주기
  #만약에 사용자가 넣은 곡이 데이터셋에 있는 곡이라면??

import numpy as np
import pandas as pd

df = pd.read_csv('/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/songnames_bpm_key.csv')

def get_key_bpm(songname):
  key_inst = df[df['songname'] == songname]['key']
  tempo_inst = df[df['songname'] == songname]['bpm']
  return tempo_inst, key_inst



input_path = '/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2'
inst_path = '/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial/추천된inst샘플.wav'
tempo_inst = 120
tempo_vocal = 125
key_vocal = 8
key_inst = 7

REMIXXX(input_path=input_path, inst_path=inst_path,tempo_vocal=tempo_vocal, tempo_inst=tempo_inst, key_vocal=key_vocal, key_inst=key_inst)

/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2/output/Ariana Grande - One last time (한국어 가사해석자막)30-chorus.wav/vocals.wav'
/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2/output/Ariana Grande - One last time (한국어 가사해석자막)30-chorus/vocals.wav

a = 'Ariana Grande - One last time (한국어 가사해석자막)30-chorus.wav' #이게 songname_30이니까
a = a[:-4]
print(a)



""" [Errno 2] No such file or directory: '/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2/output/Ariana Grande - One last time (한국어 가사해석자막)30-chorus.wav/vocals.wav'"""

!pitchshifter -h

!pitchshifter -s '/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2/Ariana Grande - One last time (한국어 가사해석자막)30-chorus.wav' -o '/content/drive/Shareddrives/YBIGTA_컨퍼런스_음악리믹서/trial2/키변환.wav' -p -1 -b 1

#15초 자르는 코드

from pydub import AudioSegment
path = '자를 곡의 파일 경로'
sound = AudioSegment.from_file(path)
trimmed_sound = sound[:15*1000]
into_file = trimmed_sound.export('저장할 경로.저장할이름.wav', format='wav')