from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def simple_secure_filename(filename):
    # Removes dangerous characters and keeps only safe ones
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def convert_to_dots(image_path, width=100):
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Grayscale
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio * 0.5)
        img = img.resize((width, new_height))

        pixels = img.getdata()
        dot_art = ''
        for i in range(len(pixels)):
            dot_art += '.' if pixels[i] < 128 else ' '
            if (i + 1) % width == 0:
                dot_art += '\n'
        return dot_art
    except Exception as e:
        return f"Error processing image: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    art = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        if file.filename == '':
            return 'No selected file'
        filename = simple_secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        art = convert_to_dots(filepath)
        # Optionally, remove the file after processing
        try:
            os.remove(filepath)
        except Exception:
            pass
    return render_template('index.html', art=art)

if __name__ == '__main__':
    app.run(debug=True)