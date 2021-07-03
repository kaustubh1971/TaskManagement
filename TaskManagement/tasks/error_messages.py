
class Message():
    # todo, assign the values meaningfully in slabs of 10s, 20s, 30s,
    CODE_MAP = {
            1 : '{} id not found',
            2 : 'Invalid status',
            3 : '{} already exists for {}',
            4 : 'missing',
            5 : 'not needed',
            6 : 'No data found for page number {}',
            7 : 'Invalid {}',
            10 : 'Something went wrong',
            101: 'Read Successful',
            102: 'Update Successful',
            103: 'Create Successful',
            104: 'Deleted Successfully',

    }

    @classmethod
    def code(cls, code):
        return cls.CODE_MAP.get(code, 'Unknown')