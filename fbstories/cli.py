
import argparse
import os
from . import run
from .utils import load_cookies, http_download

def run_script():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="URL de la Facebook Story")
    parser.add_argument("--cookies", default="cookies.json", help="Ruta del archivo json que contiene las cookies")
    parser.add_argument("--output_dir", "-o", type=str, default=".", help="Directorio para guardar las salidas")

    args = parser.parse_args().__dict__
    url: str= args.pop("url")
    output_dir: str = args.pop("output_dir")
    cookies_path: str= args.pop("cookies")

    os.makedirs(output_dir, exist_ok=True)
    cookies= load_cookies(cookies_path)

    metadata = run(url, cookies=cookies)
    for index, dl_url in enumerate(metadata["urls"],start=1):
        r= http_download(dl_url, output_dir)
        print(index, os.path.basename(r))
