#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd -P)"

for dir in "$SCRIPT_DIR"/*; do
    if [[ ! -d "$dir" ]]; then
        continue
    fi
    echo "$dir"

    image_name="moleculetest-$(basename "$dir")"
    docker build --pull "$dir" -t "$image_name"
done
