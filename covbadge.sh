#!/bin/bash

# Generate coverage report
coverage run -m pytest
coverage xml
genbadge coverage -i coverage.xml
