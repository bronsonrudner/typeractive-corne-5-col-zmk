# Typeractive Corne ZMK Config

![keymap-drawer logo](/corne.svg)

## Getting Started

Install [Docker Desktop](https://www.docker.com/products/docker-desktop),
[VS Code](https://code.visualstudio.com/) and
[Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

Clone the ZMK source repository

```bash
git clone https://github.com/zmkfirmware/zmk.git
```

Open the checkout directory in VS Code, and follow the prompt to `Reopen in Container`, then in the container run

```bash
west init -l app/
west update
```

Restart the container with

```bash
docker ps                    # List containers
docker stop "<container-id>" # Stop the container
```

Checkout this repo into the container with

```bash
cd /workspaces
git clone https://github.com/bronsonrudner/typeractive-corne-5-col-zmk zmk-config
```

and then `Add Folder to Workspace...`.

To test the build, run

```bash
(cd /workspaces/zmk && rm -rf build && west build -s app -d build/left -b nice_nano_v2 -S studio-rpc-usb-uart -- -DZMK_CONFIG=/workspaces/zmk-config/config -DSHIELD=corne_left)
```

To update the visual

```bash
apt update
apt install pipx
pipx install keymap-drawer
python3 -m pipx ensurepath
python3 draw.py
```
