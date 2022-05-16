#!/bin/bash

celery -A webhost worker -E -l info -c 10 -n worker1@%h --max-tasks-per-child=5 --autoscale=10,3 --uid=nobody --gid=nogroup