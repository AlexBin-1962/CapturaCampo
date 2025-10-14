## Resumen rápido

Este repositorio es una single-page app estática (un solo archivo principal: `captura_campo.html`) que sirve como una "App de campo" MVP para capturar puntos georreferenciados y sincronizarlos con GitHub. La mayor parte de la lógica está en JavaScript embebido en `captura_campo.html`.

## Qué debe saber un agente AI para ser productivo

- Arquitectura: no hay backend; es una app estática que usa LocalStorage para datos locales (`STORAGE_KEY = 'ct27_campo_registros_v1'`) y puede sincronizar subiendo un GeoJSON al repo destino vía GitHub Contents API (`ghPutFile`).
- Flujo de datos clave: formulario → marker temporal (`punteroTemporal`) → array de registros en LocalStorage → exportación a GeoJSON/CSV o push a GitHub.
- Ficheros y rutas de interés: `captura_campo.html`, `data/geo/secciones.geojson` (por defecto `DEFAULT_URL_SECCIONES = '/data/geo/secciones.geojson'`), objetivo de sync por defecto `data/ct27_registros.geojson`.
- Dependencias externas que afectan comportamiento en tiempo de ejecución:
  - Leaflet (mapa/markers)
  - Turf.js (point-in-polygon para autocompletar ámbitos)
  - Nominatim (OpenStreetMap) para geocoding/search

## Comandos útiles para desarrollo local

La app es estática; usa un servidor estático para evitar problemas CORS/recursos relativos. En PowerShell (Windows) una opción mínima:

```powershell
# desde la raíz del repo
python -m http.server 8000
# o, si tiene Node: npx serve -p 8000
```

Luego abrir `http://localhost:8000/captura_campo.html`.

## Configuración y secretos

- La configuración de runtime está en LocalStorage (`CONFIG_KEY = 'ct27_campo_config_v1'`).
- El token de GitHub se ingresa en el formulario (`#cfg_gh_token`) y NO se persiste en el servidor — se transmite sólo en la petición al hacer sync. Necesita permisos Contents: Read & Write en el repo destino (preferible fine-grained token).

## Puntos de integración y APIs

- GitHub Contents API: funciones `ghGetFile` y `ghPutFile` dentro de `captura_campo.html`.
- Nominatim: llamadas fetch a `https://nominatim.openstreetmap.org/search?...` para geocoding y búsqueda.
- Turf booleanPointInPolygon usado en `autocompletarAmbitoDesdeSecciones(latlng)` para rellenar MUNICIPIO/DF/DL/SECCIÓN.

## Convenciones del proyecto

- Categorías definidas en `CATEGORIAS` (array JS). Los markers usan `color` de cada categoría.
- Guardado local: todos los registros se serializan en LocalStorage como una lista de objetos con campos: id, nombre, tel, domicilio, categoria, color, ambito, ambito_clave, mun, df, dl, seccion, notas, lat, lng, created_at.

## Errores y "gotchas" detectados (importante para un agente)

- El archivo contiene bloques de código duplicados y errores de sintaxis (probablemente edición parcial):
  - `getCurrentGeoJSON()` aparece con cierre desordenado y duplicado; hay `});` sobrantes.
  - `guardarConfig()` usa `replace(/\/g,'/')` intencional pero la expresión actual es `replace(/\/g,'/')` mal escapada en el archivo; revisar la línea y validar la normalización de rutas.
  - Hay funciones / fragmentos repetidos como `autocompletarAmbitoDesdeSecciones` y bloques que terminan con `}).addTo(map);` fuera de contexto. Esto provoca errores si se abre el HTML directamente.
  - Fragmentos duplicados alrededor de `renderTabla()` y exportación GeoJSON/CSV.

  Recomendación: antes de modificar funcionalidad, arreglar las duplicaciones y ejecutar la página en un servidor local para localizar errores de consola.

## Tareas que un agente puede ejecutar con claridad

1. Limpiar/normalizar `captura_campo.html`: eliminar funciones duplicadas, arreglar cierres de paréntesis y regex en `guardarConfig`.
2. Separar el JS en un archivo `app.js` y simplificar HTML (opcional, mejora mantenibilidad).
3. Añadir una pequeña suite de pruebas manuales / checklist en README: pruebas de geocodificación, autocompletado de secciones y sincronización con GitHub usando un token de prueba.

## Ejemplos concretos en el código

- Autocompletado por polígono: `autocompletarAmbitoDesdeSecciones(latlng)` usa `turf.booleanPointInPolygon(pt, f)` y rellena `#auto_mun`, `#auto_df`, `#auto_dl`, `#auto_sec`.
- Sync GitHub: `ghPutFile({owner, repo, path, branch, token, content, message})` — construye body con base64 UTF-8 del contenido.

Si algún fragmento no queda claro o desea que incluya correcciones automáticas (p. ej., refactorizar JS externo y arreglar errores detectados), dime y lo hago en la siguiente iteración.
