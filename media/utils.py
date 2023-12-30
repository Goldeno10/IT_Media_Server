import magic

def categorize_file(file_path):
    """ Categorize a file based on its MIME type """
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)

    # Categorize based on file type
    if file_type.startswith('video'):
        return 'video'
    elif file_type.startswith('audio'):
        return 'audio'
    elif file_type.startswith('image'):
        return 'image'
    elif file_type.startswith('text'):
        return 'document'
    elif file_type.startswith('application/pdf'):
        return 'document'
    elif file_type.startswith('application/vnd'):
        return 'document'
    elif file_type.startswith('application/msword'):
        return 'document'
    else:
        return 'other'
