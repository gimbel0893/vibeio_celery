import celery
import tempfile
import zipfile
import os
import shutil


@celery.task()
def create_zip(source_dir, zip_name, include_empty_dir=True):
    zip_full_path += os.sep.join(tempfile.mkdtemp(), zip_name)
    empty_dirs = []
    zip = zipfile.ZipFile(zip_full_path, 'w', zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(source_dir))

    for root, dirs, files in os.walk(source_dir): 
        archive_root = os.path.abspath(root)[root_len:]
        empty_dirs.extend([dir for dir in dirs if os.listdir(os.path.join(root, dir)) == []])

        for name in files:
            fullpath = os.path.join(root, name)
            archive_name = os.path.join(archive_root, name)
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)

        if include_empty_dir:
            for dir in empty_dirs:
                archive_name = os.path.join(archive_root[1:], dir)
                zip_info = zipfile.ZipInfo(archive_name + os.sep)
                zip.writestr(zip_info, "")

        empty_dirs = []

    zip.close()
    shutil.rmtree(source_dir)

    return zip_full_path
