#!/bin/sh
# По умолчанию (без TEST_ARGS=...) прогонит тесты и выведет короткий отчет о покрытии кода в консоль,
# создаст test_results/test_coverage/index.html полный отчет
COVERAGE_FILE=${COVERAGE_FILE:-.coverage}

if test -f ${COVERAGE_FILE}; then
  echo "Removing existing ${COVERAGE_FILE} file"
  rm ${COVERAGE_FILE}
fi
echo "Running tests with coverage enabled"
CURRENT_PATH=$(dirname "$0")
# Смотри список доступных флагов для TEST_ARGS по ссылкам ниже
# https://pytest-cov.readthedocs.io/en/latest/reporting.html
# https://pytest-cov.readthedocs.io/en/latest/config.html
# Некоторые настройки могут задаваться только в файле .coveragerc
# Смотри https://coverage.readthedocs.io/en/7.5.2/config.html
TEST_ARGS=${TEST_ARGS:---cov-report= --cov} sh ${CURRENT_PATH}/test.sh
sh ${CURRENT_PATH}/check_coverage.sh
