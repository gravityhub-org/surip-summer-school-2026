"""Download and inspect PE samples."""

from pathlib import Path
import urllib.request

ROOT   = Path(__file__).resolve().parents[1]
PE_DIR = ROOT / "data" / "PE"
PE_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "GW150914": "https://dcc.ligo.org/public/0157/P1800370/005/GW150914_GWTC-1.hdf5",
    "GW170817": "https://dcc.ligo.org/public/0157/P1800370/005/GW170817_GWTC-1.hdf5",
    "GW170814": "https://dcc.ligo.org/public/0157/P1800370/005/GW170814_GWTC-1.hdf5",
}

for event, url in URLS.items():
    out = PE_DIR / f"{event}.hdf5"
    if out.exists():
        print(f"  [cache] {event}")
    else:
        print(f"  [download] {event} ...")
        urllib.request.urlretrieve(url, out)
        print(f"  saved → {out.name}")

# inspect structure
import h5py

for event in URLS:
    path = PE_DIR / f"{event}.hdf5"
    print(f"\n{'='*50}\n{event}\n{'='*50}")
    with h5py.File(path, "r") as f:
        f.visititems(lambda name, obj: print(f"  {name}"))