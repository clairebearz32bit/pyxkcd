import requests
import argparse

from shutil import copyfileobj

class xkcd:
    main_uri = 'https://xkcd.com/{}/info.0.json'
    img_link = 'https://imgs.xkcd.com/comics/{}.png'

    def __init__(self, comic_number, comic_title):
        self.comic_number = comic_number

        try:
            self.comic_title = comic_title.lower().replace(' ', '-')

        except:
            self.comic_title = comic_title

    def getComicInfo(self):
        return requests.get(self.main_uri.format(self.comic_number)).json()

    def getComic(self):
        r = None

        if self.comic_number is None:
            r = requests.get(self.img_link.format(self.comic_title), stream=True)

        else:
            img_link = self.getComicInfo()['img']
            r = requests.get(img_link, stream=True)

        return r

    def outputComic(self):
        comic = self.getComic()

        if self.comic_title:
            outfile = self.comic_title

        else:
            outfile = self.getComicInfo()['img'].split('/comics/')[1].replace('.png', '').replace('.jpg', '')

        with open('{}.png'.format(outfile), 'wb') as fp:
            copyfileobj(comic.raw, fp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--comic-number',
                        type=int,
                        metavar='')
    parser.add_argument('-t', '--comic-title',
                        type=str,
                        metavar='')

    args = parser.parse_args()

    if not (args.comic_number or args.comic_title):
        parser.error('Use of either --comic-number or --comic-title is required.')

    comic = xkcd(args.comic_number, args.comic_title)
    comic.outputComic()

if __name__ == '__main__':
    main()