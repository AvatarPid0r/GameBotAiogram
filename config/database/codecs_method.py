import codecs
import os


async def open(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'base', file_name)
    with codecs.open(file_path, 'r', 'utf-8') as file:
        value = eval(str(file.readline()))
        file.close()

    return value


async def write(file_name, source):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'base', file_name)
    with codecs.open(str(file_path), 'w', 'utf-8') as file:
        value = file.write(str(source))
        file.close()

    return value
