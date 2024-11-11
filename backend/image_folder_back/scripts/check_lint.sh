#!/bin/sh
SRC_DIR="."

if [ -n "${XML_OUTPUT_FILE}" ]; then
  LINT_ARGS="--output-format junit --output-file ${XML_OUTPUT_FILE} ${SRC_DIR}"
  ruff check ${LINT_ARGS}
fi

if [ -n "${JSON_OUTPUT_FILE}" ]; then
  LINT_ARGS="--output-format json --output-file ${JSON_OUTPUT_FILE} ${SRC_DIR}"
  ruff check ${LINT_ARGS}
fi

ruff check ${SRC_DIR}
