Script para descargar Facebook stories

Instalación
------------

Para comenzar, sigue los siguientes pasos de instalación:

1. instala la última version de este proyecto:

```shell
pip install git+https://github.com/CalumRakk/fbstories
```

2. Instala los navegadores requeridos de Playwright ejecutando el siguiente comando:

```shell
python -m playwright install
```

Obtener las Cookies de Facebook
------------
Este proyecto requiere el uso de cookies, ya que las URLs de las historias de Facebook están protegidas y requieren autenticación para acceder a ellas.

Puedes usar la extensión de Chrome llamada [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) para obtener las cookies de manera sencilla. Una vez que hayas instalado la extensión, sigue estos pasos:

1. Dirígete a facebook.com.
2. Haz clic en el icono de la extensión en la barra del navegador.
3. Selecciona la opción de exportar para copiar las cookies.
4. Guarda las cookies en un archivo llamado cookies.json.

Cómo descargar una historia usando la línea de comandos
------------
Puedes usar el siguiente comando para descargar todos los medios de una historia de Facebook:

```shell
fbstories https://web.facebook.com/stories/1356992473975435
```

Asegúrate de que el archivo cookies.json se encuentra en la misma ubicación desde donde ejecutas el comando.

Si el archivo cookies.json no se encuentra en la raíz del proyecto, debes especificar la ubicación utilizando el argumento --cookies de la siguiente manera:

```shell
fbstories https://web.facebook.com/stories/1460595473991895 --cookies "C:\Users\UserName\Downloads\cookies.json"
```

# Python modulo fbstories 
Si prefieres usar el script desde Python, aquí tienes un ejemplo de cómo hacerlo:

```python
from fbstories import run

url = "https://web.facebook.com/stories/1356992473975435"
cookies_path = "cookies.json"
output_dir = "Gallery"

run(url=url, cookies_path=cookies_path, output_dir=output_dir)

```







