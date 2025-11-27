import datetime
import requests
import xarray as xr
import json
import os
import numpy as np

BASE="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
STATIC_DIR=os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

VARIABLE_QUERIES={
    "temperature":"&lev_2_m_above_ground=on&var_TMP=on",
    "humidity":"&lev_2_m_above_ground=on&var_RH=on",
    "pressure":"&lev_mean_sea_level=on&var_PRMSL=on",
    "wind_u":"&lev_10_m_above_ground=on&var_UGRD=on",
    "wind_v":"&lev_10_m_above_ground=on&var_VGRD=on"
}

DECIMATE=8

def get_latest_cycle():
    now=datetime.datetime.utcnow()
    date=now.strftime("%Y%m%d")
    hour=now.hour

    if hour>=21: cycle="18"
    elif hour>=15: cycle="12"
    elif hour>=9: cycle="06"
    elif hour>=3: cycle="00"
    else:
        yesterday=now-datetime.timedelta(days=1)
        date=yesterday.strftime("%Y%m%d")
        cycle="18"

    return date, cycle

def fetch_and_convert():
    date, cycle=get_latest_cycle()
    print("Fetching data:", date, cycle)

    for name, query in VARIABLE_QUERIES.items():
        try:
            print("Downloading:", name)
            url=f"{BASE}?file=gfs.t{cycle}z.pgrb2.0p25.f000{query}&dir=%2Fgfs.{date}%2F{cycle}%2Fatmos"

            r=requests.get(url, timeout=60)
            r.raise_for_status()

            grib_path=os.path.join(STATIC_DIR, f"{name}.grib2")
            with open(grib_path, "wb")as f:
                f.write(r.content)

            print("Reading GRIB...")
            ds=xr.open_dataset(grib_path, engine="cfgrib")

            var=list(ds.data_vars)[0]
            arr=ds[var].values
            lats=ds["latitude"].values
            lons=ds["longitude"].values

            if arr.ndim==3:
                arr=arr[0]

            arr_small=arr[::DECIMATE, ::DECIMATE]
            lat_small=lats[::DECIMATE]
            lon_small=lons[::DECIMATE]

            out={
                "lat": lat_small.tolist(),
                "lon":lon_small.tolist(),
                "value":arr_small.tolist()
            }

            json_path=os.path.join(STATIC_DIR, f"{name}.json")
            with open(json_path, "w")as jf:
                json.dump(out, jf)

            ds.close()
            print(name, "saved →", json_path)

        except Exception as e:
            print("ERROR processing", name, "→", e)

if __name__=="__main__":
    fetch_and_convert()