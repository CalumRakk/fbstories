
import json
from typing import Union

from lxml import html
from playwright.sync_api import sync_playwright


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
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        page = context.new_page()
        context.add_cookies(cookies)

        page.goto(url)

        html_content = page.evaluate(
            "() => document.documentElement.outerHTML")
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
        if "VideoPlayerShakaPerformanceLoggerConfig" in node_script.text:
            data = json.loads(node_script.text)
            if data.get("require"):
                return data["require"]
    return None


def get_node_bucket(data_json: dict) -> dict:
    """Devuelve el nodo `bucket` que contiene los nodos claves:
    - `unified_stories`: contiene nodos que tienen los enlaces de descarga de la story
    - `owner`(o `story_bucket_owner`): información del autor

    Nota:
        La estructura del data_json es horrible, toca acceder a muchos campos para encontrar el campo que nos interesa ['unified_stories']['edges']
    """
    # TODO: averiguar que tiene este nodo `viewer.stories_lwr_animations`:
    # with open("data.json","w") as file:
    #     json.dump(data_json, file)
    return data_json[0][-1][0]["__bbox"]["require"][7][3][1]["__bbox"]["result"]["data"]["bucket"]


def get_metadata(bucket_node: dict) -> dict:
    """Devuelve un dict que tiene un campo `urls` que contiene una lista de urls para descargar los medios y
    otro campo `author` que contiene un diccionario con los metadatos del author de la story.
    """
    URLS = []
    for node in bucket_node["unified_stories"]["edges"]:
        media = node["node"]["attachments"][0]["media"]
        if media["__typename"] == "Photo":
            URLS.append(media["image"]["uri"])
            continue
        URLS.append(media["playable_url_quality_hd"])

    author = bucket_node["owner"]
    return {"urls": URLS, "author": author}


def run(url, cookies):
    html_content = get_html(url, cookies)
    json_data = get_script_element_in_json(html_content)
    if json_data is None:
        print("Cookies caducadas o parece que la historia ya no está disponible")
        exit()
    bucket_node = get_node_bucket(json_data)
    return get_metadata(bucket_node)
