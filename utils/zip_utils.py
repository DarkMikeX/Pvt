import os
import zipfile
import logging

logger = logging.getLogger(__name__)

def zip_files(file_paths, output_zip):
    """
    Zip multiple files into a single archive file.
    Returns output_zip path on success or None on failure.
    """
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file in file_paths:
                archive.write(file, os.path.basename(file))
        logger.info(f"Created zip archive: {output_zip}")
        return output_zip
    except Exception as e:
        logger.error(f"Failed to create zip archive: {e}")
        return None
