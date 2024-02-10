from JackTokenizer import JackTokenizer

class ComppilationEngine :
    
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.tokenizer = JackTokenizer(input_path)
        self.output = open(output_path, "w")
    
    def compileClass(self):
        self.output.write("<class>\n")
        self.tokenizer.advance()
        self.output.write("<keyword> class </keyword>\n")
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == JackTokenizer.KEYWORD and (self.tokenizer.keyWord() == "static" or self.tokenizer.keyWord() == "field"):
            self.compileClassVarDec()
        while self.tokenizer.tokenType() == JackTokenizer.KEYWORD and (self.tokenizer.keyWord() == "constructor" or self.tokenizer.keyWord() == "function" or self.tokenizer.keyWord() == "method"):
            self.compileSubroutine()
        self.output.write("<symbol> } </symbol>\n")
        self.output.write("</class>\n")
    
    def compileClassVarDec(self):
        self.output.write("<classVarDec>\n")
        self.output.write("<keyword> " + self.tokenizer.keyWord() + " </keyword>\n")
        self.tokenizer.advance()
        self.compileType()
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.output.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
            self.tokenizer.advance()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</classVarDec>\n")
        self.tokenizer.advance()
    
    def compileSubroutine(self):
        self.output.write("<subroutineDec>\n")
        self.output.write("<keyword> " + self.tokenizer.keyWord() + " </keyword>\n")
        self.tokenizer.advance()
        self.compileType()
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> ( </symbol>\n")
        self.compileParameterList()
        self.output.write("<symbol> ) </symbol>\n")
        self.compileSubroutineBody()
        self.output.write("</subroutineDec>\n")
    
    def compileSubroutineBody(self):
        self.output.write("<subroutineBody>\n")
        self.output.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        while self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "var":
            self.compileVarDec()
        self.compileStatements()
        self.output.write("<symbol> } </symbol>\n")
        self.output.write("</subroutineBody>\n")    
    
    def compileParameterList(self):
        self.output.write("<parameterList>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ")":
            self.output.write("</parameterList>\n")
            return
        self.compileType()
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.output.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            self.compileType()
            self.tokenizer.advance()
            self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
            self.tokenizer.advance()
        self.output.write("</parameterList>\n")
    
    def compileVarDec(self):
        self.output.write("<varDec>\n")
        self.output.write("<keyword> var </keyword>\n")
        self.tokenizer.advance()
        self.compileType()
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.output.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
            self.tokenizer.advance()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</varDec>\n")
        self.tokenizer.advance()
    
    def compileStatements(self):
        self.output.write("<statements>\n")
        while self.tokenizer.tokenType() == JackTokenizer.KEYWORD and (self.tokenizer.keyWord() in ["let", "if", "while", "do", "return"]):
            if self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "let":
                self.compileLet()
            elif self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "if":
                self.compileIf()
            elif self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "while":
                self.compileWhile()
            elif self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "do":
                self.compileDo()
            elif self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "return":
                self.compileReturn()
            else:
                break
        self.output.write("</statements>\n")
    
    def compileDo(self):
        self.output.write("<doStatement>\n")
        self.output.write("<keyword> do </keyword>\n")
        self.tokenizer.advance()
        self.compileSubroutineCall()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</doStatement>\n")
        self.tokenizer.advance()  # Consume the ";"
    
    def compileLet(self):
        self.output.write("<letStatement>\n")
        self.output.write("<keyword> let </keyword>\n")
        self.tokenizer.advance()
        self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            self.output.write("<symbol> [ </symbol>\n")
            self.tokenizer.advance()
            self.compileExpression()
            self.output.write("<symbol> ] </symbol>\n")
            self.tokenizer.advance()
        self.output.write("<symbol> = </symbol>\n")
        self.compileExpression()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</letStatement>\n")
        self.tokenizer.advance()
    
    def compileIf(self):
        self.output.write("<ifStatement>\n")
        self.output.write("<keyword> if </keyword>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> ( </symbol>\n")
        self.compileExpression()
        self.output.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> { </symbol>\n")
        self.compileStatements()
        self.output.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() == "else":
            self.output.write("<keyword> else </keyword>\n")
            self.tokenizer.advance()
            self.output.write("<symbol> { </symbol>\n")
            self.compileStatements()
            self.output.write("<symbol> } </symbol>\n")
            self.tokenizer.advance()
        self.output.write("</ifStatement>\n")
    
    def compileWhile(self):
        self.output.write("<whileStatement>\n")
        self.output.write("<keyword> while </keyword>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> ( </symbol>\n")
        self.compileExpression()
        self.output.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        self.output.write("<symbol> { </symbol>\n")
        self.compileStatements()
        self.output.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output.write("</whileStatement>\n")
    
    def compileDo(self):
        self.output.write("<doStatement>\n")
        self.output.write("<keyword> do </keyword>\n")
        self.tokenizer.advance()
        self.compileSubroutineCall()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</doStatement>\n")
        self.tokenizer.advance()
    
    def compileReturn(self):
        self.output.write("<returnStatement>\n")
        self.output.write("<keyword> return </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != JackTokenizer.SYMBOL or self.tokenizer.symbol() != ";":
            self.compileExpression()
        self.output.write("<symbol> ; </symbol>\n")
        self.output.write("</returnStatement>\n")
        self.tokenizer.advance()
    
    def compileExpression(self):
        self.output.write("<expression>\n")
        self.compileTerm()
        while self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.output.write("<symbol> " + self.tokenizer.symbol() + " </symbol>\n")
            self.tokenizer.advance()
            self.compileTerm()
        self.output.write("</expression>\n")
    
    def compileTerm(self):
        self.output.write("<term>\n")
        if self.tokenizer.tokenType() == JackTokenizer.INT_CONST:
            self.output.write("<integerConstant> " + str(self.tokenizer.intVal()) + " </integerConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == JackTokenizer.STRING_CONST:
            self.output.write("<stringConstant> " + self.tokenizer.stringVal() + " </stringConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == JackTokenizer.KEYWORD and self.tokenizer.keyWord() in ["true", "false", "null", "this"]:
            self.output.write("<keyword> " + self.tokenizer.keyWord() + " </keyword>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "(":
            self.output.write("<symbol> ( </symbol>\n")
            self.tokenizer.advance()
            self.compileExpression()
            self.output.write("<symbol> ) </symbol>\n")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() in ["-", "~"]:
            self.output.write("<symbol> " + self.tokenizer.symbol() + " </symbol>\n")
            self.tokenizer.advance()
            self.compileTerm()
        else:
            self.output.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "[":
                self.output.write("<symbol> [ </symbol>\n")
                self.tokenizer.advance()
                self.compileExpression()
                self.output.write("<symbol> ] </symbol>\n")
                self.tokenizer.advance()
            elif self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "(":
                self.compileSubroutineCall()
            elif self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ".":
                self.compileSubroutineCall()
        self.output.write("</term>\n")
    
    def compileExpressionList(self):
        self.output.write("<expressionList>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == ")":
            self.output.write("</expressionList>\n")
            return
        self.compileExpression()
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.output.write("<symbol> , </symbol>\n")
            self.compileExpression()
            self.tokenizer.advance()
        self.output.write("</expressionList>\n")