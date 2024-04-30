import lang
import lang.token
import lang.visitor
import lang.exec as exec
import sys



code = open(sys.argv[1], 'r').read()
code += '\n'

optimizer = lang.visitor.Optimizer()
interpreter = exec.Interpreter()
asttree = lang.token.parser.parse(code)
open('astTree.json', 'w').write(asttree.to_json())

# run the interpreter
interpreter.visit(asttree)

