class Name:
    name = None
    
    def __init__(self, symbol: str):
        self.symbol = symbol
    
    def __iter__(self): return iter(self.symbol)
    def __hash__(self): return hash(self.symbol)
    def __len__(self): return len(self.symbol)
    def __int__(self): return int(self.symbol)
    def __str__(self): return str(self.symbol)

    def __neq__(self, value): return self.symbol != value
    def __eq__(self, value): return self.symbol == value

    def __repr__(self):
        return f'{type(self).__name__}: {repr(self.symbol)}'
    
    @classmethod
    def apply(cls, items):
        return {item: cls(item) for item in items}

class Keyword(Name):
    "just an aliase to reserved words"

class Token(Name):
    def __init__(self, name: str, symbol: str):
        self.symbol = symbol
        self.name = name
    
    def __repr__(self):
        return f'{type(self).__name__}: {self.name}'
    
    @classmethod
    def apply(cls, items): 
        return {name: cls(name, symbol) for name, symbol in items}
    
class Tokenizer:
    def __init__(self, keywords, **tokens):
        self.keywords = Keyword.apply(keywords)
        self.tokens = Token.apply(tokens.items())

    def __call__(self, string):
        return self.tokenize(string)
    
    def search(self, string):
        for token in sorted(self.tokens.values(), key=len, reverse=True):
            if string.startswith(str(token)):
                return token
        
        return

    def tokenize(self, string):
        length = len(string)

        def _cast(name):
            if name.isnumeric():
                return int(name)
            elif keyword := self.keywords.get(name):
                return keyword

            return Name(name)

        def _(begin, index):
            while index < length:
                if token := self.search(string[index:]):
                    yield _cast(string[begin:index])
                    yield token

                    index += len(token)
                    begin = index
                else:
                    index += 1
            
            yield _cast(string[begin:index])

        return tuple(filter(lambda symbol: symbol not in (None, ''), _(0, 0)))