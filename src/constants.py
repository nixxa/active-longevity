# -*- coding: utf-8 -*-
import os


BASE_DIR=os.path.dirname(__file__)
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

IMAGE_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])
AUDIO_EXTENSIONS = set(['.m4a', '.wav', '.mp3', '.ogg', '.3gpp', '.mp4', '.amr', '.m4r'])
EXCEL_EXTENSIONS = set(['.xls', '.xlsx'])
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | AUDIO_EXTENSIONS | EXCEL_EXTENSIONS | set(['.pdf'])
