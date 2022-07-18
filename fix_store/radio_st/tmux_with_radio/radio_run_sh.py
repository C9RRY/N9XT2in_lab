import subprocess
from pathlib import Path


current_path = Path(__file__).resolve().parent.parent.parent


def play_st(url):
    subprocess.call(['sh', f'{Path(__file__).resolve().parent}/radio.sh',
                     f'{Path(__file__).resolve().parent}', f'{url}'])


if __name__ == '__main__':
    play_st('https://online.radioroks.ua/RadioROKS')
