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
&hrm_r RC(RSHFT) BACKSPACE ⌫
&kp GB_DQT "
&kp GB_HASH #
&kp GB_BSLH \
&kp GB_EURO €
&kp GB_AT @
&kp GB_POUND_SIGN £
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
&kp RCTRL ctrl
&kp RALT alt
&kp RWIN win
&kp RSHFT shift
&kp LEFT ⇐
&kp RIGHT ⇒
&kp UP ⇑
&kp DOWN ⇓
&kp SPACE ␣
&kp C_VOL_DN 🔉
&kp C_VOL_UP 🔊
&hrm_l LC(LSHFT) TAB tab
&spaces ⎵⎵⎵⎵
&kp ENTER ⏎
&kp DEL del
&kp LC(LEFT) ^⇐
&kp LC(RIGHT) ^⇒
&hrm_l LG(LC(LSHFT)) ESC esc
&kp HOME home
&kp END end
&kp INSERT ins
"""
raw_binding_map = dict(
    line.rsplit(maxsplit=1) for line in overrides.strip().splitlines()
)
raw_binding_map["&kp PG_UP"] = "pg up"
raw_binding_map["&kp PG_DN"] = "pg down"
raw_binding_map["&bt BT_CLR"] = {"tap": "BtClr", "hold": "FN"}
raw_binding_map["&bt BT_SEL 0"] = {"tap": "Bt1", "hold": "FN"}
raw_binding_map["&bt BT_SEL 1"] = {"tap": "Bt2", "hold": "FN"}
raw_binding_map["&kp ESC"] = "esc"
raw_binding_map["&semienter_caps LCAP 0"] = {"tap": ";⏎", "hold": "CAP"}
raw_binding_map["&hrm_l LC(LWIN) LWIN"] = "win"
raw_binding_map["&mkp LCLK"] = "left click"
raw_binding_map["&mkp RCLK"] = "right click"
raw_binding_map["&mkp MCLK"] = "middle click"
raw_binding_map["&mmv MOVE_LEFT"] = "mouse left"
raw_binding_map["&mmv MOVE_RIGHT"] = "mouse right"
raw_binding_map["&mmv MOVE_UP"] = "mouse up"
raw_binding_map["&mmv MOVE_DOWN"] = "mouse down"
raw_binding_map["&msc SCRL_LEFT"] = "scroll left"
raw_binding_map["&msc SCRL_RIGHT"] = "scroll right"
raw_binding_map["&msc SCRL_UP"] = "scroll up"
raw_binding_map["&msc SCRL_DOWN"] = "scroll down"
for char in string.ascii_uppercase:
    raw_binding_map[f"&kp {char}"] = char.lower()
    raw_binding_map[f"&kp LS({char})"] = char

combos = {
    "combo_all": {"hidden": True},
    "combo_brcs": {"hidden": True},
    "combo_cut": {"align": "bottom"},
    "combo_enter": {"hidden": True},
    "combo_esc": {"draw_separate": True},
    "combo_bt_clear": {"draw_separate": True},
    "combo_bt_sel1": {"draw_separate": True},
    "combo_bt_sel2": {"draw_separate": True},
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

# Replace implementation-oriented layer names wherever they appear as labels
# in keys, while keeping the actual firmware layer names intact.
layer_names = {
    "default": "BASE",
    "combos": "COMBOS",
    "CAP": "CAPS",
    "TAP": "CAP",
    "FUN": "FN",
    "NAV": "NAV",
}
for layer in config["layers"].values():
    for index, key in enumerate(layer):
        if not isinstance(key, dict):
            if key in layer_names:
                layer[index] = layer_names[key]
            continue
        for label in ("t", "h", "s", "l", "r", "tap", "hold", "shifted", "left", "right"):
            if key.get(label) in layer_names:
                key[label] = layer_names[key[label]]

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
del config["layers"]["CAP"]
for combo in config["combos"]:
    if "CAP" in combo["l"]:
        combo["l"].remove("CAP")
    # Move default combos to their own layer
    if "default" in combo["l"]:
        combo["l"] = ["combos"]
# Show combos second
config["layers"] = {
    "default": config["layers"]["default"],
    "combos": config["layers"]["combos"],
    **{name: layer for name, layer in config["layers"].items()},
}

# Use short, readable names in the published diagram. These are display
# names only; the layer names and bindings in the firmware stay unchanged.
config["layers"] = {
    layer_names.get(name, name): layer for name, layer in config["layers"].items()
}
for combo in config["combos"]:
    combo["l"] = [layer_names.get(name, name) for name in combo["l"]]

with tempfile.NamedTemporaryFile(mode="w+") as f:
    f.write(yaml.dump(config, sort_keys=False))
    f.flush()
    repo.joinpath(OUTPUT).write_text(
        check_output(["keymap", "draw", f.name], env=env, text=True)
    )
