import json
from typing import Union
from pathlib import Path

from lxml import html
from playwright.sync_api import sync_playwright
from .utils import load_cookies, session, get_filename_from_url, download_url


def get_html(url: str, cookies: dict) -> str:
    """Devuelve el HTML de una página de facebook story.

    - Se requiere cookies porque las URL de las stories de Facebook son una url protegida y requieren de autenticación para poder acceder.
    - Una URL de story de Facebook basta para acceder a todos los medios (fotos y videos) de esa story

    Args:
        url: url de la story, ejemplo: `https://web.facebook.com/stories/143555469917`
        cookies: Es una lista de diccionario
    Returns:
        Devuelve un string que contiene el contenido html de la story.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        )
        page = context.new_page()
        context.add_cookies(cookies)

        page.goto(url)
        # https://www.facebook.com/index.php?next=https://www.facebook.com/stories/ID
        if "index.php?" in page.url:
            print(
                "Se redireccionó la página a index.php?. Es posible que las cookies hayan expirado."
            )
            exit()
        html_content = page.evaluate("() => document.documentElement.outerHTML")
        return html_content


def get_script_element_in_json(html_content: str) -> Union[str, None]:
    """Devuelve el script_json que nos interesa y que está contenido en un elemento script de la página HTML.\n
    El script_json contiene los enlaces para descargar video o la imagen de la story

    Notas:
        Facebook devuelve un HTML al visitar un enlace de Story.
        El HTML contiene un monton de elementos script de tipo 'json' y solo uno es el que contiene el json que contiene los enlaces para descargar la story
        Para encontrar el elemento script que nos interesa toca buscar en cada elemento script un string con valor `VideoPlayerShakaPerformanceLoggerConfig`.


    Args:
        html_content: el html de la story de facebook.
    """
    root = html.fromstring(html_content)
    for node_script in root.findall(".//script[@type='application/json']"):
        # la palabra 'story_bucket_owner' aparece dos veces en el HTML de en el elemento script que nos interesa.
        if "story_bucket_owner" in node_script.text:
            data = json.loads(node_script.text)
            if data.get("require"):
                return data["require"]
    return None


def get_bucket_node(url, cookies_path) -> dict:
    """Devuelve el nodo `bucket` que contiene los nodos claves:
    - `unified_stories`: contiene nodos que tienen los enlaces de descarga de la story
    - `owner`(o `story_bucket_owner`): información del autor

    Nota:
        La estructura del data_json es horrible, toca acceder a muchos campos para encontrar el campo que nos interesa ['unified_stories']['edges']
    """
    # TODO: averiguar que tiene este nodo `viewer.stories_lwr_animations`:
    cookies = load_cookies(cookies_path)
    html_content = get_html(url, cookies)

    json_data = get_script_element_in_json(html_content)

    try:
        return json_data[0][-1][0]["__bbox"]["require"][-1][-1][-1]["__bbox"]["result"][
            "data"
        ]["extendedViewerBucket"]
    except:
        pass

    try:
        return json_data[0][-1][0]["__bbox"]["require"][-1][-1][-1]["__bbox"]["result"][
            "data"
        ]["bucket"]
    except:
        pass
    try:
        return json_data[0][-1][0]["__bbox"]["require"][5][3][1]["__bbox"]["result"][
            "data"
        ]["bucket"]
    except:
        pass
    # json_data-1.json
    try:
        return json_data[0][3][0]["__bbox"]["require"][7][3][1]["__bbox"]["result"][
            "data"
        ]["bucket"]
    except:
        pass

    raise Exception("Ninguna coincidencia.")


def run(url, cookies_path, output_dir):
    bucket_node = get_bucket_node(url, cookies_path)
    username = (
        bucket_node["owner"].get("name") or bucket_node["story_bucket_owner"]["name"]
    )

    folder = Path(output_dir).joinpath(username)
    if bucket_node["__isNode"] == "StoryHighlightContainer":
        name = bucket_node.get("name")
        if name:
            folder = folder.joinpath(name)
    folder.mkdir(parents=True, exist_ok=True)

    for edge in bucket_node["unified_stories"]["edges"]:
        media = edge["node"]["attachments"][0]["media"]

        if media["__typename"] == "Photo":
            url = media["image"]["uri"]
            download_url(url, folder)
        else:
            url = media["browser_native_hd_url"] or media["browser_native_sd_url"]
            thumbnail = media["preferred_thumbnail"]["image"]["uri"]
            path = download_url(url, folder)
            download_url(thumbnail, folder, path.stem)
