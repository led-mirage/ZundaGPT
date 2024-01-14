# ZundaGPT
#
# VOICEキャラクターモジュール
#
# Copyright (c) 2023-2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import subprocess
import time

import clr
import psutil

from settings import Settings
from sound import play_sound
from voicevox_api import VoicevoxAPI
from coeiroink_api import CoeiroinkApi

# キャラクターファクトリ
class CharacterFactory:
    # アシスタントキャラクターを作成する
    @staticmethod
    def create_assistant_character(settings: Settings):
        tts_software = settings.get_assistant_tts_software()
        if tts_software == "VOICEVOX":
            return CharacterVoicevox(
                settings.get_voicevox_path(),
                settings.get_assistant_speaker_id(),
                settings.get_assistant_speed_scale(),
                settings.get_assistant_pitch_scale())
        elif tts_software == "AIVOICE":
            return CharacterAIVoice(
                settings.get_aivoice_path(),
                settings.get_assistant_speaker_id())
        elif tts_software == "COEIROINK":
            return CharacterCoeiroink(
                settings.get_coeiroink_path(),
                settings.get_assistant_speaker_id(),
                settings.get_assistant_speed_scale(),
                settings.get_assistant_pitch_scale())
        else:
            return None

    # ユーザーキャラクターを作成する
    @staticmethod
    def create_user_character(settings: Settings):
        tts_software = settings.get_user_tts_software()
        if tts_software == "VOICEVOX":
            return CharacterVoicevox(
                settings.get_voicevox_path(),
                settings.get_user_speaker_id(),
                settings.get_user_speed_scale(),
                settings.get_user_pitch_scale())
        elif tts_software == "AIVOICE":
            return CharacterAIVoice(
                settings.get_aivoice_path(),
                settings.get_user_speaker_id())
        elif tts_software == "COEIROINK":
            return CharacterCoeiroink(
                settings.get_coeiroink_path(),
                settings.get_user_speaker_id(),
                settings.get_user_speed_scale(),
                settings.get_user_pitch_scale())
        else:
            return None

# VOICEVOXキャラクター
class CharacterVoicevox:
    DEFAULT_INSTALL_PATH = "%LOCALAPPDATA%/Programs/VOICEVOX/VOICEVOX.exe"

    def __init__(self, voicevox_path, speaker_id, speed_scale, pitch_scale):
        self.voicevox_path = voicevox_path
        self.speaker_id = speaker_id
        self.speed_scale = speed_scale
        self.pitch_scale = pitch_scale
        CharacterVoicevox.run_voicevox(self.voicevox_path)

    # 話す
    def talk(self, text):
        CharacterVoicevox.run_voicevox(self.voicevox_path)
        query_json = VoicevoxAPI.audio_query(text, self.speaker_id)
        query_json["speedScale"] = self.speed_scale
        query_json["pitchScale"] = self.pitch_scale
        wave_data = VoicevoxAPI.synthesis(query_json, self.speaker_id)
        play_sound(wave_data)

    # VOICEVOXが起動しているかどうかを調べる
    @staticmethod
    def is_voicevox_running():
        for process in psutil.process_iter(['name']):
            try:
                if process.info['name'].lower() == "voicevox.exe":
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    # VOICEVOXが起動していなかったら起動する
    @staticmethod
    def run_voicevox(voicevox_path):
        appdata_local = os.getenv("LOCALAPPDATA")
        voicevox_path = voicevox_path.replace("%LOCALAPPDATA%", appdata_local)
        if os.path.isfile(voicevox_path):
            if not CharacterVoicevox.is_voicevox_running():
                subprocess.Popen(voicevox_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# A.I.VOICEキャラクター
class CharacterAIVoice:
    DEFAULT_INSTALL_PATH = "%ProgramW6432%/AI/AIVoice/AIVoiceEditor/AI.Talk.Editor.Api.dll"

    _tts_control = None

    def __init__(self, aivoice_path, speaker_id):
        self.speaker_id = speaker_id
        self.aivoice_path = aivoice_path
        CharacterAIVoice.run_aivoice(self.aivoice_path)

    # 話す
    def talk(self, text):
        CharacterAIVoice.run_aivoice(self.aivoice_path)
        try:
            tts_control = CharacterAIVoice._tts_control
            tts_control.Connect()
            tts_control.CurrentVoicePresetName = self.speaker_id
            tts_control.Text = text
            play_time = tts_control.GetPlayTime()
            tts_control.Play()
            time.sleep((play_time + 500) / 1000)
        except Exception as err:
            CharacterAIVoice._tts_control = None
            print(err)
            raise

    # A.I.VOICEが起動していなかったら起動して接続する
    @classmethod
    def run_aivoice(cls, aivoice_path):
        program_dir = os.getenv("ProgramW6432")
        aivoice_path = aivoice_path.replace("%ProgramW6432%", program_dir)
        if os.path.isfile(aivoice_path):
            if CharacterAIVoice._tts_control is None:
                clr.AddReference(aivoice_path)
                from AI.Talk.Editor.Api import TtsControl, HostStatus

                tts_control = TtsControl()
                host_name = tts_control.GetAvailableHostNames()[0]
                tts_control.Initialize(host_name)        
                if tts_control.Status == HostStatus.NotRunning:
                    tts_control.StartHost()
                tts_control.Connect()
                cls._tts_control = tts_control

# COEIROINKキャラクター
class CharacterCoeiroink:
    def __init__(self, coeiroink_path, speaker_id, speed_scale, pitch_scale):
        self.coeiroink_path = coeiroink_path
        self.speed_scale = speed_scale
        self.pitch_scale = pitch_scale
        self.speaker_id = speaker_id
        CharacterCoeiroink.run_coeiroink(self.coeiroink_path)

    # 話す
    def talk(self, text):
        if CharacterCoeiroink.run_coeiroink(self.coeiroink_path):
            wave_data = CoeiroinkApi.get_wave_data(
                self.speaker_id, text, speedScale=self.speed_scale, pitchScale=self.pitch_scale, volumeScale=0.8)
            play_sound(wave_data)

    # COEIROINKが起動しているかどうかを調べる
    @staticmethod
    def is_coeiroink_running():
        return CoeiroinkApi.get_status() is not None

    # COEIROINKが起動していなかったら起動する
    @staticmethod
    def run_coeiroink(coeiroink_path):
        if CharacterCoeiroink.is_coeiroink_running():
            return True
        else:
            if os.path.isfile(coeiroink_path):
                subprocess.Popen(coeiroink_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                loop_count = 0
                while CharacterCoeiroink.is_coeiroink_running() == False:
                    time.sleep(1)
                    loop_count += 1
                    if loop_count >= 10:
                        return False
                return True
            else:
                return False
