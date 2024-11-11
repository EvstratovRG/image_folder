#!/bin/sh
mypy ${CHECK_TYPES_ARGS} src && exit_code=0 || exit_code=$?

if [ $exit_code -eq 0 ]; then
  exit 0
else
  exit 1
fi
