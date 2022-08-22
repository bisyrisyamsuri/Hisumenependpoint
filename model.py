from db import conn, select


class Data:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values):
        return select(query, values, self.mydb)