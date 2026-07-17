# Third-party notices

CleanText Studio does not bundle Apple PingFang, HarmonyOS Sans, Noto, or any
other font file in v1.4.2.  The application selects installed system fonts and
falls back safely when a preferred family is unavailable.  In particular, no
Apple proprietary font is copied into this repository or Windows package.

| Component | Purpose | License / source | Distributed with this repository |
| --- | --- | --- | --- |
| PySide6 / Qt | Desktop interface | LGPLv3/GPLv3/commercial; https://doc.qt.io/qtforpython/ | Python dependency only |
| python-docx | DOCX generation | MIT; https://github.com/python-openxml/python-docx | Python dependency |
| KaTeX-compatible local preview assets | Formula preview implementation where present | MIT; project dependency notices apply | No remote CDN resource is loaded |

The project itself is distributed under the [MIT License](LICENSE).
