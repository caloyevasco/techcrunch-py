from dataclasses import dataclass

@dataclass(frozen=True)
class Selector:
    tag: str
    class_name: str
    
    def to_bs_kwargs(self):
        return {'name': self.tag, 'class_': self.class_name}
