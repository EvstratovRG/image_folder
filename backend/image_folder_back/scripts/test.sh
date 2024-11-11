#!/bin/sh
python -m tests.pre_start && python -m pytest ${TEST_ARGS} -v
