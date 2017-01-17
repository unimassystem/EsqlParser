# lextab.py. This file automatically created by PLY (version 3.9). Don't edit!
_tabversion   = '3.8'
_lextokens    = set(('EXPLAIN', 'ORDER', 'IN', 'NUMBER', 'COMMA', 'LIMIT', 'WITH', 'AND', 'INTO', 'DELETE', 'CREATE', 'BULK', 'OR', 'WORD', 'DROP', 'QUOTE_STRING', 'TABLE', 'WHERE', 'NOT', 'AS', 'META', 'COMPARE_TYPE', 'ASC', 'GROUP', 'TO', 'DESC', 'END_QUERY', 'DQUOTE_STRING', 'BETWEEN', 'UPDATE', 'LIKE', 'INSERT', 'UPSERT', 'SELECT', 'SET', 'BY', 'OPTION', 'FROM', 'VALUES'))
_lexreflags   = 0
_lexliterals  = '(){}@%.*[]:-^'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_WORD>[_a-zA-Z][a-zA-Z_0-9]*|[\\u4e00-\\u9fa5]+)|(?P<t_NUMBER>(\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]? \\d+)?)|(?P<t_QUOTE_STRING>\'[^\\\']*\')|(?P<t_DQUOTE_STRING>"[^\\"]*")|(?P<t_COMPARE_TYPE><>|\\!=|==|>=|<=|=>|=<|=|>|<)|(?P<t_END_QUERY>;)|(?P<t_COMMA>,)', [None, ('t_WORD', 'WORD'), ('t_NUMBER', 'NUMBER'), None, None, None, ('t_QUOTE_STRING', 'QUOTE_STRING'), ('t_DQUOTE_STRING', 'DQUOTE_STRING'), (None, 'COMPARE_TYPE'), (None, 'END_QUERY'), (None, 'COMMA')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
