#!/bin/bash
tmux kill-session -t first
tmux new -s first \; split-window -h \; split-window -v python3 $1/radio_play.py -url $2 \; detach
