#!/bin/sh
SRC_DIR="."

ruff format --check ${SRC_DIR} && exit_code=0 || exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo 'Code style is OK. Good job.'
  if [ -n "${CODE_STYLE_XML_OUTPUT_FILE}" ]; then
    echo \
      '<?xml version="1.0" ?>
      <testsuites disabled="0" errors="0" failures="1" tests="1" time="0.0">
        <testsuite disabled="0" errors="0" failures="0" name="Ruff formatter" skipped="0" tests="1" time="0" file="">
          <testcase name="Check passed" file=""/>
        </testsuite>
      </testsuites>' \
      > ${CODE_STYLE_XML_OUTPUT_FILE}
  fi
  exit 0
elif [ $exit_code -eq 1 ]; then
  echo 'Please, run format_code.sh script on local machine.'
  if [ -n "${CODE_STYLE_XML_OUTPUT_FILE}" ]; then
    echo \
      '<?xml version="1.0" ?>
      <testsuites disabled="0" errors="0" failures="1" tests="1" time="0.0">
        <testsuite disabled="0" errors="0" failures="1" name="Ruff formatter" skipped="0" tests="1" time="0" file="">
          <testcase name="Ruff formatter fail, run format_code.sh script on local machine" file="">
            <failure type="failure" message="Ruff formatter would reformat code."/>
          </testcase>
        </testsuite>
      </testsuites>' \
      > ${CODE_STYLE_XML_OUTPUT_FILE}
  fi
  exit 1
else
  echo "Ruff error."
  exit 1
fi
