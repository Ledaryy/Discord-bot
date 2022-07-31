#!/bin/bash

celery -A webhost worker -l info &
celery -A webhost beat -l info
