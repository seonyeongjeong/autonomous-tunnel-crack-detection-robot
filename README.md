<h1 align="center">Tunnel Inspection Robot <br> for Crack Detection and Risk Mapping</h1>

> 자율 주행 로봇 기반 터널 균열 탐지 및 위험도 지도화 시스템



### Team  
  제로 JERO

### Member  
  2391022 정선영 • 2391019 이정연

### Project Description  
  자율 주행 로봇이 터널 중앙을 주행하며 RGB-D 카메라로 주변 벽면의 균열을 실시간으로 인식합니다.  
  이후 실제 균열 크기를 산출해 위험도를 판별하고, 균열 위치와 위험 등급을 지도 위에 시각화하는 터널 안전 진단 시스템입니다.

### Presentation (YouTube)

<https://youtube.com/watch?v=pLZg_E13_us&si=x81DYS0wqA8a-N9c>

## Prerequisites

이 프로젝트는 다음 환경을 기준으로 실행합니다.

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Fortress
- Python 3.10

필요한 개발 도구와 ROS-Gazebo 연동 패키지를 설치합니다.

```bash
sudo apt update
sudo apt install -y \
  git \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-venv \
  ros-humble-ros-gz
```

## Installation

저장소를 `~/tunnel_ws`에 clone합니다.

```bash
git clone https://github.com/seonyeongjeong/autonomous-tunnel-crack-detection-robot.git ~/tunnel_ws
cd ~/tunnel_ws
```

`rosdep`을 처음 사용하는 환경이라면 한 번만 초기화합니다. 이미 초기화되어
있다면 `sudo rosdep init`은 생략하세요.

```bash
source /opt/ros/humble/setup.bash
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

ROS 2 패키지를 사용할 수 있도록 system site packages를 포함한 Python
가상환경을 만들고 Python 의존성을 설치합니다.

```bash
cd ~/tunnel_ws
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Tunnel Texture Option

터널 배경은
`src/tunnel_inspection_sim/models/tunnel/scripts/make_tunnel_texture.py`의
다음 설정으로 선택할 수 있습니다.

```python
USE_TEXTURE_IMAGE = True
```

- `True`: `texture/texture2.jpg` 이미지를 터널 배경으로 사용
- `False`: `BASE_COLOR`로 지정된 기본 단색 배경을 사용

설정을 변경한 경우 텍스처 생성 스크립트를 실행하세요. 이 명령은
`tunnel_with_cracks.png`및 crack ground truth 파일을 새 설정으로 덮어씁니다.

```bash
cd ~/tunnel_ws
source .venv/bin/activate
python src/tunnel_inspection_sim/models/tunnel/scripts/make_tunnel_texture.py
```

## Build

```bash
cd ~/tunnel_ws
source /opt/ros/humble/setup.bash
source .venv/bin/activate
colcon build --symlink-install --packages-select tunnel_inspection_sim
source install/setup.bash
```

소스 코드나 터널 텍스처를 변경했다면 위 빌드 명령을 다시 실행하세요.

## Quick Start

총 4개의 터미널을 열고 아래 순서대로 실행합니다. 각 터미널에서 먼저
다음 공통 설정을 실행해야 합니다.

```bash
cd ~/tunnel_ws
source /opt/ros/humble/setup.bash
source .venv/bin/activate
source install/setup.bash
```

### Terminal 1 — Start Gazebo

```bash
ign gazebo src/tunnel_inspection_sim/worlds/tunnel_world.sdf -r
```

Gazebo 창과 터널 world가 완전히 로드될 때까지 기다립니다.

### Terminal 2 — Spawn Robot and Start Bridge

```bash
ros2 launch tunnel_inspection_sim spawn_robot.launch.py
```

### Terminal 3 — Start Crack Detector

```bash
ros2 run tunnel_inspection_sim crack_detector
```

### Terminal 4 — Start Autonomous Wall Following

```bash
ros2 run tunnel_inspection_sim wall_following
```

실행을 종료하려면 각 터미널에서 `Ctrl+C`를 누르고 Gazebo 창을 닫습니다.

## References

  - **Blender 터널 모델링**  
    <https://youtu.be/vCder5cw0Ak?si=05Mf2PctH1hxgzBh>

  - **PID 기반 자율 주행**  
    <https://wikidocs.net/300880>

  - **Dataset**  
    <https://docs.ultralytics.com/datasets/segment/crack-seg>

  - **Model**  
    <https://huggingface.co/OpenSistemas/YOLOv8-crack-seg/tree/main/yolov8n/weights>

## AI Assistance Note
  아이디어 및 전체 프로젝트 기획안을 직접 구상한 뒤, 코드 구현 과정에서 Codex를 활용했습니다.
