#
import argparse
from . import run, VERSION


def run_script():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="URL de la Facebook Story")
    parser.add_argument(
        "--cookies",
        default="cookies.json",
        help="Ruta del archivo json que contiene las cookies",
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="Gallery",
        help="Directorio para guardar las salidas",
    )
    parser.add_argument("--version", action="version", version=f"version: {VERSION}")

    args = parser.parse_args()
    run(url=args.url, cookies_path=args.cookies, output_dir=args.output_dir)
