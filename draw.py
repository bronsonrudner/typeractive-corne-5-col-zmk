#!/bin/python3
"""Updates the keymap diagram, using https://github.com/caksoylar/keymap-drawer"""
import json
import os
from pathlib import Path
from subprocess import check_output
import tempfile

OUTPUT = "corne.svg"
# https://github.com/caksoylar/keymap-drawer/blob/main/CONFIGURATION.md
overrides = r"""
&kp BACKSPACE ⌫
&kp GB_DQT "
&kp GB_HASH #
&kp GB_BSLH \
&kp GB_EURO €
&kp POUND £
&kp GB_TILDE ~
&kp GB_PIPE |
&kp LC(X) ✂
&kp LC(C) 🗐
&kp LC(V) 📋
&double_shift ⇧⇧
&kp LCTRL ✲
&kp LALT ⎇
&kp LWIN ❖
&kp LSHIFT ⇧
&kp ENTER ⏎
&kp DEL ⌦
&kp LEFT 🡄
&kp RIGHT 🡆
&kp UP 🡅
&kp DOWN 🡇
&kp SPACE ␣
&kp TAB ⇥
&kp C_VOL_DN 🔉
&kp C_VOL_UP 🔊
&caps_word CAPS_WORD
"""

repo = Path(__file__).parent
overrides_dict = dict(line.rsplit(maxsplit=1) for line in overrides.strip().splitlines())
env = os.environ | dict(KEYMAP_raw_binding_map=json.dumps(overrides_dict), KEYMAP_separate_combo_diagrams="True")
with tempfile.NamedTemporaryFile(mode="w+") as f:
    f.write(check_output(["keymap", "parse", "-z", repo / "config/corne.keymap"], env=env, text=True))
    f.flush()
    repo.joinpath(OUTPUT).write_text(check_output(["keymap", "draw", f.name], env=env, text=True))
