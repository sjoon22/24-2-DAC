import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageMergerUI:
    def __init__(self, root, background_path, person_path, output_path, max_size=(800, 600)):
        self.root = root
        self.root.title("Image Merger UI")

        # 경로 설정
        self.background_path = background_path
        self.person_path = person_path
        self.output_path = output_path

        # 이미지 로드 및 크기 조정
        self.bg_image = Image.open(self.background_path).convert("RGBA")
        self.person_image = Image.open(self.person_path).convert("RGBA")

        self.scale_factor = min(max_size[0] / self.bg_image.width, max_size[1] / self.bg_image.height, 1.0)
        self.bg_image_resized = self.bg_image.resize(
            (int(self.bg_image.width * self.scale_factor), int(self.bg_image.height * self.scale_factor)),
            Image.Resampling.LANCZOS  # ANTIALIAS 대신 Resampling.LANCZOS 사용
        )
        self.person_image_resized = self.person_image.resize(
            (int(self.person_image.width * self.scale_factor), int(self.person_image.height * self.scale_factor)),
            Image.Resampling.LANCZOS  # ANTIALIAS 대신 Resampling.LANCZOS 사용
        )

        # Tkinter 이미지 변환
        self.bg_tk = ImageTk.PhotoImage(self.bg_image_resized)
        self.person_tk = ImageTk.PhotoImage(self.person_image_resized)

        # Canvas 생성 및 스크롤 추가
        self.canvas = tk.Canvas(root, width=max_size[0], height=max_size[1], scrollregion=(0, 0, self.bg_image_resized.width, self.bg_image_resized.height))
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 스크롤바 추가
        hbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        vbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        # 배경 이미지 추가
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_tk)

        # 인물 이미지 추가 (초기 위치)
        self.person_item = self.canvas.create_image(100, 100, anchor=tk.NW, image=self.person_tk)

        # 드래그 이벤트 바인딩
        self.canvas.tag_bind(self.person_item, "<Button1-Motion>", self.on_drag)

        # 저장 버튼
        self.save_button = tk.Button(root, text="Save Merged Image", command=self.save_image)
        self.save_button.pack()

    def on_drag(self, event):
        """
        마우스 드래그 이벤트로 인물 이미지를 이동.
        """
        # 드래그된 위치로 인물 이미지 이동
        self.canvas.coords(self.person_item, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def save_image(self):
        """
        현재 배치 상태로 이미지를 합성하고 저장.
        """
        # 현재 인물 이미지의 위치 가져오기
        x, y = self.canvas.coords(self.person_item)

        # 배경 복사
        merged_image = self.bg_image.copy()

        # 원래 이미지 크기로 위치 복원
        x = int(x / self.scale_factor)
        y = int(y / self.scale_factor)

        # 인물 이미지 붙이기
        person_resized_original = self.person_image.resize(
            (int(self.person_image.width), int(self.person_image.height)), Image.Resampling.LANCZOS
        )
        merged_image.paste(person_resized_original, (x, y), person_resized_original)

        # 저장
        merged_image.save(self.output_path, format="PNG")
        print(f"Merged image saved to {self.output_path}")

# 실행
if __name__ == "__main__":
    # 이미지 경로 설정
    background_path = "./inpainting_results/inpainting_1.png"  # 배경 이미지 경로
    person_path = "./person_only/person_1.png"                         # 인물 이미지 경로
    output_path = "./merged_output.png"                                # 저장 경로

    # Tkinter 창 실행
    root = tk.Tk()
    app = ImageMergerUI(root, background_path, person_path, output_path, max_size=(800, 600))  # 디스플레이 크기 제한
    root.mainloop()
