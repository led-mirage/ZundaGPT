# ZundaGPT
#
# アプリケーション設定クラス
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import threading

from voicevox_api import VoicevoxAPI

class Settings:
    def __init__(self, setting_file_path):
        self._setting_file_path = setting_file_path
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self._speaker_id = 3
        self._speed_scale = 1.2
        self._pitch_scale = 0.0
        self._voicevox_server = VoicevoxAPI.DEFAULT_SERVER
        self._chat_api = "OpenAI"
        self._chat_model = "gpt-3.5-turbo-1106"
        self._chat_character_name = "ずんだ"
        self._chat_instruction = "君は優秀なアシスタント。ずんだもんの話し方で話す。具体的には語尾に「のだ」または「なのだ｜をつけ自然に話す。回答は１００文字以内で簡潔に行う。"
        self._chat_bad_response = "答えられないのだ"
        self._chat_history_size = 6

    # 話者ID
    def get_speaker_id(self):
        with self._lock:
            return self._speaker_id

    def set_speaker_id(self, speaker_id):
        with self._lock:
            self._speaker_id = speaker_id

    # 読み上げスピード
    def get_speed_scale(self):
        with self._lock:
            return self._speed_scale

    def set_speed_scale(self, speed_scale):
        with self._lock:
            self._speed_scale = speed_scale

    # 声の高さ
    def get_pitch_scale(self):
        with self._lock:
            return self._pitch_scale

    def set_pitch_scale(self, pitch_scale):
        with self._lock:
            self._pitch_scale = pitch_scale

    # VOICEVOX サーバーのURL
    def get_voicevox_server(self):
        with self._lock:
            return self._voicevox_server
    
    def set_voicevox_server(self, voicevox_server):
        with self._lock:
            self._voicevox_server = voicevox_server

    # チャットエージェントのモデル
    def get_chat_api(self):
        with self._lock:
            return self._chat_api

    def set_chat_api(self, chat_api):
        with self._lock:
            self._chat_api = chat_api

    # チャットエージェントのモデル
    def get_chat_model(self):
        with self._lock:
            return self._chat_model
    
    def set_chat_model(self, chat_model):
        with self._lock:
            self._chat_model = chat_model

    # チャットエージェントのキャラ名（表示用）
    def get_chat_character_name(self):
        with self._lock:
            return self._chat_character_name

    def set_chat_character_name(self, chat_character_name):
        with self._lock:
            self._chat_character_name = chat_character_name

    # チャットエージェントへの指示
    def get_chat_instruction(self):
        with self._lock:
            return self._chat_instruction
        
    def set_chat_instruction(self, chat_instruction):
        with self._lock:
            self._chat_instruction = chat_instruction

    # チャットエージェントが答えられないときの台詞
    def get_chat_bad_response(self):
        with self._lock:
            return self._chat_bad_response
        
    def set_chat_bad_response(self, chat_bad_response):
        with self._lock:
            self._chat_bad_response = chat_bad_response

    # チャットエージェントに送信する過去会話数
    def get_chat_history_size(self):
        with self._lock:
            return min(self._chat_history_size, 50) # 事故防止用 最大50まで

    def set_chat_history_size(self, chat_history_size):
        with self._lock:
            self._chat_history_size = chat_history_size

    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._setting_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["speaker_id"] = self._speaker_id
            setting["speed_scale"] = self._speed_scale
            setting["pitch_scale"] = self._pitch_scale
            setting["voicevox_server"] = self._voicevox_server
            setting["chat_api"] = self._chat_api
            setting["chat_model"] = self._chat_model
            setting["chat_character_name"] = self._chat_character_name
            setting["chat_instruction"] = self._chat_instruction
            setting["chat_bad_response"] = self._chat_bad_response
            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        with self._lock:
            try:
                with open(self._setting_file_path, "r", encoding="utf-8") as file:
                    setting = json.load(file)
                    self._speaker_id = setting["speaker_id"]
                    self._speed_scale = setting["speed_scale"]
                    self._pitch_scale = setting["pitch_scale"]
                    self._voicevox_server = setting["voicevox_server"]
                    self._chat_api = setting["chat_api"]
                    self._chat_model = setting["chat_model"]
                    self._chat_character_name = setting["chat_character_name"]
                    self._chat_instruction = setting["chat_instruction"]
                    self._chat_bad_response = setting["chat_bad_response"]
                return setting
            except Exception as err:
                self._init_member()
                self._save_nolock()
