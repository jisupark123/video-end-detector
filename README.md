# Video-End-Detector

사운드를 감지하여 동영상 종료를 탐지하고 사용자에게 알림을 보내는 스크립트

Detects the end of a video by detecting sound and sends a notification to the user.

동영상

<br/>

## Quick Start

1. Clone the repository

```bash
git clone https://github.com/jisupark123/video-end-detector.git
```

<br/>

2. Change the directory

```bash
cd video-end-detector
```

<br/>

3. Create and activate a virtual environment

```bash
# Foc macOS and Linux
python -m venv venv
source venv/bin/activate
```

```bash
# For Windows
python -m venv venv
source venv/Scripts/activate
```

<br/>

4. Install the required packages

```bash
pip install -r requirements.txt
```

<br/>

5. Run the script

```bash
python main.py
```

<br/>

## Usage

동영상이 끝났을 때 소리 알림을 제공하기 위해 소리 감지 기능을 설정해야 합니다. main.py 파일을 실행하면 소리 감지 설정이 자동으로 시작됩니다.

아래는 소리 감지 기능을 설정하고 사용하는 방법에 대한 단계별 가이드입니다.

1. 기본 노이즈 크기 설정

먼저, 동영상 재생을 멈춘 상태에서 주변의 기본 소음 크기를 측정해야 합니다. 다음과 같은 메시지가 출력됩니다.

```plaintext
동영상 재생을 멈추고 Enter를 눌러주세요
```

이 메시지가 출력되면, 동영상 재생을 멈추고 `Enter` 키를 눌러 기본 소음 크기를 측정합니다. 이때, 대화를 나누거나 다른 소음을 내지 않도록 주의해야 합니다.

<br/>

2. 활성 소음 크기 설정

다음으로, 동영상 재생 중 소리 감지를 위한 활성 소음 크기를 설정해야 합니다. 다음과 같은 메시지가 출력됩니다.

```plaintext
동영상 재생을 시작하고 Enter를 눌러주세요
```

이 메시지가 출력되면, 동영상 재생을 시작하고 `Enter` 키를 눌러 활성 소음 크기를 설정합니다.

만약 동영상의 볼륨이 너무 작다면, 설정을 통과하지 못할 수 있습니다. 이 경우 동영상의 볼륨을 높이거나 **`THRESHOLD`** 값을 낮춰서 동영상 볼륨에 대한 민감도를 높입니다.

추가로 주변 노이즈의 Variance가 높은 경우, **`EXTRA_THRESHOLD`** 값을 높여서 불필요한 알림을 최소화할 수 있습니다. (단, **`EXTRA_THRESHOLD`** 값을 높일수록 동영상 소리 감지가 더 어려워질 수 있습니다)

<br/>

설정이 완료되면, 주변 사운드를 감지하여 동영상이 끝났을 때 사용자에게 소리 알림을 제공하는 기능이 자동으로 실행됩니다.
