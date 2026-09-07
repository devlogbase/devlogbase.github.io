# 블로그 도표용 폰트

블로그 본문에 넣는 SVG 도표/차트의 글자에 쓰는 폰트다. 사이트 자체(`_config.yml`, 테마 CSS)에서는 쓰지 않는다.

| 폰트 | 용도 | 라이선스 | 출처 | 받은 날짜 |
| --- | --- | --- | --- | --- |
| `Jua-Regular.ttf` | 도표 제목 | SIL Open Font License 1.1 (`OFL-Jua.txt`) | Google Fonts (`github.com/google/fonts/ofl/jua`) | 2026-09-07 |
| `Pretendard-Regular.ttf` | 도표 본문/설명 | SIL Open Font License 1.1 (`OFL-Pretendard.txt`) | `github.com/orioncactus/pretendard` v1.3.9 (jsDelivr) | 2026-09-07 |
| `Pretendard-SemiBold.ttf` | 도표 소제목/강조 | 위와 동일 | 위와 동일 | 2026-09-07 |

## 왜 파일을 저장소에 두나

OFL로 공개된 버전은 나중에 유료로 바뀌어도 그 버전은 영구히 그 조건으로 쓸 수 있다. 받은 시점의 파일과 라이선스 원문을 함께 보관해 근거를 남긴다.

## 사용 방법

`embed_fonts.py`가 SVG 안 `<text>`에서 쓰인 글자만 골라 각 폰트를 서브셋한 뒤 woff2로 base64 임베딩한다. 네트워크 없이도 렌더링이 재현된다.

```
python embed_fonts.py <입력.svg> <출력.svg>
```

출력 SVG를 `agent-browser`로 열어 PNG로 캡처하고, 그 PNG만 게시글에 넣는다. 원본 SVG와 임베딩 SVG는 렌더 후 삭제한다.
