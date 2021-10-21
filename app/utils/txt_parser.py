import os
import shutil
import sys
import zipfile


class TxtParser:
    @staticmethod
    def __unpack_zipfile(name):
        with zipfile.ZipFile('app/static/dataset/dataset.zip') as archive:
            for entry in archive.infolist():
                current_name = entry.filename.encode('cp437').decode('utf-8')

                if current_name != name:
                    continue

                target = os.path.join(r'app/static/dataset', *current_name.split('/'))
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if not entry.is_dir():
                    with archive.open(entry) as source, open(target, 'wb') as dest:
                        shutil.copyfileobj(source, dest)

    @staticmethod
    def get_text(doc_id):
        TxtParser.__unpack_zipfile(doc_id)
        path = 'app/static/dataset/' + doc_id
        with open(path, encoding='utf-8') as f:
            return f.read()
