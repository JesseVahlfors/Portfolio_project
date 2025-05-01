from enum import StrEnum, auto
from typing import Any, List

class TokenType(StrEnum): 
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    EOF = auto()

class Token:
    def __init__(self, token_type: TokenType, value: Any):
        self.token_type = token_type
        self.value = value
    
    def __str__(self):
        return f"{self.token_type}: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Scanner:
    def __init__(self, json_string: str):
        self.json_string = json_string
        self.start = 0
        self.current_position = 0
        self.tokens: List[Token] = []
        self.line = 1
        self.current_depth = 0
       

    def increase_depth(self):
        MAX_DEPTH = 20
        self.current_depth += 1
        if self.current_depth >= MAX_DEPTH:
            raise Exception(f"Maximum depth exceeded. Maximum depth is 20. Current depth is at {self.current_depth} at line {self.line} and index {self.current_position}, token type: {self.tokens[self.current_position].token_type}")

    def decrease_depth(self):
        self.current_depth -= 1
        if self.current_depth < 0:
            raise Exception("Invalid JSON: Depth cannot be negative.")
        
    def scan_tokens(self) -> list[Token]:
        # Check that the string starts with a object or array
        if not self.is_at_end(): 
            first_char = self.json_string[0]
            if first_char != '{' and first_char != '[':
                raise Exception("Invalid JSON: JSON must start with an object or array.")
            
        while not self.is_at_end():
            self.start = self.current_position
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, None))
        self.current_position = 0
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.json_string)
    
    def scan_token(self):
        char = self.advance()
        match char:
            case '{':
                self.tokens.append(Token(TokenType.LBRACE, char))
            case '}':
                self.tokens.append(Token(TokenType.RBRACE, char))
            case '[':
                self.tokens.append(Token(TokenType.LBRACKET, char))
            case ']':
                self.tokens.append(Token(TokenType.RBRACKET, char))
            case ':':
                self.tokens.append(Token(TokenType.COLON, char))
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.add_string()
            case ',':
                self.tokens.append(Token(TokenType.COMMA, char))
            case ' ':
                pass
            case _:
                if char.isdigit() or char == '-':
                    self.add_number()
                elif char.isalpha():
                    self.add_keyword()
                else:
                    raise Exception(f"Unexpected character: {char} at line {self.line}.")

             
    def advance(self) -> str:
        char = self.json_string[self.current_position]
        self.current_position += 1
        return char
    
    def add_string(self):
        value = []
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\\':
                self.advance()
                if self.is_at_end():
                    raise Exception("Invalid JSON: Unexpected end of input in string.")
                escape_char = self.advance()
                if escape_char not in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u'):
                    raise Exception(f"Invalid JSON: Illegal backslash escape {escape_char} at line {self.line}.")
                if escape_char == 'u':
                    hex_digits = ""
                    for _ in range(4):
                        if self.is_at_end() or not self.peek().isalnum():
                            raise Exception("Invalid JSON: Invalid unicode escape sequence.")
                        hex_digits += self.advance()
                    try:
                        value.append(chr(int(hex_digits, 16)))
                    except ValueError:
                        raise Exception("Invalid JSON: Invalid unicode escape sequence.")
                else:
                    escape_map = {
                        '"': '"',
                        '\\': '\\',
                        '/': '/',
                        'b': '\b',
                        'f': '\f',
                        'n': '\n',
                        'r': '\r',
                        't': '\t'
                    }
                    value.append(escape_map[escape_char])
            else:
                char = self.advance()

                if ord(char) < 0x20:
                    raise Exception(f"Invalid JSON: Control character {repr(char)} at line {self.line}.")
                
                value.append(char)


        if self.is_at_end():
            raise Exception("Invalid JSON: Unexpected end of input in string.")
            
        self.advance() # consume closing quote
        self.tokens.append(Token(TokenType.STRING, ''.join(value)))
     
    def add_number(self):
        value = []
        value.append(self.json_string[self.current_position - 1]) # starting with the first digit

        # negative sign
        if value[0] == '-':
            if self.is_at_end() or not self.peek().isdigit():
                raise Exception(f"Invalid JSON: Unexpected character after '-' at line {self.line}.")
            value.append(self.advance())

        # leading zero check
        if value[-1] == '0':
            if not self.is_at_end() and self.peek().isdigit():
                raise Exception(f"Invalid JSON: Leading zeros in number at line {self.line}.")

        # integer part
        while not self.is_at_end() and self.peek().isdigit():
                value.append(self.advance())
        
        # decimal part
        if not self.is_at_end() and self.peek() == '.':
            value.append(self.advance())
            if self.is_at_end() or not self.peek().isdigit():
                raise Exception(f"Invalid JSON: Unexpected character after '.' at line {self.line}.")
            while not self.is_at_end() and self.peek().isdigit():
                value.append(self.advance())

        # exponent part
        if not self.is_at_end() and self.peek() in ('e', 'E'):
            value.append(self.advance())
            if not self.is_at_end() and self.peek() in ('+', '-'):
                value.append(self.advance())
            if self.is_at_end() or not self.peek().isdigit():
                raise Exception(f"Invalid JSON: Unexpected character after exponent at line {self.line}.")
            while not self.is_at_end() and self.peek().isdigit():
                value.append(self.advance())

        self.tokens.append(Token(TokenType.NUMBER, ''.join(value)))
       
    
    def add_keyword(self):
        # Get the keyword
        value = self.json_string[self.current_position - 1] # start with the first character
        while not self.is_at_end() and self.peek().isalnum():
            value += self.advance()

        # Check if it is valid
        keywords = {"true": True, "false": False, "null": None}    
        if value in keywords:
            token_type = TokenType.BOOLEAN if value in ("true", "false") else TokenType.NULL
            self.tokens.append(Token(token_type, keywords[value]))
        else:
            raise Exception(f"Unexpected keyword: {value} at line {self.line}. Keywords must be 'true', 'false', or 'null'.")
        

    def peek(self) -> str:
        if self.is_at_end():
            return "\0" # return null character
        return self.json_string[self.current_position]
