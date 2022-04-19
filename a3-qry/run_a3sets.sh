#!/bin/usr/env bash

for file in reach.in.*; do
    python3 a3sets.py $file
done
