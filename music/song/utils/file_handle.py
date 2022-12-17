def save_audio_file_into_folder(temp_audio_file, path_to_folder, file_name):
    destination = open(path_to_folder + '/' + file_name, 'wb+')
    for chunk in temp_audio_file.chunks():
        destination.write(chunk)
    destination.close()
