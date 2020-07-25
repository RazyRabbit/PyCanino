from .expression import Expression

class SyntaxTree:
    def __init__(self, name, parsed):
        self.parsed = parsed
        self.name = name
    
    def __getitem__(self, item): return self.parsed[item]
    def __iter__(self): return iter(self.parsed)
    def __hash__(self): return hash(self.name)
    def __len__(self): return len(self.parsed)
    def __str__(self): return str(self.name)

    def __neq__(self, value): return self.name != value
    def __eq__(self, value): return self.name == value
    
    def __repr__(self):
        return f'{self.name}: {self.parsed}'

class Parser:
    def __init__(self, cast=None, **expressions):
        self.expressions = Expression.apply(expressions.items())
        self.cast = cast

    def __call__(self, symbols):
        return self.parse(symbols)
    
    def __repr__(self):
        return f'{type(self).__name__} {self.expressions}'
    
    def search(self, symbols):
        for name, expression in self.expressions.items():
            if parsed := expression.match(symbols):
                return name, parsed
        
        return None, None
    
    def parse(self, symbols):
        length = len(symbols)

        def _(index, acumulator=[]):
            _cast = self.cast or (lambda tree: tree)

            while index < length:
                name, parsed = self.search(symbols[index:])

                if name:
                    yield from acumulator
                    yield _cast(SyntaxTree(name, parsed))

                    acumulator.clear()
                    index += self.lenghtof(parsed)
                else:
                    acumulator.append(symbols[index])
                    index += 1
            
            yield from acumulator

        return tuple(_(0))
    
    @classmethod
    def lenghtof(cls, symbols):
        result = 0

        for symbol in symbols:
            if type(symbol) is tuple:
                result += cls.lenghtof(symbol)
            else:
                result += 1
        
        return result