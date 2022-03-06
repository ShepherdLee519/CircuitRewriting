class Edge:
    def __init__(self,source,target,label):
        self.source=source
        self.target=target
        self.label=label

    def __repr__(self) -> str:
        return f'Edge: [{self.source} -> {self.target} / label: {self.label}]'


    def __hash__(self) -> int:
        return self.source * 1000000 + self.target * 10000 + self.label

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

    def intersect(self, other):
        if self.source == other.source or \
            self.source == other.target or \
            self.target == other.source or \
            self.target == other.target:
            return True
        else:
            return False