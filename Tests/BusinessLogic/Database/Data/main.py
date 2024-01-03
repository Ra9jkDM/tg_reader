

class Data:
    def create(self):
        self._create_data()

    def _save(self, db, obj: list):
        for i in obj:
            db.add(i)
        db.commit()

    def _create_data(self, db):
        raise Exception("Need to create data in this func")