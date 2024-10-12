def allowed_file(filename):
    """
    Проверяет, является ли расширение файла допустимым.

    :param filename: имя файла
    :return: True, если расширение допустимо, иначе False
    """
    
    # Определяем множество допустимых расширений файлов.
    ALLOWED_EXTENSIONS = {
    'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'mpeg', 'mpg', 'm4v', '3gp',
    'mts', 'm2ts', 'vob', 'asf', 'qt', 'rm', 'rmvb', 'divx', 'xvid', 'ogg', 'drc', 
    'nsv', 'f4v', 'h261', 'h263', 'h264', 'hevc', 'vp8', 'vp9', 'mjpeg'
    }


    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
