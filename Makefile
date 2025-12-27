.PHONY: test

test:
	podman run --rm -it --security-opt label=disable --workdir /workspaces/zmk -v ../zmk:/workspaces/zmk -v .:/workspaces/zmk-config zmk /bin/bash -c 'rm -rf build && west build -s app -d build/left -b nice_nano -S studio-rpc-usb-uart -- -DZMK_CONFIG=/workspaces/zmk-config/config -DSHIELD=corne_left'
