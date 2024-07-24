#!/bin/bash

# CONFIGURATION OPTIONS #
# FILE_PATH="tests/basic.br" Currently does nothing (Coming in a future update!)
# COMPILER="node.js" Currently does nothing (Coming in a future update!)

if [ -z "$1" ]; then
  echo "Usage: $0 <file_path>"
  exit 1
fi

FILE_PATH=$1

node src/burst.js "$FILE_PATH"
