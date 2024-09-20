
# Media types
ENUM_MEDIA_TYPES = {
    "VIDEO": 1,
    "AUDIO": 2,
    "AUDIOVISUAL": 3,
    "SUBTITLE": 4,
}

# Import from image files or folders
ENUM_IMPORT_MODE = {
    "IMAGE_FILES": 1,
    "IMAGE_FOLDERS": 2, # image01, image02 => clip[01-02]
    "IMAGE_FOLDERS_ASSEMBLE": 3, # image01, image02 => clip[01-02]
}