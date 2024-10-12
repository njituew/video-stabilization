import subprocess

def converting_video(input_path, conv_path):
    """
    Конвертирует видео в формат MP4 с помощью ffmpeg.

    :param input_path: Путь к исходному видеофайлу.
    :param mp4_output_path: Путь для сохранения сконвертированного видеофайла в формате MP4.
    """

    # Создаем список аргументов
    conversion_command = [
        'ffmpeg',
        '-y', '-i',
        input_path, conv_path
    ]

    # Выполняем команду
    subprocess.run(conversion_command)
