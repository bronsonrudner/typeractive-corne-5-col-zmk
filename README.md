# Typeractive Corne ZMK Config

![keymap-drawer logo](/corne.svg)

## Getting Started (Fedora)

```
sudo dnf -y install podman
git clone https://github.com/zmkfirmware/zmk.git
git clone https://github.com/bronsonrudner/typeractive-corne-5-col-zmk zmk-config
podman build -t zmk -f Dockerfile zmk/.devcontainer/
podman run --rm -it --security-opt label=disable --workdir /workspaces/zmk -v ../zmk:/workspaces/zmk -v .:/workspaces/zmk-config zmk /bin/bash west init -l app/
west update  
```

### Testing

Ensure you're In the `zmk-config` directory, and that the `zmk` directory is adjacent.
```
make test
```

### To update the visual

Install keymap-drawer
```bash
sudo dnf install pipx
pipx ensurepath
pipx install keymap-drawer
```

Then 
```bash
./draw.py
```
