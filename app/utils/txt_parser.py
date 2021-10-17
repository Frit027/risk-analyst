class TxtParser:
    @staticmethod
    def f(doc_id):
        path = 'app/static/dataset/' + doc_id
        with open(path, encoding='utf-8') as f:
            return f.read()
