# 🎬 LivePortrait Motion Studio Pro

**Real-time Interactive Animation Editor**

LivePortrait Motion Studio Pro는 정적 이미지를 입력받아 사용자가 슬라이더를 조작하면서 실시간으로 자연스러운 애니메이션을 편집할 수 있는 Windows용 데스크톱 애플리케이션입니다.

## ✨ 주요 특징

- 🖼️ **이미지 업로드**: PNG, JPG, JPEG, WEBP 지원
- 🎭 **표정 프리셋**: 11개의 미리 정의된 표정 (행복, 슬픔, 놀람, 분노, 졸음 등)
- 👀 **눈 깜빡임 제어**: 강도와 빈도 조절 가능
- 😊 **표정 변화**: 미소, 일반 표정 강도 조절
- 🤨 **고개 움직임**: 회전(좌우, 상하), 기울임, 끄덕거림
- 💇 **머리카락 흩날림**: 강도와 방향 조절 가능
- 🌬️ **호흡 애니메이션**: 강도와 빈도 조절
- 👁️ **시선 방향**: X, Y 축 조절 가능
- 📹 **실시간 프리뷰**: 슬라이더 조작 후 0.5초 뒤 자동 갱신
- 💾 **다중 포맷 저장**: MP4, GIF 지원
- 📊 **해상도 옵션**: 480P, 720P, 1080P

## 🚀 설치 방법

### 요구사항
- Windows 11 (또는 Windows 10 21H2 이상)
- Python 3.11+
- NVIDIA GPU (RTX 4060 Ti 8GB 이상 권장)
- CUDA 12.1
- cuDNN 8.x

### 설치 단계

#### 1. Python 설치
[Python 3.11](https://www.python.org/downloads/) 다운로드 및 설치

설치 시 반드시 "Add Python to PATH" 체크

#### 2. CUDA 설치

```bash
# NVIDIA CUDA Toolkit 12.1 설치
# https://developer.nvidia.com/cuda-12-1-0-download-center

# cuDNN 설치
# https://developer.nvidia.com/cudnn
```

#### 3. 프로젝트 설치

```bash
# 저장소 클론
git clone https://github.com/nero1911/LivePortrait-Motion-Studio-Pro.git
cd LivePortrait-Motion-Studio-Pro

# 자동 설치 (Windows)
double-click install.bat

# 또는 수동 설치
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 🎮 사용 방법

### 시작하기

```bash
# Windows
run.bat

# 또는
python main.py
```

그 다음 브라우저에서 `http://127.0.0.1:7860` 접속

### 기본 워크플로우

1. **이미지 업로드**
   - PNG, JPG, JPEG, WEBP 형식 이미지 업로드
   - 최소 해상도: 256x256
   - 최대 해상도: 1920x1920

2. **표정 프리셋 선택** (선택사항)
   - 11개의 미리 정의된 표정 중 선택
   - "Apply Preset" 버튼 클릭

3. **슬라이더로 세부 조절**
   - 각 슬라이더 조작
   - 0.5초 후 자동으로 프리뷰 생성

4. **실시간 프리뷰 확인**
   - 우측 패널에서 실시간 프리뷰
   - 자동 재생

5. **최종 렌더링**
   - 출력 형식 선택 (MP4/GIF)
   - FPS, 길이, 해상도 설정
   - "Render & Save" 버튼 클릭

6. **저장**
   - 기본 저장 폴더: `C:\Users\[UserName]\LivePortrait_Output`
   - 생성된 파일 자동 저장

## 🎭 표정 프리셋 목록

| 프리셋 | 설명 |
|--------|------|
| **Neutral** | 중립적인 표정 |
| **Happy** | 행복한 표정, 큰 미소 |
| **Sad** | 슬픈 표정, 고개 숙임 |
| **Confused** | 혼란스러운 표정 |
| **Serious** | 진지한 표정 |
| **Surprised** | 놀란 표정, 빠른 눈 깜빡임 |
| **Excited** | 흥분된 표정, 강한 움직임 |
| **Sleepy** | 졸린 표정, 느린 눈 깜빡임 |
| **Angry** | 화난 표정 |
| **Contemplative** | 생각하는 표정, 옆으로 흘겨봄 |
| **Idle Loop** | 기본 대기 애니메이션 |

## 🎚️ 슬라이더 컨트롤

### Face Animation (얼굴 애니메이션)
- **👀 Eye Blink Intensity**: 0~100 (눈 깜빡임 강도)
- **👁️ Eye Blink Frequency**: 0.1~5 (눈 깜빡임 빈도)
- **😊 Smile Strength**: 0~100 (미소 강도)
- **😐 Expression Intensity**: 0~100 (표정 강도)

### Head Movement (고개 움직임)
- **↔️ Head Yaw**: -30~30 (좌우 회전)
- **↕️ Head Pitch**: -30~30 (상하 회전)
- **⤴️ Head Roll**: -20~20 (기울임)
- **🤨 Head Nod Intensity**: 0~100 (끄덕거림 강도)

### Physics Simulation (물리 시뮬레이션)
- **💇 Hair Flutter Amount**: 0~100 (머리카락 흩날림 강도)
- **💨 Hair Wind Direction**: -180~180 (바람 방향)
- **🌬️ Breathing Intensity**: 0~100 (호흡 강도)
- **💓 Breathing Frequency**: 0.1~2 (호흡 빈도)

### Eye Gaze (시선)
- **👁️ Eye Gaze X**: -30~30 (좌우)
- **👁️ Eye Gaze Y**: -30~30 (상하)

## ⚙️ 출력 설정

### 형식
- **MP4**: 최고 품질, 권장
- **GIF**: 용량 작음, 웹 공유용

### 해상도
- **480P** (854x480): 빠른 처리
- **720P** (1280x720): 균형
- **1080P** (1920x1080): 최고 품질

### FPS
- 15~60 fps 선택 가능
- 30 fps 권장

### 길이
- 1~10초 설정 가능
- 기본값: 3초

## 🖥️ 시스템 요구사항

### 최소 사양
- Windows 11
- Intel i7 / AMD Ryzen 5
- NVIDIA RTX 3060 6GB
- 16GB RAM
- SSD 10GB 이상

### 권장 사양 (최적 성능)
- Windows 11
- Intel i9 / AMD Ryzen 9
- NVIDIA RTX 4060 Ti 8GB 이상
- 32GB RAM
- NVMe SSD

## 📊 성능 최적화

### 프리뷰 모드
- 자동 480P로 감소
- 15 fps로 제한
- 2초 최대 길이
- **목표**: 1~3초 생성

### CUDA 가속
- 자동으로 GPU 감지
- 최대 성능 활용
- VRAM 최적화

## 🐛 문제 해결

### CUDA 오류
```
Error: CUDA is not available
```

**해결방법**:
1. NVIDIA GPU 드라이버 최신 버전 설치
2. CUDA Toolkit 12.1 설치
3. cuDNN 설정

```bash
# CUDA 설치 확인
python -c "import torch; print(torch.cuda.is_available())"
```

### 메모리 오류
```
RuntimeError: CUDA out of memory
```

**해결방법**:
- 프리뷰 해상도 낮추기
- 영상 길이 단축
- GPU 메모리 사용량 모니터링

### 이미지 업로드 실패
- 지원 형식 확인 (PNG, JPG, JPEG, WEBP)
- 이미지 크기 확인 (256x256 이상)
- 파일 손상 여부 확인

## 📁 프로젝트 구조

```
LivePortrait-Motion-Studio-Pro/
├── main.py                 # 메인 애플리케이션
├── animation_engine.py     # 애니메이션 생성 엔진
├── ui_handler.py          # UI 처리 및 저장 기능
├── expression_presets.py   # 표정 프리셋 관리
├── requirements.txt        # 의존성 목록
├── install.bat            # Windows 자동 설치
├── run.bat                # Windows 실행 스크립트
└── README.md              # 이 파일
```

## 🔄 실시간 프리뷰 시스템

### Debounce 방식
- 사용자가 슬라이더를 조작할 때마다 타이머 시작
- 슬라이더 움직임이 0.5초 동안 멈추면 프리뷰 생성
- 생성 중 추가 조작은 무시됨
- 프리뷰 완료 후 자동 재생

### 프리뷰 캐싱
- 중복 생성 방지
- 메모리 최적화

## 📝 라이선스

MIT License

## 🤝 기여

버그 리포트 및 기능 제안은 GitHub Issues를 통해 제출해주세요.

## 📧 문의

문제 또는 제안사항: [GitHub Issues](https://github.com/nero1911/LivePortrait-Motion-Studio-Pro/issues)

---

**주의**: 이 프로젝트는 교육 및 개인 용도로 제작되었습니다. 상업적 사용은 별도의 라이선스가 필요합니다.
