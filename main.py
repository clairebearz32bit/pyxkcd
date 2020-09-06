import requests
import argparse

from shutil import copyfileobj
from PIL import Image

MONTHS = {
    '1': 'January',
    '2': 'February',
    '3': 'March',
    '4': 'April',
    '5': 'May',
    '6': 'June',
    '7': 'July',
    '8': 'August',
    '9': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}


def get_comic_info(comic_number):
    return requests.get(f'https://xkcd.com/{comic_number}/info.0.json').json()


class xkcd:
    main_uri = 'https://xkcd.com/{}/info.0.json'
    img_link = 'https://imgs.xkcd.com/comics/{}.png'

    def __init__(self, comic_number, comic_title, outfile):
        self.comic_number = comic_number
        self.outfile = outfile

        try:
            self.comic_title = comic_title.lower().replace(' ', '-')

        except AttributeError:
            self.comic_title = comic_title

    def get_comic_info(self):
        return requests.get(self.main_uri.format(self.comic_number)).json()

    def get_comic(self):
        if self.comic_number is None:
            r = requests.get(self.img_link.format(self.comic_title), stream=True)

        else:
            img_link = self.get_comic_info()['img']
            r = requests.get(img_link, stream=True)

        return r

    def output_comic(self):
        comic = self.get_comic()

        if self.outfile:
            with open(f'{self.outfile}.png', 'wb') as fp:
                copyfileobj(comic.raw, fp)

    def print_comic_info(self):
        info = self.get_comic_info()

        title = info['title']
        date = '{} {}, {}'.format(MONTHS[info['month']], info['day'], info['year'])
        alt = info['alt']
        link = info['img']

        comic_info = f'"{title}"\n{date}\nAlt: {alt}\nLink: {link}'
        print(comic_info)

    def open_comic(self):
        image = Image.open(f'{self.outfile}.png', 'r')
        image.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--comic-number',
                        type=int,
                        metavar='')
    parser.add_argument('-t', '--comic-title',
                        type=str,
                        metavar='')
    parser.add_argument('-o', '--outfile',
                        type=str,
                        metavar='')
    parser.add_argument('-p', '--print-info',
                        action='store_true',
                        default=False)
    parser.add_argument('-s', '--show-comic',
                        type=str,
                        metavar='')

    args = parser.parse_args()

    if not (args.comic_number or args.comic_title):
        parser.error('Use of either --comic-number or --comic-title is required.')

    comic = None

    if args.outfile:
        comic = xkcd(args.comic_number, args.comic_title, args.outfile)
        comic.output_comic()

    elif args.outfile is None and args.comic_title == '':
        comic = xkcd(args.comic_number, args.comic_title, get_comic_info(args.comic_number))

    if args.print_info:
        comic.print_comic_info()

    if args.show_comic and args.outfile:
        comic.open_comic()

    elif args.show_comic and not args.outfile:
        parser.error('The "output_comic" function is required to use this.')


if __name__ == '__main__':
    main()
