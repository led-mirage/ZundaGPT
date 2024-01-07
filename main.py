# ZundaGPT
#
# メインモジュール
#
# Copyright (c) 2023-2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import sys
from typing import List

import openai

from character import CharacterFactory
from chat import ChatFactory
from chat import Chat
from monthly_usage import MonthlyUsage
from settings import Settings
from voicevox_api import VoicevoxAPI

APP_NAME = "ずんだGPT"
APP_VERSION = "0.5.1"
COPYRIGHT = "Copyright 2023-2024 led-mirage"
SETTING_FILE = "settings.json"

settings = None
assistant_character = None
user_character = None

# メイン
def main():
    global settings, assistant_character, user_character

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

    assistant_character = CharacterFactory.create_assistant_character(settings)
    user_character = CharacterFactory.create_user_character(settings)

    while True:
        message = input("あなた > ")
        if message[0] == "@" or message[0] == "+" or message[0] == "-":
            if exec_command(message, chat):
                print()
                continue

        print()

        if settings.get_user_echo_enable() and user_character is not None:
            try:
                user_character.talk(message)
            except:
                pass

        print(f"{settings.get_chat_character_name()} > ")
        try:
            chat.send_message(message, outputChunk, outputSentence)
            print()
        except openai.AuthenticationError as err:
            print("APIの認証に失敗しました")
            print(err.message)
            sys.exit()
        except openai.NotFoundError as err:
            print("デプロイメントが見つかりません")
            print(err.message)
            sys.exit()

# チャット応答のチャンク出力用コールバック関数
def outputChunk(chunk):
    print(chunk, end="", flush=True)

# チャット応答のセンテンス読み上げ用コールバック関数
def outputSentence(sentence):
    if settings.get_assistant_echo_enable() and assistant_character is not None:
        try:
            assistant_character.talk(sentence)
        except:
            pass
    if not sentence.endswith("\n"):
        print()

# タイトルを表示する
def print_apptitle():
    print(f"----------------------------------------------------------------------")
    print(f" {APP_NAME} {APP_VERSION}")
    print(f"")
    print(f" {COPYRIGHT}")
    print(f"----------------------------------------------------------------------")
    print(f"")

# コマンドの実行
def exec_command(command, chat):
    words = command.lower().split()

    if words[0] == "@assistant":
        exec_command_assistant()
    elif words[0] == "@assistant_echo" or words[0] == "@echo":
        exec_command_assistant_echo(words)
    elif words[0] == "@assistant_tts_software" or words[0] == "@tts_software":
        exec_command_assistant_tts_software(words)
    elif words[0] == "@assistant_speaker_id" or words[0] == "@speaker_id":
        exec_command_assistant_speaker_id(words)
    elif words[0] == "@assistant_speed_scale" or words[0] == "@speed_scale":
        exec_command_assistant_speed_scale(words)
    elif words[0] == "@assistant_pitch_scale" or words[0] == "@pitch_scale":
        exec_command_assistant_pitch_scale(words)
    elif words[0] == "@user":
        exec_command_user()
    elif words[0] == "@user_echo":
        exec_command_user_echo(words)
    elif words[0] == "@user_tts_software":
        exec_command_user_tts_software(words)
    elif words[0] == "@user_speaker_id":
        exec_command_user_speaker_id(words)
    elif words[0] == "@user_speed_scale":
        exec_command_user_speed_scale(words)
    elif words[0] == "@user_pitch_scale":
        exec_command_user_pitch_scale(words)
    elif words[0] == "@prev" or words[0] == "-":
        exec_command_prev(chat)
    elif words[0] == "@next" or words[0] == "+":
        exec_command_next(chat)
    else:
        return False

    return True

# assistant情報の表示
def exec_command_assistant():
    print(f"echo         : {"on" if settings.get_assistant_echo_enable() else "off"}")
    print(f"tts_software : {settings.get_assistant_tts_software()}")
    print(f"speaker_id   : {settings.get_assistant_speaker_id()}")
    print(f"speed_scale  : {settings.get_assistant_speed_scale()}")
    print(f"pitch_scale  : {settings.get_assistant_pitch_scale()}")

# assistant_echoの設定
def exec_command_assistant_echo(words: List[str]):
    if len(words) == 1:
        if settings.get_assistant_echo_enable():
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
            settings.set_assistant_echo_enable(echo_enable)
            settings.save()
            if echo_enable:
                state = "有効"
            else:
                state = "無効"
            print(f"echoを{state}にしたのだ")
        else:
            print("無効なコマンドなのだ")

# assistant_tts_softwareの設定
def exec_command_assistant_tts_software(words: List[str]):
    global assistant_character

    if len(words) == 1:
        print(f"assistant_tts_softwareは {settings.get_assistant_tts_software()} なのだ")
    else:
        val = words[1].upper()
        if val == "VOICEVOX" or val == "AIVOICE":
            settings.set_assistant_tts_software(val)
            settings.save()
            assistant_character = CharacterFactory.create_assistant_character(settings)
            print(f"assistant_tts_softwareを '{val}' に変更したのだ")
        else:
            print("無効なコマンドなのだ")

# assistant_speaker_idの設定
def exec_command_assistant_speaker_id(words: List[str]):
    global assistant_character

    if len(words) == 1:
        print(f"assistant_speaker_idは {settings.get_assistant_speaker_id()} なのだ")
    else:
        val = " ".join(words[1:])
        settings.set_assistant_speaker_id(val)
        settings.save()
        assistant_character = CharacterFactory.create_assistant_character(settings)
        print(f"assistant_speaker_idを '{val}' に変更したのだ")

# assistant_speed_scaleの設定
def exec_command_assistant_speed_scale(words: List[str]):
    global assistant_character

    if len(words) == 1:
        print(f"assistant_speed_scaleは {settings.get_assistant_speed_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_assistant_speed_scale(val)
            settings.save()
            assistant_character = CharacterFactory.create_assistant_character(settings)
            print(f"assistant_speed_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# assistant_pitch_scaleの設定
def exec_command_assistant_pitch_scale(words: List[str]):
    global assistant_character

    if len(words) == 1:
        print(f"assistant_pitch_scaleは {settings.get_assistant_pitch_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_assistant_pitch_scale(val)
            settings.save()
            assistant_character = CharacterFactory.create_assistant_character(settings)
            print(f"assistant_pitch_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# user情報の表示
def exec_command_user():
    print(f"echo         : {"on" if settings.get_user_echo_enable() else "off"}")
    print(f"tts_software : {settings.get_user_tts_software()}")
    print(f"speaker_id   : {settings.get_user_speaker_id()}")
    print(f"speed_scale  : {settings.get_user_speed_scale()}")
    print(f"pitch_scale  : {settings.get_user_pitch_scale()}")

# user_echoの設定
def exec_command_user_echo(words: List[str]):
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

# user_tts_softwareの設定
def exec_command_user_tts_software(words: List[str]):
    global user_character

    if len(words) == 1:
        print(f"user_tts_softwareは {settings.get_user_tts_software()} なのだ")
    else:
        val = words[1].upper()
        if val == "VOICEVOX" or val == "AIVOICE":
            settings.set_user_tts_software(val)
            settings.save()
            user_character = CharacterFactory.create_user_character(settings)
            print(f"user_tts_softwareを '{val}' に変更したのだ")
        else:
            print("無効なコマンドなのだ")

# user_speaker_idの設定
def exec_command_user_speaker_id(words: List[str]):
    global user_character

    if len(words) == 1:
        print(f"user_speaker_idは {settings.get_user_speaker_id()} なのだ")
    else:
        val = " ".join(words[1:])
        settings.set_user_speaker_id(val)
        settings.save()
        user_character = CharacterFactory.create_user_character(settings)
        print(f"user_speaker_idを '{val}' に変更したのだ")

# user_speed_scaleの設定
def exec_command_user_speed_scale(words: List[str]):
    global user_character

    if len(words) == 1:
        print(f"user_speed_scaleは {settings.get_user_speed_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_user_speed_scale(val)
            settings.save()
            user_character = CharacterFactory.create_user_character(settings)
            print(f"user_speed_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# user_pitch_scaleの設定
def exec_command_user_pitch_scale(words: List[str]):
    global user_character

    if len(words) == 1:
        print(f"user_pitch_scaleは {settings.get_user_pitch_scale()} なのだ")
    else:
        try:
            val = float(words[1])
            settings.set_user_pitch_scale(val)
            settings.save()
            user_character = CharacterFactory.create_user_character(settings)
            print(f"user_pitch_scaleを {val} に変更したのだ")
        except:
            print("無効なコマンドなのだ")

# ひとつ前のチャット記録を読み込む
def exec_command_prev(chat: Chat):
    chat.load_prev()
    print_chat_messages(chat)

# ひとつ後のチャット記録を読み込む
def exec_command_next(chat: Chat):
    chat.load_next()
    print_chat_messages(chat)

# チャットメッセージ全体の再表示
def print_chat_messages(chat: Chat):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_apptitle()
    for message in chat.messages:
        if message["role"] == "user":
            print(f"あなた > {message["content"]}")
            print("")
        elif message["role"] == "assistant":
            print(f"{settings.get_chat_character_name()} > ")
            print(message["content"])
            print("")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了します")
