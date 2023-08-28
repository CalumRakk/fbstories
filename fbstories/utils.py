import json
from typing import List
from urllib.parse import urlparse
from pathlib import Path
import requests

headers = {
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Sec-GPC": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}
session = requests.Session()
session.headers.update(headers)


def check_cookies_for_facebook(listDict: List[dict]) -> bool:
    """
    Devuelve True si todos los name de cookies requeridos por facebook están presente en listDict
    Es importante que existan los siguientes `name` de cookies:  ["c_user","datr","fr","presence","sb","wd","xs"]
    """
    cookie_names_required = ["c_user", "datr", "fr", "presence", "sb", "wd", "xs"]
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
            "sameSite": get_value_of_sameSite(json_data),
        }
        if get_value_of_expires(json_data):
            cookie["expires"] = get_value_of_expires(json_data)

        cookies.append(cookie)
    return cookies


def load_cookies(cookies_path: str):
    path = Path(cookies_path)
    if path.exists() is False:
        print(
            "Alguno o todos de los `name` de cookies no está presente en las cookies proporcionadas."
        )
        exit()

    data = json.loads(path.read_text())
    cookies = parse_listDict_cookies(data)

    if check_cookies_for_facebook(cookies) is False:
        print("No se encontro el archivo que contiene las cookies")
        exit()
    return cookies


def get_filename_from_url(url) -> str:
    path = urlparse(url).path
    if path.endswith("/"):
        path = path[:-2]
    return path.split("/")[-1]
