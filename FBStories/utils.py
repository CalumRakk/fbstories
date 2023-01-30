
import re
import json
import os
from typing import List
from urllib.parse import urlparse

import requests
from requests.exceptions import ChunkedEncodingError


headers = {
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Sec-GPC': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document'
}
session = requests.Session()


def check_cookies_for_facebook(listDict: List[dict]) -> bool:
    """   
    Devuelve True si todos los name de cookies requeridos por facebook están presente en listDict    
    Es importante que existan los siguientes `name` de cookies:  ["c_user","datr","fr","presence","sb","wd","xs"]
    """
    cookie_names_required = ["c_user", "datr",
                             "fr", "presence", "sb", "wd", "xs"]
    for json_date in listDict:
        if json_date["name"] in cookie_names_required:
            cookie_names_required.remove(json_date["name"])

    if len(cookie_names_required) > 0:
        return False
    return True


def parse_listDict_cookies(listDict: List[dict]):
    """
    Devuelve una nueva lista de diccionario parseados segun el schema de playwright (al menos lo intenta).

    Args:
        listDict: debe ser una Lista de Diccionarios (de cookies)
    """
    assert type(listDict) is list

    # Lista de campos requeridos y opcionales para un objeto cookie https://playwright.dev/docs/api/class-browsercontext

    def get_value_of_expires(data_json: dict):
        if data_json.get("expires"):
            return data_json["expires"]
        return data_json.get("expirationDate")

    def get_value_of_sameSite(data_json: dict):
        if data_json["sameSite"] in ["Strict", "Lax", "None"]:
            return data_json["sameSite"]
        return "None"

    cookies = []
    for json_data in listDict:
        cookie = {
            "name": json_data["name"],
            "value": json_data["value"],
            "domain": json_data["domain"],
            "path": json_data["path"],
            "httpOnly": json_data["httpOnly"],
            "secure": json_data["secure"],
            "sameSite": get_value_of_sameSite(json_data)
        }
        if get_value_of_expires(json_data):
            cookie["expires"] = get_value_of_expires(json_data)

        cookies.append(cookie)
    return cookies


def load_cookies(cookies_path: str):
    if not os.path.exists(cookies_path):
        print("Alguno o todos de los `name` de cookies no está presente en las cookies proporcionadas.")
        exit()

    data = read_json_file(cookies_path)
    cookies = parse_listDict_cookies(data)
    
    if check_cookies_for_facebook(cookies) is False:
        print("No se encontro el archivo que contiene las cookies")
        exit()    
    return cookies
        
    


def parse_netscape_cookies(file) -> dict:
    cookies = []
    with open(file) as f:
        for line in f:
            if line.startswith("#") or line == "\n":
                continue
            fields = re.split(r"\s+", line.strip())
            cookies.append({
                "name": fields[5],
                "value": fields[6],
                "domain": fields[0],
                "path": fields[2],
                "expires": float(fields[4]),
                "httpOnly": False,
                "secure": fields[3] == "TRUE",
                "sameSite": "None"
            })
    return cookies


def read_json_file(path: str):
    with open(path, "r", encoding="UTF-8") as f:
        return json.load(f)


def http_download(url, output_dir):
    r = session.get(url, headers=headers, stream=True)
    r.raise_for_status()

    filename = get_filename_url(url)
    path = os.path.join(output_dir, filename)

    total_length = int(r.headers.get("Content-Length"))
    count = 0
    while True:
        try:
            with open(path, "wb") as fout:
                for chunk in r.iter_content(chunk_size=10000000):
                    fout.write(chunk)
                    count += len(chunk)

            if count == total_length:
                return path
        except ChunkedEncodingError:
            r = session.get(url, headers=headers, stream=True)
            r.raise_for_status()
            continue


def get_filename_url(url) -> str:    
    path = urlparse(url).path
    if path.endswith("/"):
        path = path[:-2]
    return path.split("/")[-1]

