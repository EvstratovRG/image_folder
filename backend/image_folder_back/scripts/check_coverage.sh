#!/bin/sh
# Обработка .coverage выделена в отдельный скрипт
# Пороговое значение падение для покрытия кода задается fail_under в файле .coveragerc

COVERAGE_FILE=${COVERAGE_FILE:-.coverage}
TEST_COVERAGE_FILE_FORMAT=${TEST_COVERAGE_FILE_FORMAT:-html}
TEST_OUTPUT_DIR=${TEST_OUTPUT_DIR:-test_results}
TEST_COVERAGE_FILE_NAME=${TEST_COVERAGE_FILE_NAME:-coverage_results}

# отчет html ожидает папку в качестве аргумента вывода
if [ $TEST_COVERAGE_FILE_FORMAT = "html" ]; then
   COVERAGE_OUTPUT_ARGS="-d ${TEST_OUTPUT_DIR}/${TEST_COVERAGE_FILE_NAME}"
else
   COVERAGE_OUTPUT_ARGS="-o ${TEST_OUTPUT_DIR}/${TEST_COVERAGE_FILE_NAME}.${TEST_COVERAGE_FILE_FORMAT}"
fi
exit_code=0
if test -f ${COVERAGE_FILE}; then
  echo "Showing coverage report from ${COVERAGE_FILE} file"
  python -m coverage report --data-file=${COVERAGE_FILE}
  exit_code=$?
  if ! [ $TEST_COVERAGE_FILE_FORMAT = "report" ] && ! [ $exit_code -eq 1 ]; then
    echo "Preparing coverage ${TEST_COVERAGE_FILE_FORMAT} report from ${COVERAGE_FILE} file"
    python -m coverage ${TEST_COVERAGE_FILE_FORMAT} --data-file=${COVERAGE_FILE} ${COVERAGE_OUTPUT_ARGS}
    exit_code=$?
  fi
else
  echo "No ${COVERAGE_FILE} file - nothing to do"
  exit 0
fi
if [ $exit_code -eq 0 ]; then
  echo "Code coverage OK. Good job."
  exit 0
elif [ $exit_code -eq 2 ]; then
  echo "Code coverage decreased. Write more tests."
  exit 1
else
  echo "Code coverage error."
  exit 1
fi
