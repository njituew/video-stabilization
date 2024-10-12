"""
Импортируем необходимые библиотеки и функции.
"""
import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from src.stabilize_video import stabilize_video
from src.utils import allowed_file
from src.converting_mp4 import converting_video

"""
Создаем экземпляр Flask-приложения.
"""
app = Flask(__name__)

"""
Устанавливаем пути для загрузки и сохранения файлов.
"""
UPLOAD_FOLDER = 'static/uploads'
STABILIZED_FOLDER = 'static/stabilized'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STABILIZED_FOLDER'] = STABILIZED_FOLDER

"""
Определяем маршруты для различных функций.
"""
@app.route('/')
def index():
    """
    Главная страница приложения.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Обрабатывает POST-запросы на '/upload'. Проверяет наличие файла и его допустимый формат,
    сохраняет его и стабилизирует, после чего перенаправляет на страницу 'preview'.
    Если входной файл не в mp4 - он конвертируется в него и отправляется на 'preview'
    как stabilized_filename_mp4, чтобы браузер смог его воспроизвести.
    Отстабилизированный файл пользовательского формата отправляется как 
    stabilized_filename, чтобы его можно было скачать в неконвертированном виде.
    """
    file = request.files.get('file')

    # Проверка имени и формата файла
    if not file.filename == '' and allowed_file(file.filename):
        input_filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        output_filename = 'stabilized_' + input_filename
        output_path = os.path.join(app.config['STABILIZED_FOLDER'], output_filename)
        output_filename_mp4 = output_filename

        # Стабилизация видео
        shakiness = int(request.form.get('shakiness', 10))
        smoothing = int(request.form.get('smoothing', 30))
        stabilize_video(input_path, output_path, shakiness, smoothing)

        # Если входной и соответственно отстабилизированный файлы не в mp4 -
        # - они конвертируется в него
        if not input_filename.lower().endswith('.mp4'):
            mp4_input_path = os.path.splitext(input_path)[0] + '_converted.mp4'
            mp4_output_path = os.path.splitext(output_path)[0] + '_converted.mp4'
            
            converting_video(input_path, mp4_input_path)
            converting_video(output_path, mp4_output_path)
            
            # Удаление старого входного файла формата не mp4
            if os.path.exists(input_path):
                os.remove(input_path)
            
            input_filename = os.path.basename(mp4_input_path)
            output_filename_mp4 = os.path.basename(mp4_output_path)

        # Перенаправление на preview с передачей оригинального, стабилизированного и 
        # стабилизированного (формата mp4) файлов
        return redirect(url_for(
            'preview',
            original_filename=input_filename,
            stabilized_filename = output_filename,
            stabilized_filename_mp4=output_filename_mp4
        ))

    else:
        # Ошибка: неверный формат файла
        error_message = "Недопустимый формат файла."
        return render_template('index.html', error=error_message)

@app.route('/preview')
def preview():
    """
    Обрабатывает GET-запросы на '/preview'. Получает параметры 'original_filename' и 'stabilized_filename' из запроса.
    Если хотя бы один из параметров отсутствует, происходит перенаправление на страницу 'index'.
    Отображает страницу 'preview' с передачей оригинального и стабилизированных файлов.
    """
    original_filename = request.args.get('original_filename')
    stabilized_filename = request.args.get('stabilized_filename')
    stabilized_filename_mp4 = request.args.get('stabilized_filename_mp4')

    # Проверка наличия файлов
    if not original_filename or not stabilized_filename or not stabilized_filename_mp4:
        return redirect(url_for('index'))

    return render_template(
        'preview.html',
        original_filename=original_filename,
        stabilized_filename=stabilized_filename,
        stabilized_filename_mp4=stabilized_filename_mp4
    )

@app.route('/download/<filename>')
def download_file(filename):
    """
    Загружает стабилизированное видео.
    """
    return send_from_directory(app.config['STABILIZED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    """
    Создаем директории для загрузки и сохранения файлов, если они не существуют.
    Запускаем приложение.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(STABILIZED_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5500)
