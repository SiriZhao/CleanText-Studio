<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# Estudio de texto limpio

**Limpieza de texto local, recuperación de la estructura del documento, vista previa con reconocimiento de fórmulas y exportación DOCX/TXT para texto copiado, generado por IA y con formato deficiente.**

[Inglés](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Descargar para Windows

Current version: **v1.5.0**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## ¿Qué hay de nuevo en v1.5.0?

- Catálogos de configuración regional estática completos, un cuadro de diálogo de ayuda local y validación de configuración regional atómica para la capa de presentación.
- Se mantuvieron las etiquetas del cuadro combinado separadas de los valores de limpieza estables, por lo que cambiar el idioma nunca cambia un ajuste preestablecido ni activa la limpieza.
- Panel unificado, control, enfoque, casilla de verificación y redondeo de tarjeta de resumen a través de tokens de diseño compartidos.
- Utiliza fuentes alternativas del sistema legal. En esta versión no se incluyen PingFang, HarmonyOS Sans ni ningún otro archivo de fuente.
- Se modificó la documentación principal y se agregaron verificaciones automatizadas de README, idioma de la interfaz de usuario y limpieza y congelación.

## que hace

CleanText Studio elimina los residuos de formato copiados y al mismo tiempo conserva la estructura útil del documento. Reconoce títulos, listas, citas, códigos, tablas de Markdown, enlaces y fórmulas matemáticas comunes. El mismo modelo de documento estructurado alimenta el editor de texto, la vista previa, la exportación TXT y la exportación DOCX para que una tabla o fórmula no se pierda silenciosamente durante la exportación.

### Limpieza y recuperación de estructuras.

- Limpie los encabezados de Markdown, énfasis, código en línea, enlaces, imágenes, separadores, residuos de copia HTML, emoji y caracteres decorativos.
- Detecte títulos, listas, citas, bloques de código y tablas en lugar de aplanarlos en una pared de caracteres.
- Elija unión compacta, espaciado de sección inteligente o límites de párrafo preservados.
- Mantenga las URL independientes de forma predeterminada; El manejo de URL opcional es explícito.

### Exportación de tablas y Word

Las tablas de rebajas se analizan en bloques de tablas estructurados. El modo de vista previa muestra una tabla real y la exportación DOCX escribe una tabla nativa de Word con un encabezado en negrita, bordes visibles, anchos adaptables y texto de celda limpio. El contenido extenso sigue siendo legible en lugar de convertirse en una secuencia de líneas cortas forzadas.

### Matemáticas

LaTeX común en línea y en pantalla, expresiones matemáticas Unicode y ecuaciones simples están protegidas antes de la limpieza de Markdown. Las fórmulas admitidas se exportan como ecuaciones nativas de Word OMML; las construcciones no compatibles recurren a texto legible en lugar de perder variables. La aplicación no calcula, prueba ni cambia el significado matemático.

### Optimización opcional de IA BYOK

La limpieza local funciona completamente sin conexión. La optimización de la IA es opcional y solo se ejecuta después de configurar su propio proveedor, punto final, modelo y clave API. CleanText Studio no proporciona claves públicas, proveedores de proxy ni facturas de modelos de pago. No envíe material que no sea apto para que un tercero lo procese.

<!-- section:privacy -->
## Privacidad y seguridad

La limpieza básica, la vista previa, la exportación TXT y la exportación de Word se ejecutan localmente. La aplicación no tiene publicidad, telemetría, sistema de cuentas ni clave pública de IA. Es una herramienta de formato, estructura de documentos y diseño; **no** ofrece evasión de detección de IA, evasión de plagio, suplantación de identidad, mala conducta académica o citas inventadas.

## Inicio rápido

1. Inicie la aplicación, pegue texto o abra TXT, Markdown o DOCX.
2. Seleccione un ajuste preestablecido de limpieza y un modo de párrafo.
3. Haga clic en **Limpiar** e inspeccione **Modo de texto** o **Modo de vista previa**.
4. Exporte contenido estructurado a TXT o Word.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## Requisitos de entrada, salida y sistema.

Entrada: `.txt`, `.md`, `.markdown` y `.docx`. Salida: UTF-8 `.txt` y estructurado `.docx`. v1.5.0 es una versión de escritorio de Windows x64. macOS, Linux y Android no se consideran plataformas lanzadas.

## De la fuente

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## Probar y construir

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/check_ui_language_consistency.py
.\.venv\Scripts\python scripts/check_readme_quality.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
.\scripts\build_windows.ps1
```

La compilación de Windows produce una aplicación onedir, un ZIP portátil, un instalador de Inno Setup, sumas de comprobación SHA256 y notas de la versión en `dist/`.

## Localización, contribuciones y limitaciones.

La interfaz proporciona chino simplificado, chino tradicional, inglés, japonés, coreano, español, francés, alemán, portugués brasileño, ruso, árabe (RTL) e hindi. La revisión de la traducción es bienvenida; consulte [la guía de traducción] (docs/TRANSLATION_GUIDE.md). Las macros LaTeX personalizadas complejas pueden utilizar un texto alternativo, y la importación DOCX no conserva todos los estilos del documento fuente ni las imágenes incrustadas.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## Licencia

Licencia MIT. Consulte [LICENCIA](LICENCIA) y [TERCER_PARTY_LICENSES.md](TERCERO_PARTY_LICENSES.md).

> Translation review from the community is welcome.
