#!/bin/bash

python3 -m scraper.main --dry-run

crond -f
