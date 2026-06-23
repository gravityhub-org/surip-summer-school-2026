import os
import urllib.request
from pathlib import Path
import tarfile
from gwpy.timeseries import TimeSeries
from pesummary.gw.fetch import fetch_open_samples

datadir = Path('./data')
datadir.mkdir(exist_ok=True)

trigger_time = 1126259462.4
duration = 4  # Analysis segment duration
post_trigger_duration = 2  # Time between trigger time and end of segment
end_time = trigger_time + post_trigger_duration
start_time = end_time - duration

print("Downloading public strain data, this may take a while...")
gwosc_url = "https://gwosc.org/archive/data/O1_16KHZ/1126170624/"
for det in ['H1', 'L1']:
    print("\tDownloading data for", det)
    filename = f"{det[0]}-{det}_LOSC_16_V1-1126256640-4096.gwf"
    urllib.request.urlretrieve(f"{gwosc_url}/{filename}", filename=datadir/filename)

print("Downloading public PE results")
# GW231123 Discovery PE results
fetch_open_samples(
    "GW231123_135430", version=1, read_file=False, delete_on_exit=False,
    outdir="./data", unpack=False
)
discovery_result = datadir / "posterior_samples.tar.gz"
if tarfile.is_tarfile(discovery_result):
    with tarfile.open(discovery_result) as f:
        f.extractall(path=datadir)
old_filename = Path(datadir / "posterior_samples.h5")
rename_path = old_filename.with_name("S231123cg_discovery_pesummary.hdf5")
old_filename.rename(rename_path)

# GW231123 GWTC-4.0 PE results
fetch_open_samples(
    "GW231123_135430", catalog="GWTC-4.0", read_file=False, delete_on_exit=False,
    outdir="./data", unpack=False
)

# GW150914 Public PE results (GWTC-2.1)
fetch_open_samples(
    "GW150914", catalog="GWTC-2.1-confident", read_file=False, delete_on_exit=False,
    outdir="./data", unpack=False
)