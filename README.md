
Script para descargar Facebook stories 

# Instación
El primer comando instalará la última version de este repositorio.

El segundo instalará los navegadores playwright que se requieren para que este proyecto funcione.

```python
pip install git+https://github.com/CalumRakk/fbstories
python -m playwright install
```
# Cookies de Facebook
Este proyecto requiere de cookies de facebook porque las URL de las stories son urls protegidas y requieren de autenticación para poder acceder.

Para conseguir las cookies de facebook se puede usar cualquier herramiente de su preferencia. Sin embargo, en este proyecto he usado la extension [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) 

Una vez instala vaya a facebook.com y haga los siguiente pasos:

- Dale clic al icono de la extension
- clic en el boton de exportar para copiar las cookies
- guardar las cookies en un archivo llamado `cookies.json`

# Uso de línea de comandos
Como un ejemplo se uso 

El siguiente comando descargara la siguiente story de Facebook
```shell
fbstories https://web.facebook.com/stories/1356992473975435
```
Si el archivo `cookies.json` no está en la raiz del proyecto, debe especificar la ubicacion pasando el argumento `--cookies` asi:
```shell
fbstories https://web.facebook.com/stories/1460595473991895 --cookies "C:\Users\UserName\Downloads\cookies.json"
```

# Usando Python
```python
import os
from fbstories import run
from fbstories.utils import load_cookies, http_download

url = "https://web.facebook.com/stories/1356992473975435"
output_dir = "."
cookies_path = "cookies.json"

os.makedirs(output_dir, exist_ok=True)
cookies = load_cookies(cookies_path)

metadata = run(url, cookies=cookies)
for url in metadata["urls"]:
    http_download(url, output_dir)
```






