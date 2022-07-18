#!/bin/bash
tmux kill-session -t first
tmux new -s first \; split-window -h \; split-window -v python3 /home/c9rry/MyGit/N9XT2in_lab/fix_store/radio_st/tmux_with_radio/radio_play.py -url $1 \; detach
