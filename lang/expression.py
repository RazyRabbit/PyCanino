class Catcher:
    def __init__(self, *rules):
        self.values = tuple(filter(lambda r: type(r) is not type, rules))
        self.types = tuple(filter(lambda r: type(r) is type, rules))
    
    def __call__(self, values):
        return self.catch(values)
    
    def __repr__(self):
        return f'{type(self).__name__} {self.types or self.values}'
    
    def catch(self, values):
        for value in values:
            if self.can_catch(value):
                yield value
            else:
                return
        
        return

    def can_catch(self, value):
        tvalue = type(value)

        if tvalue in self.types:
            return tvalue
        elif value in self.values:
            return value
            
        return any in self.values
    
    @classmethod
    def apply(cls, items):
        return tuple((cls(*item[1:]) if type(item) is tuple and item[0] is ... else item) for item in items)

class Expression:
    def __init__(self, *rules):
        self.rules = Catcher.apply(rules)
    
    def __call__(self, symbols):
        return self.match(symbols)
    
    def __repr__(self):
        return f'{type(self).__name__} {self.rules}'
    
    def match(self, symbols):
        if len(parsed := self.parse(symbols)) == len(self.rules):
            return parsed
        
        return
    
    def parse(self, symbols):
        acumulator = []
        
        def _(index, acumulator=[]):
            for rule in self.rules:
                if type(rule) is Catcher:
                    acumulator.clear()

                    for symbol in rule.catch(symbols[index:]):
                        if symbol in self.rules:
                            break

                        acumulator.append(symbol)
                        index += 1
                        
                    yield tuple(acumulator)
                    continue

                elif self.match_rule(rule, symbols[index]):
                    yield symbols[index]

                else:
                    raise IndexError

                index += 1
        
        try:
            for symbol in _(0):
                acumulator.append(symbol)
        except IndexError:
            return tuple(acumulator)

        return tuple(acumulator)
    
    @classmethod
    def match_rule(cls, rule, symbol):
        tsymbol = type(symbol)
        trule = type(rule)

        if trule is tuple:
            return sum(cls.match_rule(r, symbol) for r in rule)
        elif trule is type:
            return tsymbol is rule

        return rule is any or rule == symbol
    
    @classmethod
    def apply(cls, items):
        return {name: cls(*rules) for name, rules in items}