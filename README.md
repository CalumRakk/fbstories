
Script para descargar Facebook stories 

# Instación
El siguiente comando instalará la última version de este repositorio:

```python
pip install git+https://github.com/CalumRakk/fbstories
python -m playwright install
```
# Cookies de Facebook
Este paquete requiere de cookies de facebook porque las URL de las stories son urls protegidas y requieren de autenticación para poder acceder.

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
fbstories https://web.facebook.com/stories/1460595473991895 --cookies "C:\Users\Leo\Downloads\cookies.json"
```








