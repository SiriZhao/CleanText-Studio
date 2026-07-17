<p align="center">
  <img src="assets/icon.png" width="96" alt="CleanText Studio logo">
</p>

<h1 align="center">CleanText Studio</h1>

<p align="center"><strong>Limpieza de texto local primero, recuperación de estructura de documentos, vista previa con reconocimiento de fórmulas y exportación DOCX/TXT pulida para texto copiado y generado por IA.</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.hi.md">हिन्दी</a>
</p>

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.2"><img src="https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver" alt="Latest release"></a>
  <a href="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml"><img src="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Windows-x64-0078D4" alt="Windows x64">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="MIT License"></a>
</p>

> **Versión actual: v1.5.2 · Windows x64 · primero local de forma predeterminada**

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Setup.exe"><strong>Descargar instalador</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Portable.zip"><strong>Descargar ZIP portátil</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/SHA256SUMS.txt">SHA256 sumas de comprobación</a>
</p>

![CleanText Studio interfaz en inglés](assets/screenshots/v1.5.2/01-main-light.png)

CleanText Studio convierte el texto copiado desordenado en un documento legible y editable sin tratar la estructura útil como ruido. Elimina Markdown y decoración redundantes, recupera encabezados, listas, tablas y notación matemática común, luego le brinda una vista de texto, una vista previa estructurada y exportación DOCX o TXT. La limpieza básica se realiza en el dispositivo; La optimización de IA opcional utiliza solo un proveedor API que usted mismo configura.

**Por qué es útil**

- Mantenga el significado mientras elimina residuos visuales de páginas web, chats, notas y borradores generados.
- Conserve un modelo de documento para que los encabezados, tablas, enlaces y fórmulas no se acoplen silenciosamente antes de la exportación.
- Revise el resultado antes de escribir una tabla nativa Word, una ecuación editable o un archivo de texto UTF-8.
- Cambie el idioma y el tema de la interfaz en tiempo de ejecución sin cambiar la fuente, el resultado o la configuración de limpieza.

## Descargar para Windows

CleanText Studio v1.5.2 se lanzó para **Windows x64**. Elija el instalador para una instalación normal por usuario, o elija el ZIP portátil cuando prefiera ejecutar desde una carpeta extraída. Ninguno de los paquetes requiere una instalación Python por separado.

| Paquete | Uso previsto | Descargar |
| --- | --- | --- |
| Configuración | Soporte para instalación, entrada en el menú Inicio y desinstalación | [CleanText-Studio-v1.5.2-Windows-x64-Setup.exe](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Setup.exe) |
| Portátil | Ejecutar después de extraer el ZIP; sin instalación | [CleanText-Studio-v1.5.2-Windows-x64-Portable.zip](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Portable.zip) |
| Verificación | Verifique el paquete descargado | [SHA256SUMS.txt](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/SHA256SUMS.txt) |

La página de publicación es la fuente veraz de los archivos disponibles: [CleanText Studio v1.5.2](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.2).

## ¿Qué hace CleanText Studio?

### Creado para una limpieza práctica de documentos

El contenido copiado a menudo llega con títulos escritos como marcadores, separadores repetidos, emoji decorativos, líneas discontinuas, etiquetas de tutoriales, enlaces pegados o tablas que solo son visualmente tabulares. CleanText Studio hace explícitas esas elecciones en lugar de aplicar una reescritura oculta y única. Elija un ajuste preestablecido, inspeccione el resultado y exporte solo después de que la estructura se vea bien.

### Escenarios típicos- Normalizar notas de investigación, notas de reuniones, extractos de bases de conocimientos y copias de páginas web.
- Prepare borradores asistidos por IA para su edición y entrega profesional de documentos.
- Recuperar una tabla Markdown antes de enviarla como tabla Word nativa.
- Preservar matemáticas simples en línea y en bloque mientras se elimina el ruido de formato circundante.
- Cree una transferencia TXT limpia cuando un diseño Word no sea necesario.

## Capacidades principales

### Markdown y limpieza de formato

El proceso de limpieza puede eliminar Markdown marcadores de encabezado, marcadores de énfasis, marcadores de código en línea, sintaxis de imágenes, reglas horizontales, residuos de HTML copiados, símbolos decorativos, emoji y etiquetas instructivas fragmentadas. Conserva el texto normal y hace que las opciones de limpieza sean visibles en el panel de configuración.

### Recuperación de la estructura del documento

Los encabezados, listas, citas, bloques de código, párrafos, tablas, enlaces y bloques matemáticos se representan como estructura de documento en lugar de colapsarse ciegamente en un flujo de caracteres. Es por eso que la vista previa y la exportación pueden tomar las mismas decisiones estructurales.

### Encabezados y listas

Elija si desea conservar los marcadores, naturalizar una estructura o eliminar marcadores cuando corresponda. La herramienta está diseñada para conservar una jerarquía útil y una semántica de listas; no es un reescritor genérico el que inventa un nuevo esquema.

### Párrafos y saltos de línea

Tres modos cubren material fuente común:

| Modo | Úselo cuando |
| --- | --- |
| Compacto | Desea que las líneas fuente envueltas ordinarias se unan en párrafos compactos. |
| Secciones inteligentes | Desea un espaciado de párrafo natural y al mismo tiempo conservar saltos de sección significativos. |
| Preservar todo | Necesita que los límites del párrafo fuente se mantengan lo más ajustados posible. |

### Enlaces y URL independientes

El manejo de enlaces puede mantener Markdown, mantener solo el texto para mostrar o conservar el texto para mostrar junto con su URL. Las URL independientes se pueden conservar, fusionar con el párrafo anterior o eliminar cuando son solo residuos del tutorial. Las URL se manejan deliberadamente en lugar de desaparecer como efecto secundario de la limpieza de Markdown.

## Tablas, ecuaciones y vista previa

### tablas Markdown y tablas Word

Las tablas Markdown se analizan en bloques de tablas estructuradas. El modo de vista previa muestra la tabla como una tabla y la exportación DOCX crea una tabla Word nativa con una fila de encabezado, contenido de celda legible, bordes y anchos elegidos del contenido en lugar de una división igual fija. Markdown las filas de separación, los marcadores de énfasis residuales, las columnas vacías sin sentido y los saltos de línea suaves accidentales se limpian antes de la exportación cuando la configuración de limpieza activa lo permite.

![Vista previa de la tabla estructurada](assets/screenshots/v1.5.2/05-table-export.png)

### Fórmulas matemáticas y ecuaciones Word editables

Los delimitadores comunes en línea y en pantalla LaTeX, las expresiones matemáticas Unicode y las ecuaciones simples están protegidos mientras se limpia el texto circundante. Las fórmulas admitidas se emiten como Word OMML ecuaciones nativas, por lo que las variables y expresiones comunes siguen siendo editables en Word. El espaciado de fórmulas, los problemas obvios con los delimitadores y la numeración de fórmulas se pueden normalizar según las opciones seleccionadas.

Las macros personalizadas complejas no se descartan silenciosamente. Cuando una fórmula está fuera del rango de conversión admitido, la aplicación mantiene un respaldo legible y lo informa en la información de calidad de exportación.

![Vista previa con reconocimiento de fórmulas](assets/screenshots/v1.5.2/06-word-export.png)

### Modo texto y modo vista previa

El modo texto es útil para revisar el resultado normalizado. El modo de vista previa muestra títulos, listas, tablas, enlaces y fórmulas en un formato orientado a documentos. Cambiar el modo de visualización no vuelve a ejecutar la limpieza ni cambia el resultado.

## Antes y despuésEl siguiente ejemplo compacto muestra el tipo de residuo para el cual la aplicación está diseñada para limpiar y al mismo tiempo preservar el contenido útil.

**Fuente**```markdown
### **Project notes** ✨
---
Read the **draft** first.

- Keep the main conclusion
- Remove decorative labels

| Item | Value |
| --- | --- |
| Formula | \( E = mc^2 \) |

https://example.com/reference
```**Concepto de resultado**```text
Project notes

Read the draft first.

• Keep the main conclusion
• Remove decorative labels

The table and E = mc² formula remain structured in Preview and DOCX export.
`

![Fuente y resultado limpio](assets/screenshots/v1.5.2/03-before-after-light.png)

## Formatos de exportación

### Exportar Word

Elija exportar Word cuando el destino necesite encabezados, listas, tablas y fórmulas admitidas como elementos de documento editables. El exportador produce un archivo `.docx`; no automatiza una aplicación Word instalada localmente. Antes de exportar, la aplicación puede mostrar una estructura y un resumen de calidad para que las limitaciones de fórmulas/tablas recuperables sean visibles.

### Exportar TXT

Elija TXT para obtener un resultado portátil de texto sin formato UTF-8. La exportación TXT conserva el contenido textual normalizado, pero no puede representar tablas nativas Word ni ecuaciones OMML editables como objetos de documento enriquecido.

| Entrada | Salida |
| --- | --- |
| TXT, Markdown, MD, DOCX | UTF-8 TXT y estructurado DOCX |

## Idiomas, temas y accesibilidad

La interfaz de escritorio ofrece chino simplificado, chino tradicional, inglés, japonés, coreano, español, francés, alemán, portugués brasileño, ruso, árabe e hindi. Los cambios de idioma se aplican en tiempo de ejecución y conservan el texto, los resultados, las selecciones actuales y el historial de deshacer. El árabe utiliza una interfaz de derecha a izquierda, mientras que los valores técnicos como las URL, las claves API y el código siguen siendo legibles de izquierda a derecha.

Los temas claros y oscuros comparten el mismo panel, control, enfoque y sistema de superficie redondeada. La aplicación utiliza fuentes alternativas del sistema legal cuando estén disponibles; **no** incluye archivos Apple PingFang.

![Tema oscuro y superficies redondeadas](assets/screenshots/v1.5.2/07-settings.png)

## Optimización de IA opcional (BYOK)

La optimización de la IA es opcional. La limpieza básica, la vista previa, la exportación TXT y la exportación DOCX están disponibles sin conexión de red. Cuando habilita deliberadamente la optimización de IA, elige un proveedor, punto final, modelo compatible y su propia clave API. La aplicación no proporciona una clave API compartida gratuita ni un proxy de su cuenta de proveedor.

DeepSeek y otros proveedores expuestos por la configuración de la aplicación instalada se pueden seleccionar a través del cuadro de diálogo de configuración de AI. Los identificadores de proveedor y modelo permanecen separados de las etiquetas de visualización traducidas. Revise los términos de datos del propio proveedor antes de enviar material confidencial.

![Configuración de IA](assets/screenshots/v1.5.2/07-settings.png)

## Inicio rápido

1. Inicie CleanText Studio y pegue el texto, o abra un archivo compatible.
2. Elija un ajuste preestablecido de limpieza y ajuste solo las opciones necesarias para este documento.
3. Haga clic en **Limpiar** y luego inspeccione el modo Texto o el modo Vista previa.
4. Exporte a Word para una entrega estructurada o a TXT para un archivo de texto sin formato normalizado.
5. Si es necesario, configure su propio proveedor de IA y elija conscientemente cuándo enviarle mensajes de texto.

### Instalador o versión portátil

- **Instalador:** ejecute el ejecutable de instalación, siga el instalador e inicie CleanText Studio desde el menú Inicio. Utilice la configuración de aplicaciones Windows o el desinstalador para eliminarlo.
- **Portátil:** extrae el ZIP a una carpeta grabable e inicia el ejecutable dentro de ella. Mantenga los archivos extraídos juntos; no lo ejecute directamente desde un archivo comprimido.

### Flujo de trabajo completo

1. Coloque el texto fuente en el panel izquierdo.
2. Utilice el panel central para decidir cómo se manejan Markdown, enlaces, párrafos, listas y fórmulas.
3. Revise el resultado limpio a la derecha y use Vista previa para tablas y ecuaciones.
4. Utilice la barra de herramientas de resultados para copiar, deshacer, restaurar el resultado más reciente, borrar, exportar TXT o exportar Word.
5. Conservar una copia de la fuente original siempre que el documento tenga importancia legal, de archivo o de publicación.

## Privacidad, seguridad y flujo de datos

### Procesamiento básico local primeroLa limpieza básica se ejecuta localmente. La aplicación no tiene sistema de cuentas, servicio de publicidad, servicio de telemetría ni clave pública compartida API. Su texto no se carga simplemente porque se pega, se obtiene una vista previa, se limpia o se exporta localmente.

### Las solicitudes de IA son voluntarias

Solo una acción explícita de optimización de IA utiliza el proveedor externo que usted configura. El proveedor recibe el material necesario para esa solicitud bajo sus propios términos. No utilice una solicitud de proveedor para material que no tiene derecho a compartir.

### API manejo de claves

Las claves API las proporciona el usuario y no se escriben en la configuración del documento exportado. En Windows, la aplicación utiliza su mecanismo de almacenamiento de credenciales configurado cuando está disponible; Si el almacenamiento seguro de credenciales no está disponible, recurre de forma segura en lugar de exportar silenciosamente una clave de texto sin formato. Trate la cuenta de su sistema operativo y las credenciales de su proveedor como límites de seguridad.

## Requisitos del sistema

- Windows x64.
- Un entorno de escritorio Windows compatible actualmente.
- No hay tiempo de ejecución Python instalado por separado para los paquetes de lanzamiento.
- El acceso a Internet es opcional y solo es necesario para descargas de GitHub, uso opcional de IA o enlaces abiertos por el usuario.

Windows SmartScreen puede mostrar una advertencia de reputación para una nueva compilación sin firmar o de baja reputación. Descargue únicamente desde la página de lanzamiento del repositorio, verifique la suma de verificación SHA256 y siga la política de instalación de software de su organización.

## Pila técnica y arquitectura del proyecto.

CleanText Studio es una aplicación de escritorio Python que utiliza PySide6 para la interfaz, python-docx para escritura DOCX, PyInstaller para empaquetado portátil, Inno Setup para el instalador Windows y pytest/Ruff/mypy para controles de calidad. El modelo de limpieza y bloque de documentos se encuentra debajo de la capa de presentación, lo que permite que el texto, la vista previa y la exportación consuman la misma estructura normalizada.```text
src/cleantext_studio/
├── app.py                 # desktop window and presentation wiring
├── cleaners/              # stable text-cleaning pipeline
├── math/                  # detection, parsing, preview, and OMML support
├── exporters/             # DOCX and TXT exporters
├── i18n/                  # locale catalogs and runtime translation service
├── ui/                    # cards, controls, and theme components
└── llm/                   # optional provider configuration and requests
assets/                    # icon, screenshots, and packaged resources
scripts/                   # validation, screenshot, and Windows-build helpers
tests/                     # unit, GUI, integration, and regression checks
```## Ejecutar desde la fuente

Los siguientes comandos coinciden con el diseño de desarrollo del repositorio en PowerShell.```powershell
git clone https://github.com/SiriZhao/CleanText-Studio.git
cd CleanText-Studio
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```## Probar y construir```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/check_readme_quality.py
.\.venv\Scripts\python scripts/check_screenshot_quality.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
.\scripts\build_windows.ps1
```La compilación Windows escribe sus artefactos, sumas de verificación y notas de versión actuales en `dist/`. El resultado de la compilación no se envía intencionalmente al repositorio.

## Liberación de artefactos y verificación SHA256

Cada versión proporciona el ejecutable de configuración, ZIP portátil, `SHA256SUMS.txt` y notas de la versión cuando estén disponibles. En PowerShell, compare un artefacto descargado con la suma de comprobación publicada:```powershell
Get-FileHash .\CleanText-Studio-v1.5.2-Windows-x64-Setup.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```## Internacionalización y aportaciones de traducción

Los catálogos locales oficiales son `zh_CN`, `zh_TW`, `en_US`, `ja_JP`, `ko_KR`, `es_ES`, `fr_FR`, `de_DE`, `pt_BR`, `ru_RU`, `ar` y `hi_IN`. Consulte [docs/TRANSLATION_GLOSSARY.md](docs/TRANSLATION_GLOSSARY.md) y [docs/README_TRANSLATION_STATUS.md](docs/README_TRANSLATION_STATUS.md) antes de proponer cambios de terminología. La revisión de la traducción de la comunidad es bienvenida; Este repositorio no afirma que cada traducción de documentación haya sido revisada por un hablante nativo.

## Hoja de ruta

La versión pública actual es Windows x64. El trabajo futuro de la plataforma, una mayor fidelidad de las importaciones y una cobertura más amplia de la fórmula son temas de la hoja de ruta más que las reclamaciones de envío actuales. Las solicitudes de funciones y los informes de problemas son bienvenidos, pero un elemento de la hoja de ruta no es un compromiso ni un anuncio de lanzamiento.

## Limitaciones conocidas

- Las macros LaTeX personalizadas complejas pueden requerir un respaldo legible en lugar de la conversión de ecuaciones nativas Word.
- La importación DOCX no puede conservar todos los estilos, objetos incrustados o características de diseño originales de archivos Word arbitrarios.
- TXT no puede codificar tablas nativas Word ricas ni ecuaciones editables.
- La salida de IA opcional la produce el proveedor externo que usted seleccione y requiere revisión humana.
- Windows packaging es la única plataforma publicada indicada aquí; macOS, Linux, Android e iOS no se anuncian actualmente como versiones publicadas.

## Preguntas frecuentes

### ¿Debo estar en línea?

No. La limpieza local, la vista previa y la exportación local funcionan sin una conexión de red. El acceso a la red solo es necesario para acciones como descargar versiones, abrir un enlace externo o una solicitud de IA que usted elija realizar.

### ¿La aplicación cargará mi texto?

No para procesamiento local básico. Una solicitud de terceros ocurre solo cuando utiliza explícitamente la optimización de IA con su propio proveedor configurado.

### ¿Debo configurar una clave API?

No. Se necesita una clave API solo para la optimización de IA opcional.

### ¿Qué archivos puedo usar?

La aplicación acepta entradas TXT, Markdown/MD y DOCX y puede exportar UTF-8 TXT o DOCX estructurado.

### ¿Cuál es la diferencia entre la exportación Word y TXT?

Word puede conservar una estructura rica, como encabezados, tablas nativas y ecuaciones editables compatibles. TXT es una transferencia de texto UTF-8 limpia sin objetos de documento enriquecidos.

### ¿Por qué se recomienda la exportación Word para algunos documentos?

Es el formato que puede transmitir con mayor fidelidad la estructura del documento recuperado, especialmente las tablas y fórmulas admitidas.

### ¿Las fórmulas son editables?

Las fórmulas admitidas se exportan como Word OMML ecuaciones nativas. Las macros complejas no compatibles pueden utilizar un respaldo legible y deben verificarse antes de publicarlas.

### ¿Las tablas se exportan como tablas Word?

Las tablas Markdown estructuradas se exportan como tablas Word nativas cuando se selecciona la exportación Word.

### ¿Cómo cambio el idioma o el tema?

Utilice los controles de idioma y tema en la barra de herramientas/configuración de la aplicación. El modificador de tiempo de ejecución conserva el documento activo y las selecciones de limpieza.

### ¿Dónde se almacena mi clave API?

La aplicación utiliza su ruta de almacenamiento de credenciales Windows configurada cuando está disponible y no incluye la clave en la configuración exportada. Revise la configuración de la compilación instalada y la política de seguridad de su sistema.

### ¿Instalador o ZIP portátil?

Elija el instalador para la integración normal de Windows y soporte de desinstalación. Elija portátil cuando desee una carpeta extraída e independiente.

### ¿Cómo informo un problema o contribuyo con una traducción?Abra una incidencia o solicitud de extracción en [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio), incluida una muestra no confidencial y el resultado esperado cuando sea posible.

## Contribuyendo

Lea [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir una solicitud de extracción. Mantenga los cambios enfocados, agregue pruebas cuando cambie el comportamiento, evite comprometer los resultados de la compilación o las credenciales y preserve la postura de privacidad local del proyecto.

## Desarrollador

Mantenido por [SiriZhao](https://github.com/SiriZhao). Inicio del proyecto: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio).

## Licencias de terceros

Consulte [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) para obtener avisos de dependencia distribuidos y de tiempo de ejecución. CleanText Studio no empaqueta archivos de fuentes Apple PingFang.

## Licencia

CleanText Studio está disponible bajo la [MIT License](LICENCIA).

> Agradecemos la revisión comunitaria de la traducción de este README.
