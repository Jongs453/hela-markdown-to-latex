#!/bin/bash

echo "hex"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Script directory: $SCRIPT_DIR"
python3 $SCRIPT_DIR/hela.py "$PWD/$1"
