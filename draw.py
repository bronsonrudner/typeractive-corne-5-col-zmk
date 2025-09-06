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
&kp GB_AT @
&kp POUND £
&kp GB_TILDE ~
&kp GB_PIPE |
&kp LC(X) Cut
&kp LC(C) Copy
&hls LC(LSHFT) LC(V) Paste
&kp LC(Z) Undo
&double_shift ⇧⇧
&kp LCTRL ✲
&kp LALT ⎇
&kp LWIN ❖
&kp LSHIFT ⇧
&kp LEFT 🡄
&kp RIGHT 🡆
&kp UP 🡅
&kp DOWN 🡇
&kp SPACE ␣
&kp C_VOL_DN 🔉
&kp C_VOL_UP 🔊
&caps_word CAPS_WORD
&num_word 1 NUM
&tdsh Shift
"""

combos_to_separate = ["enter", "r_enter", "cut", "escape", "caps", "brcs"]

overrides = dict(
    raw_binding_map=dict(line.rsplit(maxsplit=1) for line in overrides.strip().splitlines()),
    zmk_combos={f"combo_{combo}": {"draw_separate": "True"} for combo in combos_to_separate},
)

env = os.environ | {f"KEYMAP_{k}": json.dumps(v) for k, v in overrides.items()}

repo = Path(__file__).parent
with tempfile.NamedTemporaryFile(mode="w+") as f:
    f.write(check_output(["keymap", "parse", "-z", repo / "config/corne.keymap"], env=env, text=True))
    f.flush()
    repo.joinpath(OUTPUT).write_text(check_output(["keymap", "draw", f.name], env=env, text=True))
