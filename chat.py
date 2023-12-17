# ZundaGPT
#
# チャットクラス
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import os
from datetime import datetime
from typing import Tuple

from openai import OpenAI
from openai import AzureOpenAI

# チャット基底クラス
class Chat:
    def __init__(self, client, model: str, instruction: str, bad_response: str, history_size: int, log_folder: str):
        self.messages = []
        self.client = client
        self.model = model
        self.instruction = instruction
        self.bad_response = bad_response
        self.history_size = history_size
        self.log_folder = log_folder
        self.chat_start_time = datetime.now()

    # メッセージを送信して回答を得る
    def send_message(self, text: str) -> Tuple[str, int]:
        self.messages.append({"role": "user", "content": text})
        messages = self.messages[-self.history_size:]
        messages.insert(0, {"role": "system", "content": self.instruction})
        response = self.client.chat.completions.create(model=self.model, messages=messages)
        role = response.choices[0].message.role
        content = response.choices[0].message.content
        if content:
            self.messages.append({"role": role, "content": content})
            self.write_chat_log()
            return content, response.usage.total_tokens
        else:
            return self.bad_response, 0
    
    # チャットのログを保存する
    def write_chat_log(self):
        if self.log_folder == "":
            return

        if not os.path.exists(self.log_folder):
            os.mkdir(self.log_folder)

        filename = self.chat_start_time.strftime("chatlog-%Y%m%d-%H%M%S.txt")
        path = os.path.join(self.log_folder, filename)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=4)
        
# OpenAI チャットクラス
class ChatOpenAI(Chat):
    def __init__(self, model: str, instruction: str, bad_response: str, history_size: int, log_folder: str):
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("環境変数 OPENAI_API_KEY が設定されていません。")

        client = OpenAI()
        super().__init__(
            client = client,
            model = model,
            instruction = instruction,
            bad_response = bad_response,
            history_size = history_size,
            log_folder = log_folder
        )

# Azure OpenAI チャットクラス
class ChatAzureOpenAI(Chat):
    def __init__(self, model: str, instruction: str, bad_response: str, history_size: int, log_folder: str):
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if endpoint is None:
            raise ValueError("環境変数 AZURE_OPENAI_ENDPOINT が設定されていません。")

        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("環境変数 AZURE_OPENAI_API_KEY が設定されていません。")

        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2023-05-15")
        super().__init__(
            client = client,
            model = model,
            instruction = instruction,
            bad_response = bad_response,
            history_size = history_size,
            log_folder = log_folder
        )

# チャットファクトリー
class ChatFactory:
    # api_idに基づいてChatオブジェクトを作成する
    @classmethod
    def create(cls, api_id: str, model: str, instruction: str, bad_response: str, history_size: int, log_folder: str) -> Chat:
        if api_id == "OpenAI":
            return ChatOpenAI(model, instruction, bad_response, history_size, log_folder)
        elif api_id == "AzureOpenAI":
            return ChatAzureOpenAI(model, instruction, bad_response, history_size, log_folder)
        else:
            raise ValueError("API IDが間違っています。")
