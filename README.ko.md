<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# 클린텍스트 스튜디오

**로컬 우선 텍스트 정리, 문서 구조 복구, 수식 인식 미리 보기 및 복사, AI 생성 및 형식이 잘못된 텍스트에 대한 DOCX/TXT 내보내기.**

[영어](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [포르투갈어](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [اندي](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Windows용 다운로드

Current version: **v1.5.0**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## v1.5.0의 새로운 기능

- 프리젠테이션 계층에 대한 완전한 정적 로케일 카탈로그, 로컬 도움말 대화 상자 및 원자 로케일 유효성 검증.
- 안정적인 청소 값과 별도로 콤보 상자 라벨을 유지하므로 언어를 변경해도 사전 설정이 변경되거나 청소가 실행되지 않습니다.
- 공유 디자인 토큰을 통한 통합 패널, 컨트롤, 포커스, 체크박스 및 요약 카드 반올림.
- 법적 시스템 글꼴 대체를 사용합니다. 이 릴리스에는 PingFang, HarmonyOS Sans 또는 기타 글꼴 파일이 번들로 제공되지 않습니다.
- 주력 문서를 재작업하고 자동화된 README, UI 언어 및 정리 정지 검사를 추가했습니다.

## 기능

CleanText Studio는 유용한 문서 구조를 유지하면서 복사된 서식 잔여물을 제거합니다. 제목, 목록, 인용문, 코드, 마크다운 테이블, 링크 및 일반적인 수학 공식을 인식합니다. 동일한 구조화된 문서 모델이 텍스트 편집기, 미리 보기, TXT 내보내기 및 DOCX 내보내기에 피드를 제공하므로 내보낼 때 테이블이나 공식이 자동으로 손실되지 않습니다.

### 청소 및 구조 복구

- Markdown 제목, 강조, 인라인 코드, 링크, 이미지, 구분 기호, HTML 사본 잔여물, 이모티콘 및 장식 문자를 정리합니다.
- 제목, 목록, 인용문, 코드 블록 및 표를 문자 벽으로 병합하는 대신 감지합니다.
- 압축 결합, 스마트 섹션 간격 또는 보존된 단락 경계를 선택하세요.
- 기본적으로 독립형 URL을 유지합니다. 선택적 URL 처리는 명시적입니다.

### 테이블 및 Word 내보내기

마크다운 테이블은 구조화된 테이블 블록으로 구문 분석됩니다. 미리보기 모드는 실제 테이블을 표시하고 DOCX 내보내기는 굵은 머리글, 보이는 테두리, 적응형 너비 및 깨끗한 셀 텍스트가 있는 기본 Word 테이블을 작성합니다. 긴 내용은 강제로 짧은 줄로 나열되는 대신 읽을 수 있는 상태로 유지됩니다.

### 수학

일반적인 인라인 및 디스플레이 LaTeX, 유니코드 수학 표현식 및 간단한 방정식은 Markdown 정리 전에 보호됩니다. 지원되는 수식은 Word OMML 기본 방정식으로 내보내집니다. 지원되지 않는 구문은 변수를 잃지 않고 읽을 수 있는 텍스트로 대체됩니다. 이 애플리케이션은 수학적 의미를 계산, 증명 또는 변경하지 않습니다.

### 선택적 BYOK AI 최적화

로컬 정리는 완전히 오프라인으로 작동합니다. AI 최적화는 선택 사항이며 자체 공급자, 엔드포인트, 모델 및 API 키를 구성한 후에만 실행됩니다. CleanText Studio는 공개 키, 프록시 공급자 또는 유료 모델 청구서를 제공하지 않습니다. 제3자가 처리하기에 적합하지 않은 자료를 보내지 마십시오.

<!-- section:privacy -->
## 개인 정보 보호 및 안전

기본 정리, 미리보기, TXT 내보내기 및 Word 내보내기는 로컬에서 실행됩니다. 앱에는 광고, 원격 측정, 계정 시스템 또는 공개 AI 키가 없습니다. 서식 지정, 문서 구조 및 레이아웃 도구입니다. AI 탐지 회피, 표절 회피, 사칭, 학문적 부정행위 또는 조작된 인용을 제공하지 **않습니다**.

## 빠른 시작

1. 애플리케이션을 시작하고 텍스트를 붙여넣거나 TXT, Markdown 또는 DOCX를 엽니다.
2. 정리 사전 설정 및 단락 모드를 선택합니다.
3. **Clean**을 클릭하고 **텍스트 모드** 또는 **미리보기 모드**를 검사합니다.
4. 구조화된 콘텐츠를 TXT 또는 Word로 내보냅니다.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## 입력, 출력 및 시스템 요구 사항

입력: `.txt`, `.md`, `.markdown` 및 `.docx`. 출력: UTF-8 `.txt` 및 구조화된 `.docx`. v1.5.0은 Windows x64 데스크톱 릴리스입니다. macOS, Linux 및 Android는 출시된 플랫폼으로 주장되지 않습니다.

## 소스에서

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## 테스트 및 빌드

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

Windows 빌드는 `dist/` 아래에 onedir 애플리케이션, 휴대용 ZIP, Inno 설치 프로그램, SHA256 체크섬 및 릴리스 노트를 생성합니다.

## 현지화, 기여 및 제한사항

인터페이스는 중국어 간체, 중국어 번체, 영어, 일본어, 한국어, 스페인어, 프랑스어, 독일어, 브라질 포르투갈어, 러시아어, 아랍어(RTL) 및 힌디어를 제공합니다. 번역 검토를 환영합니다. [번역 가이드](docs/TRANSLATION_GUIDE.md)를 참조하세요. 복잡한 사용자 정의 LaTeX 매크로는 텍스트 대체를 사용할 수 있으며 DOCX 가져오기는 모든 소스 문서 스타일이나 포함된 이미지를 유지하지 않습니다.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## 특허

MIT 라이센스. [LICENSE](LICENSE) 및 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)를 참조하세요.

> Translation review from the community is welcome.
