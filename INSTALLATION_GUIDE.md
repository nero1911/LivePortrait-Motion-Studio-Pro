# 📖 상세 설치 가이드

## Windows 11 기준 설치

### 1단계: 필수 소프트웨어 설치

#### 1.1 Python 3.11 설치

1. [Python 3.11 공식 사이트](https://www.python.org/downloads/) 방문
2. "Download Python 3.11" 버튼 클릭
3. 설치 프로그램 실행
4. **중요**: 아래의 체크박스 반드시 선택
   - ✅ "Add Python 3.11 to PATH"
5. "Install Now" 클릭
6. 설치 완료 대기

**설치 확인**:
```bash
python --version
# 또는
python -V
```

#### 1.2 NVIDIA CUDA Toolkit 설치

**전제조건**: NVIDIA GPU 드라이버 설치 필요

```bash
# NVIDIA 드라이버 확인
nvidia-smi
```

1. [NVIDIA CUDA Toolkit 12.1](https://developer.nvidia.com/cuda-12-1-0-download-center) 다운로드
2. 설치 선택:
   - OS: Windows
   - Architecture: x86_64
   - Version: 11 (또는 최신)
   - Installer Type: exe (local) 권장
3. 설치 프로그램 실행
4. "Express Installation" 또는 "Custom Installation" 선택
   - Express 권장 (모든 기본값 설정)
5. 설치 완료 대기 (15~30분)

#### 1.3 cuDNN 설치

1. [NVIDIA cuDNN](https://developer.nvidia.com/cudnn) 다운로드
   - NVIDIA 계정 가입 필요
   - cuDNN 8.x for CUDA 12.x 버전 다운로드
2. ZIP 파일 압축 해제
3. 폴더 내 파일들을 CUDA 설치 경로로 복사:
   ```
   C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\
   ```
   - `bin` 폴더 → CUDA `bin` 에 복사
   - `lib` 폴더 → CUDA `lib` 에 복사
   - `include` 폴더 → CUDA `include` 에 복사

### 2단계: 프로젝트 준비

#### 2.1 GitHub에서 다운로드

**방법 1: Git 사용 (권장)**
```bash
git clone https://github.com/nero1911/LivePortrait-Motion-Studio-Pro.git
cd LivePortrait-Motion-Studio-Pro
```

**방법 2: ZIP 다운로드**
1. GitHub 저장소 방문
2. Code → Download ZIP 클릭
3. ZIP 파일 압축 해제
4. 명령 프롬프트에서 폴더 이동

### 3단계: 자동 설치 (권장)

#### Windows 사용자

1. 파일 탐색기에서 프로젝트 폴더 이동
2. `install.bat` 더블클릭
3. 명령 프롬프트 창이 열림
4. 설치 과정 자동 실행
5. 완료 대기 (10~20분)

**설치 과정**:
```
Installing LivePortrait Motion Studio Pro...

Creating virtual environment...
Activating virtual environment...
Installing dependencies...
(많은 패키지 설치 중...)

Installation complete!
```

### 4단계: 수동 설치 (install.bat 실패시)

#### 4.1 가상 환경 생성

```bash
python -m venv venv
```

#### 4.2 가상 환경 활성화

```bash
# Windows
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

**확인**: 프롬프트가 `(venv)` 로 시작되어야 함

#### 4.3 pip 업그레이드

```bash
pip install --upgrade pip
```

#### 4.4 의존성 설치

```bash
pip install -r requirements.txt
```

**주요 패키지**:
- torch==2.0.1 (PyTorch)
- gradio==4.30.0 (UI)
- opencv-python==4.8.1.78 (이미지 처리)
- imageio==2.34.0 (비디오 저장)

### 5단계: CUDA 설치 확인

```bash
# Python에서 CUDA 가용성 확인
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('CUDA Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

**정상 출력 예**:
```
CUDA Available: True
CUDA Device: NVIDIA GeForce RTX 4060 Ti
```

**문제 해결**: "CUDA Available: False" 출력시
1. NVIDIA 드라이버 업데이트
   ```bash
   nvidia-smi  # 드라이버 버전 확인
   ```
2. CUDA 설치 경로 확인
   ```
   C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\
   ```
3. 환경 변수 확인:
   - "고급 시스템 설정" → "환경 변수"
   - CUDA_HOME 또는 CUDA_PATH 확인

### 6단계: 애플리케이션 실행

#### 6.1 자동 실행

Windows 사용자:
```bash
run.bat
```

#### 6.2 수동 실행

```bash
# 가상 환경 활성화 (필요시)
venv\Scripts\activate.bat

# 애플리케이션 실행
python main.py
```

**정상 실행 표시**:
```
Initializing LivePortrait Motion Studio Pro...
Using device: cuda
AnimationEngine initialized on cuda
Creating UI...
Launching Gradio interface...
Running on http://127.0.0.1:7860
```

### 7단계: 브라우저에서 접속

1. 브라우저 열기 (Chrome, Firefox, Edge 등)
2. 주소창에 입력: `http://127.0.0.1:7860`
3. Enter 키 누르기

**로그인 필요**: 없음 (로컬 실행)

---

## 문제 해결

### 문제 1: "Python is not recognized"

**원인**: Python이 PATH에 추가되지 않음

**해결방법**:
1. Python 재설치 (Add Python to PATH 체크)
2. 또는 완전한 경로로 실행:
   ```bash
   C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\python.exe --version
   ```

### 문제 2: "CUDA out of memory"

**원인**: GPU 메모리 부족

**해결방법**:
1. 다른 GPU 프로그램 종료
2. 프리뷰 해상도 낮추기 (480P)
3. 더 낮은 사양 GPU 지원 확인

### 문제 3: "ModuleNotFoundError: No module named 'torch'"

**원인**: 의존성 설치 실패

**해결방법**:
1. 가상 환경 재생성:
   ```bash
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate.bat
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### 문제 4: Gradio 포트 이미 사용중

**원인**: 다른 프로세스가 7860 포트 사용

**해결방법**:
```bash
# 다른 포트로 실행
python main.py --port 7861
```

그 후 `http://127.0.0.1:7861` 접속

### 문제 5: 이미지 업로드 실패

**확인 사항**:
- 파일 형식: PNG, JPG, JPEG, WEBP만 지원
- 파일 크기: 256x256 이상
- 파일 손상 여부

---

## 업그레이드

### 최신 버전으로 업데이트

```bash
cd LivePortrait-Motion-Studio-Pro
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 완전 제거

```bash
# 가상 환경 삭제
rmdir /s venv

# 프로젝트 폴더 삭제
cd ..
rmdir /s LivePortrait-Motion-Studio-Pro
```

---

## 다음 단계

설치가 완료되면:
1. [README.md](README.md) 참조 - 기본 사용법
2. 이미지 업로드하여 테스트
3. 각 슬라이더로 애니메이션 조절
4. 최종 영상 렌더링 및 저장

**행운을 빕니다! 🎉**
