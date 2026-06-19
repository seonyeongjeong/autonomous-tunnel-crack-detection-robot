import os
import urllib.request
import zipfile
import cv2
import numpy as np
from pathlib import Path

def load_dataset():
    url = "https://ultralytics.com/assets/crack-seg.zip"
    zip_path = "crack_preprocess/crack-seg.zip"

    if not os.path.exists("./images/test"):
        print("📦 1. Downloading dataset...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("🗜️ 2. Extracting zip file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print("✅ Completed!")
    else:
        print("✅ Existing dataset found. Skipping download and extraction.")
    
def process_yolo_segmentation_to_transparent():
    img_dir = "crack_preprocess/images/test"
    label_dir = "crack_preprocess/labels/test"
    output_dir = "crack_preprocess/transparent_cracks"
    os.makedirs(output_dir, exist_ok=True)

    # Test 폴더 내의 모든 jpg 이미지 찾기
    img_files = list(Path(img_dir).glob("*.jpg"))
    print(f"🔍 Found a total of {len(img_files)} images in the test set.")

    print("🖌️ 3. Starting background transparency work...")
    for img_path in img_files:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
            
        h, w = img.shape[:2]
        label_path = os.path.join(label_dir, img_path.stem + ".txt")

        # 마스크용 빈 캔버스 (전부 검은색=투명 0) 생성
        mask = np.zeros((h, w), dtype=np.uint8)

        # 라벨 파일이 존재하면 읽어서 다각형 그리기
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                # YOLO 포맷: class_id x1 y1 x2 y2 ... (모두 0~1 사이로 정규화된 값)
                data = list(map(float, line.strip().split()))
                
                # 첫 번째 값(class_id)을 제외한 나머지 좌표 가져오기
                coords = data[1:]
                
                # 좌표를 (x, y) 쌍으로 묶고 실제 픽셀 크기로 복원
                pts = np.array(coords).reshape(-1, 2)
                pts[:, 0] *= w  # x좌표 복원
                pts[:, 1] *= h  # y좌표 복원
                pts = pts.astype(np.int32)

                # 다각형 내부를 흰색(255=불투명)으로 채우기
                cv2.fillPoly(mask, [pts], 255)

        # 균열 색상을 밝은 원본 대신 완전히 진한 검은색(0)으로 채웁니다.
        black_channel = np.zeros_like(mask)
        # RGB 채널은 모두 0(검은색), Alpha 채널만 mask(균열 부위만 255=불투명) 적용
        rgba = cv2.merge([black_channel, black_channel, black_channel, mask])

        out_name = os.path.join(output_dir, img_path.stem + "_decal.png")
        cv2.imwrite(out_name, rgba)

    print(f"Success! Converted transparent crack images are saved in the '{output_dir}' folder.")

# 실행
if __name__ == "__main__":
    load_dataset()
    process_yolo_segmentation_to_transparent()