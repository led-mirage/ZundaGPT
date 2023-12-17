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
APP_VERSION = "0.2.0"
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
                    settings.get_chat_history_size(),
                    settings.get_chat_log_folder())
    except ValueError as err:
        print(err)
        sys.exit()

    monthly_usage = MonthlyUsage(MONTHLY_USAGE_FILE)
    monthly_usage.load()

    while True:
        message = input("あなた > ")
        if message[0] == "@":
            exec_command(settings, message)
            print()
            continue

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

        if settings.get_user_echo_enable():
            try:
                text_to_speech(message,
                        settings.get_user_speaker_id(),
                        settings.get_user_speed_scale(),
                        settings.get_user_pitch_scale())
            except:
                pass

        monthly_usage.add_token(tokens)

        response = response.replace("。", "。;")
        sentences = response.split(";")
        print(f"{settings.get_chat_character_name()} > ")
        for text in sentences:
            if text != "":
                print(text)
                if settings.get_echo_enable():
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

# 設定コマンドの実行
def exec_command(settings, command):
    words = command.lower().split()

    if words[0] == "@echo":
        exec_command_echo(settings, words)
    elif words[0] == "@speaker_id":
        exec_command_speaker_id(settings, words)
    elif words[0] == "@speed_scale":
        exec_command_speed_scale(settings, words)
    elif words[0] == "@pitch_scale":
        exec_command_pitch_scale(settings, words)
    elif words[0] == "@user_echo":
        exec_command_user_echo(settings, words)
    elif words[0] == "@user_speaker_id":
        exec_command_user_speaker_id(settings, words)
    elif words[0] == "@user_speed_scale":
        exec_command_user_speed_scale(settings, words)
    elif words[0] == "@user_pitch_scale":
        exec_command_user_pitch_scale(settings, words)
    else:
        print("無効なコマンドなのだ")

# echoの設定
def exec_command_echo(settings, words):
    if len(words) == 1:
        if settings.get_echo_enable():
            state = "有効"
        else:
            state = "無効"
        print(f"echoは{state}なのだ")
    else:
        if words[1] == "on":
            echo_enable = True
        elif words[1] == "off":
            echo_enable = False
        else:
            echo_enable = None

        if echo_enable is not None:
            settings.set_echo_enable(echo_enable)
            settings.save()
            if echo_enable:
                state = "有効"
            else:
                state = "無効"
            print(f"echoを{state}にしたのだ")
        else:
            print("無効なコマンドなのだ")

# speaker_idの設定
def exec_command_speaker_id(settings, words):
    if len(words) == 1:
        print(f"speaker_idは {settings.get_speaker_id()} なのだ")
    else:
        try:
            val = int(words[1])
            settings.set_speaker_id(val)
            settings.save()
            print(f"speaker_idを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# speed_scaleの設定
def exec_command_speed_scale(settings, words):
    if len(words) == 1:
        print(f"speed_scaleは {settings.get_speed_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_speed_scale(val)
            settings.save()
            print(f"speed_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# pitch_scaleの設定
def exec_command_pitch_scale(settings, words):
    if len(words) == 1:
        print(f"pitch_scaleは {settings.get_pitch_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_pitch_scale(val)
            settings.save()
            print(f"pitch_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# user_echoの設定
def exec_command_user_echo(settings, words):
    if len(words) == 1:
        if settings.get_user_echo_enable():
            state = "有効"
        else:
            state = "無効"
        print(f"user_echoは{state}なのだ")
    else:
        if words[1] == "on":
            user_echo_enable = True
        elif words[1] == "off":
            user_echo_enable = False
        else:
            user_echo_enable = None

        if user_echo_enable is not None:
            settings.set_user_echo_enable(user_echo_enable)
            settings.save()
            if user_echo_enable:
                state = "有効"
            else:
                state = "無効"
            print(f"user_echoを{state}にしたのだ")
        else:
            print("無効なコマンドなのだ")

# user_speaker_idの設定
def exec_command_user_speaker_id(settings, words):
    if len(words) == 1:
        print(f"user_speaker_idは {settings.get_user_speaker_id()} なのだ")
    else:
        try:
            val = int(words[1])
            settings.set_user_speaker_id(val)
            settings.save()
            print(f"user_speaker_idを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# user_speed_scaleの設定
def exec_command_user_speed_scale(settings, words):
    if len(words) == 1:
        print(f"user_speed_scaleは {settings.get_user_speed_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_user_speed_scale(val)
            settings.save()
            print(f"user_speed_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# user_pitch_scaleの設定
def exec_command_user_pitch_scale(settings, words):
    if len(words) == 1:
        print(f"user_pitch_scaleは {settings.get_user_pitch_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_user_pitch_scale(val)
            settings.save()
            print(f"user_pitch_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了します")
