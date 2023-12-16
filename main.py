# ZundaGPT
#
# メインモジュール
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import io
import sys
import wave

import openai
import pyaudio

from chat import ChatFactory
from monthly_usage import MonthlyUsage
from settings import Settings
from voicevox_api import VoicevoxAPI

APP_NAME = "ずんだGPT"
APP_VERSION = "0.1.0"
COPYRIGHT = "Copyright 2023 led-mirage"
SETTING_FILE = "settings.json"
MONTHLY_USAGE_FILE = "monthly_token_usage.json"

# メイン
def main():
    print_apptitle()

    settings = Settings(SETTING_FILE)
    settings.load()
    VoicevoxAPI.server = settings.get_voicevox_server()

    try:
        chat = ChatFactory.create(
                    settings.get_chat_api(),
                    settings.get_chat_model(),
                    settings.get_chat_instruction(),
                    settings.get_chat_bad_response(),
                    settings.get_chat_history_size())
    except ValueError as err:
        print(err)
        sys.exit()

    monthly_usage = MonthlyUsage(MONTHLY_USAGE_FILE)
    monthly_usage.load()

    while True:
        message = input("あなた > ")
        print()
        try:
            response, tokens = chat.send_message(message)
        except openai.AuthenticationError as err:
            print("APIの認証に失敗しました")
            print(err.message)
            sys.exit()
        except openai.NotFoundError as err:
            print("デプロイメントが見つかりません")
            print(err.message)
            sys.exit()

        monthly_usage.add_token(tokens)

        response = response.replace("。", "。;")
        sentences = response.split(";")
        print(f"{settings.get_chat_character_name()} > ")
        for text in sentences:
            if text != "":
                print(text)
                try:
                    text_to_speech(text,
                        settings.get_speaker_id(),
                        settings.get_speed_scale(),
                        settings.get_pitch_scale())
                except:
                    pass
        print()

# タイトルを表示する
def print_apptitle():
    print(f"----------------------------------------------------------------------")
    print(f" {APP_NAME} {APP_VERSION}")
    print(f"")
    print(f" {COPYRIGHT}")
    print(f"----------------------------------------------------------------------")
    print(f"")

# テキストを読み上げる
def text_to_speech(text, speaker_id, speed_scale, pitch_scale):
    query_json = VoicevoxAPI.audio_query(text, speaker_id)
    query_json["speedScale"] = speed_scale
    query_json["pitchScale"] = pitch_scale
    wave_data = VoicevoxAPI.synthesis(query_json, speaker_id)
    play_sound(wave_data)

# 音声データを再生する
def play_sound(wave_data):
    wave_file = wave.open(io.BytesIO(wave_data), 'rb')
    audio = pyaudio.PyAudio()

    try:
        format = audio.get_format_from_width(wave_file.getsampwidth())

        stream = audio.open(
            format=format,
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True)

        data = wave_file.readframes(1024)
        while data != b'':
            stream.write(data)
            data = wave_file.readframes(1024)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio.close()
        wave_file.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了します")
