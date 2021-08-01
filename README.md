# SDSS_spec_downloader

**Here is a script to download SDSS optical spectra based on python.**

## Usage: 

Add the RA-DEC to the `spec_coord.txt` file, and the run:

```sh
$ python SSDer.py
```

The result will be in the `sdss` folder. There will be 3 types of outputted file:

* `spec-{plate}-{mjd}-{fiberID}.fits`: the spectrum fits file
* `spec-{plate}-{mjd}-{fiberID}.gif`: the spectrum preview
* `spec-{plate}-{mjd}-{fiberID}-image.gif`: the fiber position image preview

## More:

Please see the jupyter notebook to check the step-by-step details.