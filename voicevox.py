# ZundaGPT
#
# VOICEVOX制御用
#
# Copyright (c) 2023 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import subprocess

import psutil

# VOICEVOXの既定のインストール先を取得する
def get_default_voicevox_install_path():
    return "%LOCALAPPDATA%/Programs/VOICEVOX/VOICEVOX.exe"

# VOICEVOXが起動しているかどうかを調べる
def is_voicevox_running():
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower() == "voicevox.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# VOICEVOXが起動していなかったら起動する
def run_voicevox(voicevox_path):
    appdata_local = os.getenv("LOCALAPPDATA")
    voicevox_path = voicevox_path.replace("%LOCALAPPDATA%", appdata_local)
    if os.path.exists(voicevox_path):
        if not is_voicevox_running():
            subprocess.Popen(voicevox_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
