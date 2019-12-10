# Al-Co-W

Basic testing of a CALPHAD database for Co-based superalloys:
https://materialsdata.nist.gov/handle/11256/948

## Dependencies

This repository depends on [pycalphad][1]. The recommended means of
installation is through a [conda][2] environment:

```bash
$ conda create -n cobalt -c conda-forge python=3 matplotlib numpy pycalphad 
```

## Usage

After the "cobalt" environment has been built, activate it and run the script:

```bash
$ conda activate cobalt
$ python Al-Co.py
```

This will generate two files, `diagram.png` and `disorder.png`, showing the
Gibbs free energy and extent of disorder, respectively, at 1200 K.

<!--References-->
[1]: https://pycalphad.org
[2]: https://docs.conda.io/en/latest/miniconda.html
