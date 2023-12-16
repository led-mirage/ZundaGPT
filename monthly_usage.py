# ZundaGPT
#
# 利用量記録クラス
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
from datetime import date

class MonthlyUsage:
    def __init__(self, filepath):
        self.usages = {}
        self.filepath = filepath
        self.load()

    def add_token(self, tokens):
        key = self._get_key()
        if key in self.usages:
            self.usages[key] += tokens
        else:
            self.usages[key] = tokens
        self.save()

    def _get_key(self):
        today = date.today()
        return f"{today.year}/{today.month}"

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.usages, file, ensure_ascii=False, indent=4)

    def load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                self.usages = json.load(file)
        except:
            pass
