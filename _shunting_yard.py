'''
	25.05.23
	Метод сортировочной станции.
'''


import math as m
# правильные функции очистки и токенизации. старый алгоритм вычисления

'''
	Словарь операций и их приоритетов, реализаций
	На данный момент в качестве реализаций операций взяты приватные методы класса float,
		это не очень хороший способ, но скорость вырастает. To-do: как нибудь поменять
'''

OPERATORS = {'+': (1, lambda x, y: float.__add__(x, y)), '-': (1, lambda x, y: float.__sub__(x, y)), 
			 '*': (2, lambda x, y: float.__mul__(x, y)), '/': (2, lambda x, y: float.__truediv__(x, y)),
			 '^': (3, lambda x, y: float.__pow__(x, y)), '//': (2, lambda x, y: float.__floordiv__(x, y)),
			 '%': (2, lambda x, y: float.__divmod__(x, y)), }


'''
	Функции и их реализации
	Представляют собой хэш, в котором в качестве ключей взяты токены соответствующие
		функциям, а значениями являются реализации этих функций, и колличество аргументов
'''
	
FUNCTIONS = {'exp': (1, lambda x: m.exp(x)), 'sin': (1, lambda x: m.sin(x)), 
			 'cos': (1, lambda x: m.cos(x)), 'sqrt': (1, lambda x: m.sqrt(x)),
			 'abs': (1, lambda x: abs(x)), }


'''
	Проверка на число
'''

def is_num(string):
	if '-' in string and (string[0] != '-' or len(string) == 1):
		return False
	for c in string:
		if c not in "1234567890.-":
			return False
	return True
	
	
'''
	Токенизатор, возвращает (status_code, tokens).
	status_code = 1 в случае успешной токенизации, tokens = [токены]
	status_code = 0 при обнаружении неизвестного символа, tokens = символ
'''

def tokenize(string):
	tokens = []
	buff = ''
	flag = None


	for c in string:
		
		if c in '0123456789.':
			if flag != 0:
				flag = 0
				if buff: tokens.append(buff)
				buff = c
			else:
				buff += c
		
		elif c.isalpha():
			if flag != 1:
				flag = 1
				if buff: tokens.append(buff)
				buff = c
			else:
				buff += c
		
		elif c in '+-*/^%()':
			if flag != 2:
				if buff: tokens.append(buff)
				tokens.append(c)
				flag = 2
				buff = ''
			else:
				tokens.append(c)
		
		elif c != ' ':
			return (0, c)
			
	if flag in (0, 1):
		tokens.append(buff)
		
	return (1, tokens)


'''
	Подготовка списка токенов, убираем лишние операнды:
'''

def purifier(tokens):
	ops_ex_m = ['+', '*', '/', '^', '/', '//', '%']
	err_cases = (
				'+*', '+/', '+%', '+^', '+//', 
				'-*', '-/', '-%', '-^', '-//',
				'*/', '*%', '*^', '*//',
				'/*', '/%', '/^', '///',
				'%*', '%/', '%%', '%^', '%//',
				'^*', '^/', '^%', '^^', '^//',
				'//*', '//%', '//^', '////'
				)
	add_cases = {'++', '-+', '*+', '/+', '%+', '^+', '//+', '(+'}
	min_cases = ['+-', '*-', '/-', '%-', '^-', '//-'] # без --	
	
	if tokens[0] in ops_ex_m: return (0, tokens[0])
	
	for i in range(len(tokens)-1): # ищем ошибки
		t = ''.join(tokens[i:i+2])
		if t in err_cases:
			return (0, t)

	flag = 1
	while flag: # исправляем двойные операнды, операции замены на другие операции
		flag = 0 
		for i in range(len(tokens)-1):
			t = ''.join(tokens[i:i+2])
			if t == '--':
				flag = 1
				tokens.pop(i)
				tokens[i] = '+'
			elif t == '**':
				flag = 1
				tokens.pop(i)
				tokens[i] = '^'
			elif t == '//':
				flag = 1
				tokens.pop(i)
				tokens[i] = '//'
	print(tokens)
	flag=1
	while flag: # исправляем вычитание
		flag = 0
		for i in range(len(tokens)-1):
			t = ''.join(tokens[i:i+2])
			if t in min_cases:
				flag = 1
				tokens.pop(i+1)
				tokens.insert(i+1, '*')
				tokens.insert(i+1, '-1')
				
	flag = 1
	while flag: # исправляем сложение
		flag = 0
		for i in range(len(tokens)-1):
			t = ''.join(tokens[i:i+2])
			if t in add_cases:
				flag = 1
				tokens.pop(i+1)
				
	if tokens[0] in ops_ex_m: tokens.pop(0)	# убираем первый ненужный токен
	
	if tokens[0] == '-' and is_num(tokens[1]):
		tokens.pop(0)
		tokens[0] = '-'+tokens[0]
		
	flag = 1
	while flag:
		flag = 0
		for i in range(len(tokens)-2):
			if tokens[i] + tokens[i+1] == '(-':
				tokens[i+2] = '-' + tokens[i+2]
				tokens.pop(i+1)
	
	return tokens


def sh_yard(prd_str):
	d_stack = []  # стек для чисел
	op_stack = []  # стек для операций и скобок
	
	for token in prd_str:
		
		if is_num(token):
			d_stack.append(float(token)) # число в стек

		elif token in FUNCTIONS:
			op_stack.append(token) # функцию в стек

		elif token in OPERATORS:
			while op_stack and op_stack[-1] != '(' and OPERATORS[token][0] <= OPERATORS[op_stack[-1]][0]:
				y, x = d_stack.pop(), d_stack.pop()
				d_stack.append(OPERATORS[op_stack.pop()][1](x, y))
			op_stack.append(token)

		elif token == '(':
			op_stack.append(token)
			
		elif token == ')':
			while op_stack[-1] != '(':
				y, x = d_stack.pop(), d_stack.pop()
				d_stack.append(OPERATORS[op_stack.pop()][1](x, y))
			op_stack.pop()
			
			if op_stack and op_stack[-1] in FUNCTIONS:  # блок вычисления функций, пока только одной переменной.
				f = op_stack.pop()
				arg = d_stack.pop()
				# print(f, arg)
				d_stack.append(FUNCTIONS[f][1](arg))
		print(d_stack, op_stack)

	while op_stack:
		y, x = d_stack.pop(), d_stack.pop()
		d_stack.append(OPERATORS[op_stack.pop()][1](x, y))
		
	return (d_stack, op_stack)


while True:
	print(40*'-')
	tokenized_str = tokenize(input())[1]
	print('tokenizer: ', tokenized_str)
	purified_str = purifier(tokenized_str)
	print('purifier: ', purified_str)
	print('Шаги алгоритма сортировочной станции: ')

	result = sh_yard(purified_str)
	print('Результат: ', result)
