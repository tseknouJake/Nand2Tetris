class JackTokenizer:

    KEYWORD = 0
    SYMBOL = 1
    INT_CONST = 2
    STRING_CONST = 3
    IDENTIFIER = 4

    symbols = '{}()[].,;+-*/&|<>=~'
    keywords = [
        "class", "constructor", "function", "method", "static", "field",
        "var", "int", "char", "boolean", "void", "true", "false", "null", "this",
        "let", "do", "if", "else", "while", "return"
    ]

    def __init__(self, input_file):
        with open(input_file, "r") as file:
            self.lines = file.readlines()
        self.clear_comments()
        self.tokens = self.tokenize()
        self.currentTokenIndex = -1
        self.token_type = None

    def clear_comments(self):
        # Simplified comment removal (does not handle inline comments after code or multiline comments perfectly)
        self.lines = [line.split('//')[0].strip() for line in self.lines
                      if not line.strip().startswith('//')
                      and not line.strip().startswith('/*')]

    def tokenize(self):
        tokens = []
        for line in self.lines:
            # Splitting by space to get tokens, this is a simplification
            tokens += line.split()
        return tokens

    def hasMoreTokens(self):
        return self.currentTokenIndex < len(self.tokens) - 1

    def advance(self):
        if self.hasMoreTokens():
            self.currentTokenIndex += 1
            self._currentToken = self.tokens[self.currentTokenIndex]
            self.token_type = self._determineTokenType(self._currentToken)

    def _determineTokenType(self, token):
        if token in self.keywords:
            return self.KEYWORD
        elif token in self.symbols:
            return self.SYMBOL
        elif token.isdigit():
            return self.INT_CONST
        elif token.startswith('"') and token.endswith('"'):
            return self.STRING_CONST
        else:
            return self.IDENTIFIER

    def tokenType(self):
        return self.token_type

    def keyWord(self):
        if self.token_type == self.KEYWORD:
            return self._currentToken

    def symbol(self):
        if self.token_type == self.SYMBOL:
            return self._currentToken

    def identifier(self):
        if self.token_type == self.IDENTIFIER:
            return self._currentToken

    def intVal(self):
        if self.token_type == self.INT_CONST:
            return int(self._currentToken)

    def stringVal(self):
        if self.token_type == self.STRING_CONST:
        # Removing quotes from string constants
            return self._currentToken.strip('"')



# class JackTokenizer:
    
#     def __init__(self, input_file):
#         pass

#     def clear_comments(self):
#         pass

#     def hasMoreTokens(self):
#         pass

#     def advance(self):
#         pass

#     def tokenType(self):
#         pass

#     def keyWord(self):
#         pass

#     def symbol(self):
#         pass

#     def identifier(self):
#         pass

#     def intVal(self):
#         pass

#     def stringVal(self):
#         pass