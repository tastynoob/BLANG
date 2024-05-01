# blang: A programming language designed by python-lex-yacc(ply)

###

you need to install ply package
```sh
apt install python3-ply
```

interpret and run a blang file 
```
python3 blang.py example/fibo.blang
```

dump AST tree
```
python3 blang.py example/fibo.blang -d
```