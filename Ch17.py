import os
import time
import sys
import requests
from concurrent import futures

MAX_WORKERS = 20

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as f:
        f.write(img)


def get_flag(cc):
    url = f'{BASE_URL}/{cc.lower()}/{cc.lower()}.gif'
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f'{future} downloading {cc}')

        result = []
        for future in futures.as_completed(to_do):
            res = future.result()
            result.append(res)
            msg = f'{future} result: {res}'
            print(msg)

    return len(result)


def main(download_many):
    t0 = time.perf_counter()
    cnt = download_many(POP20_CC)
    elapsed = time.perf_counter() - t0
    msg = f'\n{cnt} flags downloaded in {elapsed:.2f}s'
    print(msg)


main(download_many)
