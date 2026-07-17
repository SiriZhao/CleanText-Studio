"""Structured, locale-aware presentation data for the About dialog."""

from __future__ import annotations

from dataclasses import dataclass

from cleantext_studio import __version__
from cleantext_studio.i18n import I18nService

PRODUCT_NAME = "CleanText Studio"
DEVELOPER = "SiriZhao"
HOMEPAGE_URL = "https://github.com/SiriZhao/CleanText-Studio"
LICENSE_NAME = "MIT License"
COPYRIGHT = "Copyright © 2026 SiriZhao. All rights reserved."


@dataclass(frozen=True, slots=True)
class AboutViewModel:
    """Facts stay immutable while explanations follow the active locale."""

    product_name: str
    localized_product_subtitle: str
    version: str
    developer: str
    homepage_url: str
    license_name: str
    copyright_text: str
    description: str
    local_processing: str
    ai_processing: str
    privacy: str
    disclaimer: str

    @classmethod
    def from_service(cls, service: I18nService) -> AboutViewModel:
        copy = _ABOUT_COPY.get(service.active, _ABOUT_COPY["en_US"])
        return cls(
            product_name=PRODUCT_NAME,
            localized_product_subtitle=copy["subtitle"],
            version=f"v{__version__}",
            developer=DEVELOPER,
            homepage_url=HOMEPAGE_URL,
            license_name=LICENSE_NAME,
            copyright_text=COPYRIGHT,
            description=copy["description"],
            local_processing=copy["local"],
            ai_processing=copy["ai"],
            privacy=copy["privacy"],
            disclaimer=copy["disclaimer"],
        )


_ABOUT_COPY: dict[str, dict[str, str]] = {
    "en_US": {"subtitle": PRODUCT_NAME, "description": "A local-first text cleanup, document-structure, and Word/TXT formatting tool.", "local": "Basic cleanup is performed locally.", "ai": "AI optimization only calls a third-party API configured by the user.", "privacy": "The application does not provide a shared API key.", "disclaimer": "Third-party providers process data under their own terms."},
    "zh_CN": {"subtitle": "净文排版 · CleanText Studio", "description": "一款本地优先的文本清理、文档结构整理与 Word/TXT 格式化工具。", "local": "基础清理在本机完成。", "ai": "只有在用户主动使用 AI 优化时，应用才会调用用户自行配置的第三方 API。", "privacy": "应用不提供共享 API Key。", "disclaimer": "第三方服务的数据处理受其各自条款约束。"},
    "zh_TW": {"subtitle": "淨文排版 · CleanText Studio", "description": "一款本機優先的文字清理、文件結構整理與 Word/TXT 格式化工具。", "local": "基礎清理在本機完成。", "ai": "只有在使用者主動使用 AI 最佳化時，應用程式才會呼叫使用者自行設定的第三方 API。", "privacy": "應用程式不提供共用 API Key。", "disclaimer": "第三方服務的資料處理受其各自條款約束。"},
    "ja_JP": {"subtitle": PRODUCT_NAME, "description": "ローカル優先のテキスト整形、文書構造整理、Word/TXT 書式化ツールです。", "local": "基本的なクリーニングはローカルで実行されます。", "ai": "AI 最適化は、利用者が設定した第三者 API を使用する場合にのみ呼び出されます。", "privacy": "アプリケーションは共有 API Key を提供しません。", "disclaimer": "第三者サービスによるデータ処理には、それぞれの規約が適用されます。"},
    "ko_KR": {"subtitle": PRODUCT_NAME, "description": "로컬 우선 텍스트 정리, 문서 구조 정리 및 Word/TXT 서식 도구입니다.", "local": "기본 정리는 로컬에서 수행됩니다.", "ai": "AI 최적화는 사용자가 구성한 타사 API를 사용할 때만 호출됩니다.", "privacy": "애플리케이션은 공유 API Key를 제공하지 않습니다.", "disclaimer": "타사 서비스의 데이터 처리는 해당 서비스의 약관을 따릅니다."},
    "es_ES": {"subtitle": PRODUCT_NAME, "description": "Una herramienta local para limpiar texto, recuperar estructura documental y dar formato a Word/TXT.", "local": "La limpieza básica se realiza localmente.", "ai": "La optimización con IA solo llama a una API de terceros configurada por la persona usuaria.", "privacy": "La aplicación no proporciona una API Key compartida.", "disclaimer": "El procesamiento de datos de terceros está sujeto a sus propios términos."},
    "fr_FR": {"subtitle": PRODUCT_NAME, "description": "Un outil local de nettoyage de texte, de structuration de documents et de mise en forme Word/TXT.", "local": "Le nettoyage de base est effectué localement.", "ai": "L’optimisation par IA appelle uniquement une API tierce configurée par l’utilisateur.", "privacy": "L’application ne fournit pas de API Key partagée.", "disclaimer": "Le traitement des données par des tiers est régi par leurs propres conditions."},
    "de_DE": {"subtitle": PRODUCT_NAME, "description": "Ein lokales Werkzeug für Textbereinigung, Dokumentstruktur und Word/TXT-Formatierung.", "local": "Die grundlegende Bereinigung erfolgt lokal.", "ai": "Die KI-Optimierung ruft nur eine vom Benutzer konfigurierte Drittanbieter-API auf.", "privacy": "Die Anwendung stellt keinen gemeinsamen API Key bereit.", "disclaimer": "Für die Datenverarbeitung durch Drittanbieter gelten deren eigene Bedingungen."},
    "pt_BR": {"subtitle": PRODUCT_NAME, "description": "Uma ferramenta local para limpeza de texto, estruturação de documentos e formatação Word/TXT.", "local": "A limpeza básica é realizada localmente.", "ai": "A otimização por IA chama apenas uma API de terceiros configurada pela pessoa usuária.", "privacy": "O aplicativo não fornece uma API Key compartilhada.", "disclaimer": "O processamento de dados por terceiros está sujeito aos próprios termos."},
    "ru_RU": {"subtitle": PRODUCT_NAME, "description": "Локальный инструмент для очистки текста, восстановления структуры документа и форматирования Word/TXT.", "local": "Базовая очистка выполняется локально.", "ai": "Оптимизация с ИИ вызывает только сторонний API, настроенный пользователем.", "privacy": "Приложение не предоставляет общий API Key.", "disclaimer": "Обработка данных сторонними сервисами регулируется их собственными условиями."},
    "ar": {"subtitle": PRODUCT_NAME, "description": "أداة محلية أولاً لتنظيف النص وتنظيم بنية المستند وتنسيق Word/TXT.", "local": "يتم التنظيف الأساسي محلياً.", "ai": "لا يستدعي تحسين الذكاء الاصطناعي إلا API تابعاً لجهة خارجية يضبطه المستخدم.", "privacy": "لا يوفر التطبيق API Key مشتركاً.", "disclaimer": "تخضع معالجة البيانات بواسطة الجهات الخارجية لشروطها الخاصة."},
    "hi_IN": {"subtitle": PRODUCT_NAME, "description": "टेक्स्ट सफाई, दस्तावेज़ संरचना और Word/TXT स्वरूपण के लिए स्थानीय-प्रथम उपकरण।", "local": "मूल सफाई स्थानीय रूप से की जाती है।", "ai": "AI अनुकूलन केवल उपयोगकर्ता द्वारा कॉन्फ़िगर की गई तृतीय-पक्ष API को कॉल करता है।", "privacy": "ऐप कोई साझा API Key प्रदान नहीं करता।", "disclaimer": "तृतीय-पक्ष डेटा प्रसंस्करण उनकी अपनी शर्तों के अधीन है।"},
}
