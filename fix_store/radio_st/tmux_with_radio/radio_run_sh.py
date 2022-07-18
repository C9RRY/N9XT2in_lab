import subprocess


def play_st(url):
    subprocess.call(['sh', '/home/c9rry/MyGit/N9XT2in_lab/fix_store/radio_st/tmux_with_radio/radio.sh', f'{url}'])


if __name__ == '__main__':
    play_st('https://online.radioroks.ua/RadioROKS')
