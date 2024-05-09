#!/usr/bin/python3
import lang
import lang.syntax
import lang.visitor
import lang.exec as exec
import argparse as ap


parser = ap.ArgumentParser(description="Run the blang interpreter")
# args[1] is the file to run
parser.add_argument("file", nargs="?", help="The file to run")
parser.add_argument(
    "-d", "--dump_json", action="store_true", help="Dump the AST tree to a json file"
)
args = parser.parse_args()

if args.file:
    code = open(args.file, "r").read()
    code += "\n"
else:
    exit()

asttree = lang.syntax.parser.parse(code)
if args.dump_json:
    open("astTree.json", "w").write(asttree.to_json())

# optimize the tree (do some simple const expr folding)
optimizer = lang.visitor.Optimizer()
asttree = optimizer.visit(asttree)
if args.dump_json:
    open("astTreeOptimized.json", "w").write(asttree.to_json())

# run the interpreter
interpreter = exec.Interpreter()

interpreter.visit(asttree)
if args.dump_json:
    open("astTreeExecuted.json", "w").write(asttree.to_json())
