from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'input')
RESULT_FOLDER = os.path.join(os.getcwd(), 'inpainting_results')
PERSON_FOLDER = os.path.join(os.getcwd(), 'person_only')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(PERSON_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or request.files['image'].filename == '':
        return render_template('index.html', error="No image file provided")

    file = request.files['image']
    if not allowed_file(file.filename):
        return render_template('index.html', error="Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")

    # 파일 저장
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # main.py 실행
        subprocess.run(['python', os.path.join(os.getcwd(), 'main.py')], check=True)

        # 결과 파일 이름 추론
        result_filename = f"inpainting_{os.path.splitext(filename)[0]}.png"
        return redirect(url_for('result', filename=result_filename))
    except subprocess.CalledProcessError as e:
        return render_template('index.html', error=f"Error during processing: {e.stderr}")

@app.route('/result/<filename>')
def result(filename):
    result_path = os.path.join(RESULT_FOLDER, filename)
    if not os.path.exists(result_path):
        return render_template('result.html', error="Processed file not found")
    return render_template('result.html', filename=filename)

@app.route('/inpainting_results/<filename>')
def serve_result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

@app.route('/input/<filename>')
def serve_input_image(filename):
    safe_filename = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, safe_filename)

@app.route('/editor/<bg_filename>/<person_filename>')
def editor(bg_filename, person_filename):
    return render_template('editor.html', bg_filename=bg_filename, person_filename=person_filename)

def is_valid_image_data(image_data):
    try:
        img_data = base64.b64decode(image_data.split(',')[1])
        Image.open(BytesIO(img_data))
        return True
    except Exception as e:
        return False

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json['image']
    if not is_valid_image_data(data):
        return jsonify({'error': 'Invalid image data'}), 400

    img_data = base64.b64decode(data.split(',')[1])
    img = Image.open(BytesIO(img_data))

    # 이미지 저장 경로 설정
    output_path = './merged_output.png'
    img.save(output_path)
    
    return jsonify({'message': 'Image saved successfully!', 'path': output_path})

@app.route('/person_only/<filename>')
def serve_person_image(filename):
    safe_filename = secure_filename(filename)
    return send_from_directory(PERSON_FOLDER, safe_filename)

@app.route('/view_images')
def view_images():
    # 원본 이미지 경로에서 파일 목록 가져오기
    input_images = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if allowed_file(f)
    ]

    # 병합된 결과 이미지 경로 설정
    merged_output = os.path.join(os.getcwd(), 'merged_output.png')
    merged_output_exists = os.path.exists(merged_output)
    
    return render_template(
        'view_images.html',
        input_images=input_images,
        merged_output='merged_output.png' if merged_output_exists else None
    )

@app.route('/merged_output.png')
def serve_merged_output():
    output_path = os.path.join(os.getcwd(), 'merged_output.png')
    if os.path.exists(output_path):
        return send_from_directory(os.getcwd(), 'merged_output.png')
    else:
        return jsonify({'error': 'Merged output not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
