from radio import cli
import argparse


def play(url):
    cli.play_url(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='radio')
    parser.add_argument('-url', dest='url')

    args = parser.parse_args()
    play(args.url)
