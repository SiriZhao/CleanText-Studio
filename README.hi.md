<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# क्लीनटेक्स्ट स्टूडियो

**स्थानीय-प्रथम पाठ सफाई, दस्तावेज़ संरचना पुनर्प्राप्ति, सूत्र-जागरूक पूर्वावलोकन, और कॉपी किए गए, एआई-जनरेटेड और खराब स्वरूपित पाठ के लिए DOCX/TXT निर्यात।**

[अंग्रेजी](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [पुर्तगाली](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## विंडोज़ के लिए डाउनलोड करें

Current version: **v1.5.0**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## v1.5.0 में नया क्या है?

- पूर्ण स्थैतिक लोकेल कैटलॉग, एक स्थानीय सहायता संवाद, और प्रस्तुति परत के लिए परमाणु लोकेल सत्यापन।
- कॉम्बो-बॉक्स लेबल को स्थिर सफाई मूल्यों से अलग रखा जाता है, इसलिए भाषा बदलने से कभी भी प्रीसेट नहीं बदलता या सफाई शुरू नहीं होती।
- साझा डिज़ाइन टोकन के माध्यम से एकीकृत पैनल, नियंत्रण, फ़ोकस, चेकबॉक्स और सारांश-कार्ड राउंडिंग।
- कानूनी प्रणाली-फ़ॉन्ट फ़ॉलबैक का उपयोग करता है। इस रिलीज़ में कोई पिंगफैंग, हार्मनीओएस सैन्स या अन्य फ़ॉन्ट फ़ाइल बंडल नहीं की गई है।
- प्रमुख दस्तावेज़ीकरण पर दोबारा काम किया गया और स्वचालित README, UI-भाषा और क्लीनिंग-फ़्रीज़ जाँचें जोड़ी गईं।

## यह क्या करता है

क्लीनटेक्स्ट स्टूडियो उपयोगी दस्तावेज़ संरचना को संरक्षित करते हुए कॉपी किए गए फ़ॉर्मेटिंग अवशेषों को हटा देता है। यह शीर्षकों, सूचियों, उद्धरणों, कोड, मार्कडाउन तालिकाओं, लिंक और सामान्य गणितीय सूत्रों को पहचानता है। वही संरचित दस्तावेज़ मॉडल टेक्स्ट एडिटर, पूर्वावलोकन, TXT निर्यात और DOCX निर्यात को फीड करता है ताकि निर्यात पर कोई तालिका या सूत्र चुपचाप खो न जाए।

### सफ़ाई और संरचना पुनर्प्राप्ति

- साफ़ मार्कडाउन शीर्षक, जोर, इनलाइन कोड, लिंक, चित्र, विभाजक, HTML कॉपी अवशेष, इमोजी और सजावटी वर्ण।
- शीर्षकों, सूचियों, उद्धरणों, कोड ब्लॉकों और तालिकाओं को एक चरित्र दीवार में समतल करने के बजाय उनका पता लगाएं।
- कॉम्पैक्ट जॉइनिंग, स्मार्ट सेक्शन स्पेसिंग, या संरक्षित पैराग्राफ सीमाएँ चुनें।
- डिफ़ॉल्ट रूप से स्टैंडअलोन यूआरएल रखें; वैकल्पिक यूआरएल प्रबंधन स्पष्ट है।

### टेबल्स और वर्ड निर्यात

मार्कडाउन तालिकाओं को संरचित तालिका ब्लॉकों में पार्स किया जाता है। पूर्वावलोकन मोड एक वास्तविक तालिका प्रदर्शित करता है, और DOCX निर्यात बोल्ड हेडर, दृश्य सीमाओं, अनुकूली चौड़ाई और स्वच्छ सेल टेक्स्ट के साथ एक मूल वर्ड तालिका लिखता है। लंबी सामग्री जबरन छोटी पंक्तियों का क्रम बनने के बजाय पठनीय बनी रहती है।

### अंक शास्त्र

मार्कडाउन क्लीनअप से पहले सामान्य इनलाइन और डिस्प्ले लाटेक्स, यूनिकोड गणितीय अभिव्यक्ति और सरल समीकरण सुरक्षित हैं। समर्थित फ़ार्मुलों को Word OMML मूल समीकरणों के रूप में निर्यात किया जाता है; असमर्थित निर्माण वेरिएबल खोने के बजाय पठनीय पाठ पर वापस आते हैं। एप्लिकेशन गणितीय अर्थ की गणना, सिद्ध या परिवर्तन नहीं करता है।

### वैकल्पिक BYOK AI अनुकूलन

स्थानीय सफ़ाई पूरी तरह से ऑफ़लाइन काम करती है। एआई अनुकूलन वैकल्पिक है और आपके द्वारा अपने स्वयं के प्रदाता, समापन बिंदु, मॉडल और एपीआई कुंजी को कॉन्फ़िगर करने के बाद ही चलता है। क्लीनटेक्स्ट स्टूडियो सार्वजनिक कुंजी, प्रॉक्सी प्रदाता या मॉडल बिल का भुगतान नहीं करता है। ऐसी सामग्री न भेजें जो किसी तीसरे पक्ष के प्रसंस्करण के लिए अनुपयुक्त हो।

<!-- section:privacy -->
## गोपनीयता और सुरक्षा

बुनियादी सफाई, पूर्वावलोकन, TXT निर्यात और Word निर्यात स्थानीय रूप से चलते हैं। ऐप में कोई विज्ञापन, टेलीमेट्री, खाता प्रणाली या सार्वजनिक एआई कुंजी नहीं है। यह एक फ़ॉर्मेटिंग, दस्तावेज़-संरचना और लेआउट टूल है; यह एआई-डिटेक्शन चोरी, साहित्यिक चोरी चोरी, प्रतिरूपण, शैक्षणिक कदाचार, या मनगढ़ंत उद्धरण की पेशकश **नहीं** करता है।

## त्वरित शुरुआत

1. एप्लिकेशन प्रारंभ करें, टेक्स्ट पेस्ट करें या TXT, Markdown, या DOCX खोलें।
2. सफाई प्रीसेट और पैराग्राफ़ मोड का चयन करें।
3. **साफ़** पर क्लिक करें और **टेक्स्ट मोड** या **पूर्वावलोकन मोड** का निरीक्षण करें।
4. संरचित सामग्री को TXT या Word में निर्यात करें।

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## इनपुट, आउटपुट और सिस्टम आवश्यकताएँ

इनपुट: `.txt`, `.md`, `.markdown`, और `.docx`। आउटपुट: UTF-8 `.txt` और संरचित `.docx`। v1.5.0 एक विंडोज़ x64 डेस्कटॉप रिलीज़ है। macOS, Linux और Android को रिलीज़ किए गए प्लेटफ़ॉर्म के रूप में दावा नहीं किया गया है।

## स्रोत से

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## परीक्षण करें और निर्माण करें

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

विंडोज़ बिल्ड एक onedir एप्लिकेशन, एक पोर्टेबल ज़िप, एक इनो सेटअप इंस्टॉलर, SHA256 चेकसम और `dist/` के तहत रिलीज़ नोट्स तैयार करता है।

## स्थानीयकरण, योगदान और सीमाएँ

इंटरफ़ेस सरलीकृत चीनी, पारंपरिक चीनी, अंग्रेजी, जापानी, कोरियाई, स्पेनिश, फ्रेंच, जर्मन, ब्राजीलियाई पुर्तगाली, रूसी, अरबी (आरटीएल) और हिंदी प्रदान करता है। अनुवाद समीक्षा का स्वागत है; [अनुवाद मार्गदर्शिका](docs/TRANSLATION_GUIDE.md) देखें। जटिल कस्टम LaTeX मैक्रोज़ टेक्स्ट फ़ॉलबैक का उपयोग कर सकते हैं, और DOCX आयात प्रत्येक स्रोत-दस्तावेज़ शैली या एम्बेडेड छवि को संरक्षित नहीं करता है।

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## लाइसेंस

एमआईटी लाइसेंस. [लाइसेंस](लाइसेंस) और [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) देखें।

> Translation review from the community is welcome.
