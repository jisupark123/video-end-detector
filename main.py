import pyaudio
import pygame
import numpy as np
import time
from rainbow_tqdm import tqdm
from utils import print_rainbow_text, print_color_text

# 사운드 감지 설정
CHUNK = 2048  # 버퍼 크기
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 1: mono, 2: stereo
RATE = 44100  # Hz
THRESHOLD = 10  # 사운드 감지 임계값 (작게 설정할수록 민감해짐)
EXTRA_THRESHOLD = 5  # 추가 임계값 (초기 설정 시 사용, 사운드에 대해 더욱 Robust하게 만들기 위함) | fmt:off
SILENCE_LIMIT = 5  # 연속적인 사운드 없음을 감지할 시간 (초 아님)
ALERT_SOUND_FILE = "notification.wav"  # 알림 사운드 파일 경로
SOUND_VOLUME = 1.0  # 효과음 볼륨, `0.0` ~ `1.0` 사이의 값으로 설정
BASE_NOISE = 0.0  # 기본 노이즈 크기 (동영상 재생 멈췄을 때)
ACTIVE_NOISE = 0.0  # 활성 노이즈 크기 (동영상 재생 중일 때)
TIME_INTERVAL = 0.3  # 사운드 체크 간격 (초)

notification_count = 0
silent_colors = ["", "cyan", "green", "yellow", "purple", "red"]


def get_stream():
    return p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )


def get_buffer():
    stream = get_stream()
    return np.frombuffer(
        stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16
    )


# 최대값과 최소값을 제외한 평균값 계산
def mean_excluding_min_max(nums):
    return (np.sum(nums) - np.max(nums) - np.min(nums)) / (len(nums) - 2)


def get_volume(iter=10, verbose=False):
    noises = []
    iter_class = tqdm(range(iter)) if verbose else range(iter)
    for _ in iter_class:
        data = get_buffer()
        noise = mean_excluding_min_max(np.abs(data))
        noises.append(noise)
        time.sleep(TIME_INTERVAL)

    return mean_excluding_min_max(noises)


def config_sound_detection():
    global BASE_NOISE, ACTIVE_NOISE
    input("동영상 재생을 멈추고 Enter를 눌러주세요")
    BASE_NOISE = get_volume(iter=20, verbose=True)
    print(f"기본 노이즈 크기: {BASE_NOISE:.2f}", end="\n\n")

    while not ACTIVE_NOISE:
        input("동영상 재생을 시작하고 Enter를 눌러주세요")
        noise = get_volume(iter=20, verbose=True)
        print(
            f"활성 노이즈 크기: {noise:.2f}, 목표 노이즈 크기: {BASE_NOISE + THRESHOLD + EXTRA_THRESHOLD:.2f}"
        )
        if noise - BASE_NOISE > THRESHOLD + EXTRA_THRESHOLD:
            ACTIVE_NOISE = noise
            print(end="\n\n\n")
            print_rainbow_text("#" * 50, end="\n\n")
            print_rainbow_text("노이즈 크기 설정 완료 | 프로그램 시작", end="\n\n")
            print_rainbow_text("#" * 50)
            print(end="\n\n\n")
        else:
            print(
                "볼륨을 높이고 다시 시도해주세요 (민감도를 높이려면 THRESHOLD 값을 낮춰주세요)"
            )


def send_notification(sound):
    global notification_count
    sound.play()
    notification_count += 1
    print_rainbow_text(f"Notification #{notification_count}!", end="\n\n")


def load_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(SOUND_VOLUME)
    return sound


def is_silent(data):
    # 사운드가 없으면 True 반환
    return np.mean(np.abs(data)) < THRESHOLD


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = get_stream()
    alert_sound = load_sound(ALERT_SOUND_FILE)
    config_sound_detection()

    silent_chunks = 0
    while True:
        try:
            volume = get_volume(iter=10)
            if volume - BASE_NOISE < THRESHOLD:
                silent_chunks += 1

                # if silent_chunks > (SILENCE_LIMIT * RATE / CHUNK):
                if silent_chunks > SILENCE_LIMIT:
                    send_notification(alert_sound)
                    silent_chunks = 0  # 알림을 보낸 후 silent_chunks 초기화

                else:
                    print_color_text(
                        f"Silent chunks: {silent_chunks} | volume: {volume}",
                        color=silent_colors[silent_chunks],
                    )
            else:
                silent_chunks = 0
                print(f"Slient chunks reset | volume: {volume}")

        except IOError as e:
            print(f"Error recording: {e}")

        stream.close()
