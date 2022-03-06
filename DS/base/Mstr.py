class M_:

    def __init__(self, Mstr, Msem):
        self.Mstr=list(Mstr)
        self.Msem = [[] for i in range(2)]
    
    def __repr__(self) -> str:
        return f'Mstr mstr: {self.Mstr}, msem: {self.Msem}'
