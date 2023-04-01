#!/bin/bash
set -e -v

echo "Creating and filling tables from HW3 solution..."
./hw3_soln.sh

echo "Running..."
python3 ./python_db_example.py
