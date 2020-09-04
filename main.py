import requests
import argparse

from shutil import copyfileobj

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

class xkcd:
    main_uri = 'https://xkcd.com/{}/info.0.json'
    img_link = 'https://imgs.xkcd.com/comics/{}.png'

    def __init__(self, comic_number, comic_title):
        self.comic_number = comic_number

        try:
            self.comic_title = comic_title.lower().replace(' ', '-')

        except:
            self.comic_title = comic_title

    def get_comic_info(self):
        return requests.get(self.main_uri.format(self.comic_number)).json()

    def get_comic(self):
        r = None

        if self.comic_number is None:
            r = requests.get(self.img_link.format(self.comic_title), stream=True)

        else:
            img_link = self.get_comic_info()['img']
            r = requests.get(img_link, stream=True)

        return r

    def output_comic(self, outfile):
        comic = self.get_comic()
        title = self.get_comic_info()['title'].lower().replace(' ', '-')

        if outfile:
            with open(f'{outfile}/{title}.png', 'wb') as fp:
                copyfileobj(comic.raw, fp)

    def print_comic_info(self):
        info = self.get_comic_info()

        title = info['title']
        date = '{} {}, {}'.format(MONTHS[info['month']], info['day'], info['year'])
        alt = info['alt']
        link = info['img']

        comic_info = f'"{title}"\n{date}\nAlt: {alt}\nLink: {link}'
        print(comic_info)


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

    args = parser.parse_args()

    if not (args.comic_number or args.comic_title):
        parser.error('Use of either --comic-number or --comic-title is required.')

    comic = xkcd(args.comic_number, args.comic_title)

    if args.outfile:
        comic.output_comic(args.outfile)

    if args.print_info:
        comic.print_comic_info()

if __name__ == '__main__':
    main()