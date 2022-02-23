class Gate:
    def __init__(self):
        self.index=None
        self.type=None
        self.qlist=[]
        self.angle=0
        self.target = -1
        self.control = -1

    def __repr__(self) -> str:
        return f'Gate No.{self.index}, type:{self.type}, qlist:{self.qlist}'

    def __eq__(self, other):
        if self.type == other.type and \
           self.qlist == other.qlist and \
            self.angle == other.angle and \
            self.target == other.target and \
            self.control == other.control and \
            self.index == other.index:
            return True
        else:
            return False