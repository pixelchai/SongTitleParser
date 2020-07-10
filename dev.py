from lark import Lark

parser = Lark("title.lark", parser="earley")

print(parser.parse("Hi mate"))
