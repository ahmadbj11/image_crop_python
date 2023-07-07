from flask import Flask, render_template, request
import cv2
import numpy as np
import os
import datetime

app = Flask(__name__)

def crop_by_position(img, position, size):
    height, width, _ = img.shape

    if position == 'top_left':
        return img[:size, :size]
    elif position == 'top_center':
        return img[:size, width//2 - size//2:width//2 + size//2]
    elif position == 'top_right':
        return img[:size, width - size:]
    elif position == 'center_left':
        return img[height//2 - size//2:height//2 + size//2, :size]
    elif position == 'center':
        return img[height//2 - size//2:height//2 + size//2, width//2 - size//2:width//2 + size//2]
    elif position == 'center_right':
        return img[height//2 - size//2:height//2 + size//2, width - size:]
    elif position == 'bottom_left':
        return img[height - size:, :size]
    elif position == 'bottom_center':
        return img[height - size:, width//2 - size//2:width//2 + size//2]
    elif position == 'bottom_right':
        return img[height - size:, width - size:]
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ambil gambar yang diunggah
        uploaded_file = request.files['image']
        img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # Ambil data dari form
        position = request.form['position']
        size = int(request.form['size'])

        # Validasi ukuran potongan tidak melebihi ukuran gambar
        if size > min(img.shape[0], img.shape[1]):
            return render_template('index.html', error_message='Ukuran potongan melebihi ukuran gambar yang diunggah.')

        # Memotong gambar
        cropped_img = crop_by_position(img, position, size)
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # Simpan gambar hasil potong
        folder_name = 'static/uploads'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            #simpan nama file dengan nama posisi dan waktu saat ini
        save_path = os.path.join(folder_name, f'{position}_{current_time}.jpg')
        cv2.imwrite(save_path, cropped_img)

        # Tampilkan gambar hasil potong
        return render_template('result.html', image_path=save_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()