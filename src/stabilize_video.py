"""
Импортируем модуль subprocess для выполнения команд командной строки.
"""
import subprocess

def stabilize_video(input_path, output_path, shakiness, smoothing):
    """
    Стабилизирует видео по заданному пути.

    :param input_path: путь к исходному видеофайлу
    :param output_path: путь к выходному стабилизированному видеофайлу
    """

    # обнаружение движения
    detect_command = f"ffmpeg -i {input_path} -vf vidstabdetect=shakiness={shakiness}:accuracy={15} -f null -"
    subprocess.run(detect_command, shell=True)

    # стабилизация
    stabilize_command = f"ffmpeg -y -i {input_path} -vf vidstabtransform=smoothing={smoothing}:input=transforms.trf -c:v libx264 -preset slow -crf 18 {output_path}"
    subprocess.run(stabilize_command, shell=True)
