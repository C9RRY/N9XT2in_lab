#!/bin/bash
tmux kill-session -t first
tmux new -d -s first python3 $1/radio_play.py -url $2

