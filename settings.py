# ZundaGPT
#
# アプリケーション設定クラス
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import os
import threading

from voicevox_api import VoicevoxAPI

class Settings:
    FILE_VER = 4

    def __init__(self, setting_file_path):
        self._setting_file_path = setting_file_path
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self._assistant_echo = True
        self._assistant_tts_software = "VOICEVOX"
        self._assistant_speaker_id = "3"    # ずんだもん
        self._assistant_speed_scale = 1.2
        self._assistant_pitch_scale = 0.0
        self._user_echo = True
        self._user_tts_software = "VOICEVOX"
        self._user_speaker_id = "13"    # 青山龍星
        self._user_speed_scale = 1.2
        self._user_pitch_scale = 0.0
        self._chat_api = "OpenAI"
        self._chat_model = "gpt-3.5-turbo-1106"
        self._chat_character_name = "ずんだ"
        self._chat_instruction = "君は優秀なアシスタント。ずんだもんの話し方で話す。具体的には語尾に「のだ」または「なのだ」をつけて自然に話す。回答は１００文字以内で簡潔に行う。"
        self._chat_bad_response = "答えられないのだ"
        self._chat_history_size = 6
        self._chat_log_folder = "log"
        self._voicevox_server = VoicevoxAPI.DEFAULT_SERVER
        from character import CharacterVoicevox
        self._voicevox_path = CharacterVoicevox.DEFAULT_INSTALL_PATH
        from character import CharacterAIVoice
        self._aivoice_path = CharacterAIVoice.DEFAULT_INSTALL_PATH

    # 発話するか（アシスタント）
    def get_assistant_echo_enable(self):
        with self._lock:
            return self._assistant_echo

    def set_assistant_echo_enable(self, enable):
        with self._lock:
            self._assistant_echo = enable

    # 使用する読み上げソフト（アシスタント）
    def get_assistant_tts_software(self):
        with self._lock:
            return self._assistant_tts_software

    def set_assistant_tts_software(self, software):
        with self._lock:
            self._assistant_tts_software = software

    # 話者ID（アシスタント）
    def get_assistant_speaker_id(self):
        with self._lock:
            return self._assistant_speaker_id

    def set_assistant_speaker_id(self, speaker_id):
        with self._lock:
            self._assistant_speaker_id = speaker_id

    # 読み上げスピード（アシスタント）
    def get_assistant_speed_scale(self):
        with self._lock:
            return self._assistant_speed_scale

    def set_assistant_speed_scale(self, speed_scale):
        with self._lock:
            self._assistant_speed_scale = speed_scale

    # 声の高さ（アシスタント）
    def get_assistant_pitch_scale(self):
        with self._lock:
            return self._assistant_pitch_scale

    def set_assistant_pitch_scale(self, pitch_scale):
        with self._lock:
            self._assistant_pitch_scale = pitch_scale

    # 発話するか（ユーザー）
    def get_user_echo_enable(self):
        with self._lock:
            return self._user_echo

    def set_user_echo_enable(self, enable):
        with self._lock:
            self._user_echo = enable

    # 使用する読み上げソフト（ユーザー）
    def get_user_tts_software(self):
        with self._lock:
            return self._user_tts_software

    def set_user_tts_software(self, software):
        with self._lock:
            self._user_tts_software = software

    # 話者ID（ユーザー）
    def get_user_speaker_id(self):
        with self._lock:
            return self._user_speaker_id

    def set_user_speaker_id(self, speaker_id):
        with self._lock:
            self._user_speaker_id = speaker_id

    # 読み上げスピード（ユーザー）
    def get_user_speed_scale(self):
        with self._lock:
            return self._user_speed_scale

    def set_user_speed_scale(self, speed_scale):
        with self._lock:
            self._user_speed_scale = speed_scale

    # 声の高さ（ユーザー）
    def get_user_pitch_scale(self):
        with self._lock:
            return self._user_pitch_scale

    def set_user_pitch_scale(self, pitch_scale):
        with self._lock:
            self._user_pitch_scale = pitch_scale

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

    # チャットのログを保存するフォルダ
    def get_chat_log_folder(self):
        with self._lock:
            return self._chat_log_folder
        
    def set_chat_log_folder(self, chat_log_folder):
        with self._lock:
            self._chat_log_folder = chat_log_folder

    # VOICEVOX サーバーのURL
    def get_voicevox_server(self):
        with self._lock:
            return self._voicevox_server
    
    def set_voicevox_server(self, voicevox_server):
        with self._lock:
            self._voicevox_server = voicevox_server

    # VOICEVOXインストールパス
    def get_voicevox_path(self):
        with self._lock:
            return self._voicevox_path
        
    def set_voicevox_path(self, path):
        with self._lock:
            self._voicevox_path = path

    # A.I.VOICEインストールパス
    def get_aivoice_path(self):
        with self._lock:
            return self._aivoice_path
        
    def set_aivoice_path(self, path):
        with self._lock:
            self._aivoice_path = path

    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._setting_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["file_ver"] = Settings.FILE_VER
            setting["assistant_echo"] = self._assistant_echo
            setting["assistant_tts_software"] = self._assistant_tts_software
            setting["assistant_speaker_id"] = self._assistant_speaker_id
            setting["assistant_speed_scale"] = self._assistant_speed_scale
            setting["assistant_pitch_scale"] = self._assistant_pitch_scale
            setting["user_echo"] = self._user_echo
            setting["user_tts_software"] = self._user_tts_software
            setting["user_speaker_id"] = self._user_speaker_id
            setting["user_speed_scale"] = self._user_speed_scale
            setting["user_pitch_scale"] = self._user_pitch_scale
            setting["chat_api"] = self._chat_api
            setting["chat_model"] = self._chat_model
            setting["chat_character_name"] = self._chat_character_name
            setting["chat_instruction"] = self._chat_instruction
            setting["chat_bad_response"] = self._chat_bad_response
            setting["chat_history_size"] = self._chat_history_size
            setting["chat_log_folder"] = self._chat_log_folder
            setting["voicevox_server"] = self._voicevox_server
            setting["voicevox_path"] = self._voicevox_path
            setting["aivoice_path"] = self._aivoice_path
            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        if not os.path.exists(self._setting_file_path):
            self._init_member()
            self._save_nolock()
            return

        with self._lock:
            with open(self._setting_file_path, "r", encoding="utf-8") as file:
                setting = json.load(file)
                file_ver = setting.get("file_ver", 1)
                self._assistant_echo = setting.get("assistant_echo", self._assistant_echo)
                self._assistant_tts_software = setting.get("assistant_tts_software", self._assistant_tts_software)
                self._assistant_speaker_id = setting.get("assistant_speaker_id", self._assistant_speaker_id)
                self._assistant_speed_scale = setting.get("assistant_speed_scale", self._assistant_speed_scale)
                self._assistant_pitch_scale = setting.get("assistant_pitch_scale", self._assistant_pitch_scale)
                self._user_echo = setting.get("user_echo", self._user_echo)
                self._user_tts_software = setting.get("user_tts_software", self._user_tts_software)
                self._user_speaker_id = setting.get("user_speaker_id", self._user_speaker_id)
                self._user_speed_scale = setting.get("user_speed_scale", self._user_speed_scale)
                self._user_pitch_scale = setting.get("user_pitch_scale", self._user_pitch_scale)
                self._chat_api = setting.get("chat_api", self._chat_api)
                self._chat_model = setting.get("chat_model", self._chat_model)
                self._chat_character_name = setting.get("chat_character_name", self._chat_character_name)
                self._chat_instruction = setting.get("chat_instruction", self._chat_instruction)
                self._chat_bad_response = setting.get("chat_bad_response", self._chat_bad_response)
                self._chat_history_size = setting.get("chat_history_size", self._chat_history_size)
                self._chat_log_folder = setting.get("chat_log_folder", self._chat_log_folder)
                self._voicevox_server = setting.get("voicevox_server", self._voicevox_server)
                self._voicevox_path = setting.get("voicevox_path", self._voicevox_path)
                self._aivoice_path = setting.get("aivoice_path", self._aivoice_path)

        if file_ver < Settings.FILE_VER:
            self._save_nolock()

        return setting
