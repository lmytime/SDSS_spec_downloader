import warnings
warnings.filterwarnings("ignore")

#---------------------
# Search radius [arcsec]:
radius = 2
#---------------------


def sdss_image_preview(cat):
    from PIL import Image
    import requests
    import pandas as pd
    for _, row in cat.iterrows():
        ra = row['ra']
        dec = row['dec']
        plate = row['plate']
        mjd = row['mjd']
        fiberID = row['fiberID']
        url = f"http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.Image&ra={ra}&dec={dec}&scale=0.2&width=512&height=512&opt=SLG&query=&Grid=on&Label=on&SpecObjs=on"
#         print(f"image-{ra=:.4f}-{dec=:.4f}.gif Preview link:")
#         print(url)

        im = Image.open(requests.get(url, stream=True).raw)
        im.save(f"sdss/spec-{plate:04d}-{mjd:05d}-{fiberID:04d}-image.gif" , quality='keep')
    return im

def sdss_spec_download(cat):
    import requests
    import pandas as pd
    for _, row in cat.iterrows():
        plate = row['plate']
        mjd = row['mjd']
        fiberID = row['fiberID']
        run2d = row['run2d'].decode("utf-8") 
        url = f"https://dr16.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/{plate:04d}/spec-{plate:04d}-{mjd:05d}-{fiberID:04d}.fits"
#         print(f"spec-{plate:04d}-{mjd:05d}-{fiberID:04d}.fits Download link:")
#         print(url)

        r = requests.get(url, allow_redirects=True)
        open(f"sdss/spec-{plate:04d}-{mjd:05d}-{fiberID:04d}.fits", 'wb').write(r.content)

def sdss_spec_preview(cat):
    from PIL import Image
    import requests
    import pandas as pd
    for _, row in cat.iterrows():
        plate = row['plate']
        mjd = row['mjd']
        fiberID = row['fiberID']
        specobjid = row['specobjid']
        url = f"http://skyserver.sdss.org/dr16/en/get/SpecById.ashx?id={specobjid}"
#         print(f"spec-{plate:04d}-{mjd:05d}-{fiberID:04d}.gif Preview link:")
#         print(url)

        im = Image.open(requests.get(url, stream=True).raw)
        im.save(f"sdss/spec-{plate:04d}-{mjd:05d}-{fiberID:04d}.gif", quality='keep')
    return im

import pandas as pd
import astropy.units as u
from astropy import coordinates as coords
from astroquery.sdss import SDSS
spec_coord = pd.read_csv("spec_coord.txt")
for _,obj in spec_coord.iterrows():
    ra = obj['RA']
    dec = obj['DEC']
    pos = coords.SkyCoord(f"{ra}d {dec}d", frame='fk5')
    print(pos)

    xid = SDSS.query_region(pos, spectro=True, radius=radius*u.arcsec, data_release=16)
    print(xid)
    sdss_image_preview(xid.to_pandas())
    sdss_spec_download(xid.to_pandas())
    sdss_spec_preview(xid.to_pandas())
    print("Downloading OK!\n")