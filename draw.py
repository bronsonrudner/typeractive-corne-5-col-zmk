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
&kp LC(BACKSPACE) ^⌫
&kp GB_DQT "
&kp GB_HASH #
&kp GB_BSLH \
&kp GB_EURO €
&kp GB_AT @
&kp POUND £
&kp GB_TILDE ~
&kp GB_PIPE |
&kp LC(X) cut
&kp LC(C) copy
&kp LC(V) paste
&kp LC(Z) undo
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
&kp LS(TAB) ⇧tab
&hls LC(LSHFT) TAB tab
&spaces ⎵⎵⎵⎵
&kp ENTER ⏎
&kp DEL del
&kp LC(DEL) ^del
&kp LC(LEFT) ^🡄
&kp LC(RIGHT) ^🡆
"""
raw_binding_map = dict(
    line.rsplit(maxsplit=1) for line in overrides.strip().splitlines()
)
for char in string.ascii_uppercase:
    raw_binding_map[f"&kp {char}"] = char.lower()
    raw_binding_map[f"&kp LS({char})"] = char

combos = {
    "combo_brcs": {"hidden": True},
    "combo_cut": {"align": "bottom"},
    "combo_enter": {"hidden": True},
}

overrides = dict(
    raw_binding_map=raw_binding_map,
    zmk_combos=combos,
)

env = os.environ | {f"KEYMAP_{k}": json.dumps(v) for k, v in overrides.items()}

repo = Path(__file__).parent
raw_config = check_output(
    [
        "keymap",
        "parse",
        "-z",
        repo / "config/corne.keymap",
        "--virtual-layers",
        "combos",
    ],
    env=env,
    text=True,
)
config = yaml.safe_load(raw_config)
# Don't repeat any default combos in other layers
for combo in config["combos"]:
    if "default" not in combo["l"]:
        if any(
            combo["k"] == other_combo["k"]
            for other_combo in config["combos"]
            if "default" in other_combo["l"]
        ):
            combo["hidden"] = True
# Don't show the CAP layer at all
for combo in config["combos"]:
    if "CAP" in combo["l"]:
        combo["l"].remove("CAP")
    if "default" in combo["l"]:
        combo["l"] = ["combos"]
del config["layers"]["CAP"]
# Show combos second
config["layers"] = {
    "default": config["layers"]["default"],
    "combos": config["layers"]["combos"],
    **{name: layer for name, layer in config["layers"].items()},
}

with tempfile.NamedTemporaryFile(mode="w+") as f:
    f.write(yaml.dump(config, sort_keys=False))
    f.flush()
    repo.joinpath(OUTPUT).write_text(
        check_output(["keymap", "draw", f.name], env=env, text=True)
    )
