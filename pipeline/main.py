import os
import sys
# BiRefNet 폴더의 절대 경로를 Python 경로에 추가
birefnet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BiRefNet')
sys.path.append(birefnet_path)
import time
from glob import glob
from PIL import Image
import requests
import torch
from torchvision import transforms
from models.birefnet import BiRefNet
from utils import check_state_dict
from image_proc import refine_foreground
import wget

# Stability AI API 정보
API_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"
API_KEY = "sk-IlZh99pIYsl4UhAay5IjtXfbCZ6cNRhWr6dlh1sCvcBeb6bS"

# BiRefNet 모델 초기화
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

model_path = 'BiRefNet-general-epoch_244.pth'
if not os.path.exists(model_path):
    print("Downloading BiRefNet model weights...")
    wget.download("https://github.com/ZhengPeng7/BiRefNet/releases/download/v1/BiRefNet-general-epoch_244.pth", model_path)

birefnet = BiRefNet(bb_pretrained=False)
state_dict = torch.load(model_path, map_location=device)
state_dict = check_state_dict(state_dict)
birefnet.load_state_dict(state_dict)
birefnet.to(device)
birefnet.eval()
print("BiRefNet is ready to use.")

# Transformation 설정
transform_image = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 경로 설정
src_dir = './input'
person_only_dir = './person_only'
mask_dir = './mask'
background_only_dir = './background_only'
inpainting_dir = './inpainting_results'

# 디렉토리 생성
os.makedirs(person_only_dir, exist_ok=True)
os.makedirs(mask_dir, exist_ok=True)
os.makedirs(background_only_dir, exist_ok=True)
os.makedirs(inpainting_dir, exist_ok=True)

# Helper 함수
def resize_and_compress_image(image_path, output_path, max_pixels=9437184, quality=85):
    with Image.open(image_path) as img:
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        width, height = img.size
        total_pixels = width * height
        if total_pixels > max_pixels:
            scaling_factor = (max_pixels / total_pixels) ** 0.5
            img = img.resize((int(width * scaling_factor), int(height * scaling_factor)))
        img.save(output_path, format="JPEG", quality=quality)

def compress_mask_image(mask_path, output_path, max_pixels=9437184):
    with Image.open(mask_path) as mask:
        if mask.mode in ('RGBA', 'RGB', 'P'):
            mask = mask.convert('L')
        width, height = mask.size
        total_pixels = width * height
        if total_pixels > max_pixels:
            scaling_factor = (max_pixels / total_pixels) ** 0.5
            mask = mask.resize((int(width * scaling_factor), int(height * scaling_factor)))
        mask.save(output_path, format="PNG", optimize=True)

def inpaint_image(image_path, mask_path, prompt, output_path, negative_prompt=None):
    temp_image_path = "temp_image.jpg"
    temp_mask_path = "temp_mask.png"
    resize_and_compress_image(image_path, temp_image_path)
    compress_mask_image(mask_path, temp_mask_path)
    
    # 요청 데이터 생성
    data = {
        "prompt": prompt,
        "output_format": "png",
    }
    if negative_prompt:
        data["negative_prompt"] = negative_prompt

    response = requests.post(
        API_URL,
        headers={
            "authorization": f"Bearer {API_KEY}",
            "accept": "image/*"
        },
        files={
            "image": open(temp_image_path, "rb"),
            "mask": open(temp_mask_path, "rb"),
        },
        data=data,
    )
    os.remove(temp_image_path)
    os.remove(temp_mask_path)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Inpainting successful. Result saved at: {output_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 전체 파이프라인 실행
start_time = time.time()
image_paths = glob(os.path.join(src_dir, '*'))

for image_path in image_paths:
    print(f"Processing {image_path}...")
    image = Image.open(image_path).convert("RGB")
    input_images = transform_image(image).unsqueeze(0).to(device)

    with torch.no_grad():
        preds = birefnet(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()

    pred_pil = transforms.ToPILImage()(pred).convert("L")
    pred_pil = pred_pil.resize(image.size)

    image_masked = refine_foreground(image, pred_pil)
    image_masked.putalpha(pred_pil)

    # Segmentation 결과 저장
    person_save_path = os.path.join(person_only_dir, f"person_{os.path.splitext(os.path.basename(image_path))[0]}.png")
    mask_save_path = os.path.join(mask_dir, f"mask_{os.path.splitext(os.path.basename(image_path))[0]}.png")
    background_save_path = os.path.join(background_only_dir, f"background_{os.path.splitext(os.path.basename(image_path))[0]}.png")
    image_masked.save(person_save_path)
    pred_pil.save(mask_save_path)
    background_image = image.copy()
    inverted_mask = Image.eval(pred_pil, lambda x: 255 - x)
    background_image.putalpha(inverted_mask)
    background_image.save(background_save_path)

    # Inpainting
    inpaint_save_path = os.path.join(inpainting_dir, f"inpainting_{os.path.splitext(os.path.basename(image_path))[0]}.png")
    inpaint_image(
        image_path=image_path,
        mask_path=mask_save_path,
        prompt="inpaint natural background",
        negative_prompt= "human, person, people, body",
        output_path=inpaint_save_path
    )

end_time = time.time()
print(f"Pipeline complete. Total time taken: {end_time - start_time:.2f} seconds.")
