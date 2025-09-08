#!/bin/python3
"""Updates the keymap diagram, using https://github.com/caksoylar/keymap-drawer"""
import json
import os
import string
import tempfile
from pathlib import Path
from subprocess import check_output

import yaml

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
&kp LC(V) Paste
&kp LC(Z) Undo
&double_shift ⇧⇧
&kp LCTRL ctrl
&kp LALT alt
&kp LWIN win
&kp LSHFT shift
&kp LEFT 🡄
&kp RIGHT 🡆
&kp UP 🡅
&kp DOWN 🡇
&kp SPACE ␣
&kp C_VOL_DN 🔉
&kp C_VOL_UP 🔊
&kp LS(TAB) ⇧Tab
&hls LC(LSHFT) TAB Tab
&spaces ⎵⎵⎵⎵
"""
raw_binding_map=dict(line.rsplit(maxsplit=1) for line in overrides.strip().splitlines())
for char in string.ascii_uppercase:
    raw_binding_map[f"&kp {char}"] = char.lower()
    raw_binding_map[f"&kp LS({char})"] = char

# combos_to_separate = ["enter", "r_enter", "cut", "caps"]
# combos = {f"combo_{combo}": {"draw_separate": "True"} for combo in combos_to_separate}
combos = {
    "combo_brcs": {"hidden": True},
    "combo_cut": {"align": "top"},
    "combo_enter": {"hidden": True},
}

overrides = dict(
    raw_binding_map=raw_binding_map,
    zmk_combos=combos,
)

env = os.environ | {f"KEYMAP_{k}": json.dumps(v) for k, v in overrides.items()}

repo = Path(__file__).parent
with tempfile.NamedTemporaryFile(mode="w+") as f:
    config = check_output(["keymap", "parse", "-z", repo / "config/corne.keymap", "--virtual-layers", "combos"], env=env, text=True)
    data = yaml.safe_load(config)
    for combo in data["combos"]:
        if "default" in combo["l"]:
            combo["l"] = ["combos"]
        elif any(combo["k"] == other_combo["k"] for other_combo in data["combos"] if other_combo != combo):
            combo["hidden"] = True
    new_config = yaml.dump(data, sort_keys=False)
    f.write(new_config)
    f.flush()
    repo.joinpath(OUTPUT).write_text(check_output(["keymap", "draw", f.name], env=env, text=True))
