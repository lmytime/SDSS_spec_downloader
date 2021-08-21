import argparse
import requests
import time
from os.path import join
import csv

from requests.exceptions import HTTPError


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output_dir', type=str, default='./dr16', help='where the download files are stored', required=True)
parser.add_argument('-m', '--multiprocessing', action='store_true', default=False)
parser.add_argument('-n', '--n_process', type=int, default=8, help='how many process to use')
parser.add_argument('-l', '--list', type=str, default='spec.csv', help='csv file of the plate-mjd-fiberID information')
parser.add_argument('-e', '--err', type=str, default='err.csv', help='csv file of failed information')
args = parser.parse_args()


output_dir = args.output_dir
error_list = []


def download_by_crossid(info):
    global output_dir
    global error_list
    plate, mjd, fiberID = info
    mjd = mjd.rjust(5, '0')
    fiberID = fiberID.rjust(4, '0')
    path = join(output_dir, f'spec-{plate}-{mjd}-{fiberID}.fits')
    url = f"https://dr16.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/{plate}/spec-{plate}-{mjd}-{fiberID}.fits"
    print(url)
    try:
        r = requests.get(url=url, allow_redirects=True)
        with open(path, 'wb') as f:
            f.write(r.content)
    except:
        error_list.append(info)


if __name__ == '__main__':
    start = time.time()
    rows = []
    with open(args.list, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for info in reader:
            rows.append(info)
    if args.multiprocessing:
        from multiprocessing import Pool
        with Pool(processes=args.n_process) as p:
            p.map(download_by_crossid, rows)
    else:
        from tqdm import tqdm
        for info in tqdm(rows):
            download_by_crossid(info)
    with open(args.err, 'w', newline='', encoding='utf-8') as e:
        writer = csv.DictWriter(e, fieldnames=['plate', 'mjd', 'fiberID'])
        writer.writeheader()
        for row in error_list:
            plate, mjd, fiberID = row
            writer.writerow({'plate': plate, 'mjd': mjd, 'fiberID': fiberID})
    print('Download Finished in %.2f seconds!' % (time.time()-start))
    print('%d fits files to be downloaded, %d fits files were successfully downloaded, %d fits files failed!' % (len(rows), len(rows)-len(error_list), len(error_list)))

