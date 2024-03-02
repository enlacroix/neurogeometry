
ALL_TYPES = [
    'POINT',
    'Line',
    'NUMBER',
    'DICT',
    'Angle',
    'Relation',
    'LIST',
]

ALLOWED_COMMANDS = {
    'Line': {
        'arg-0': ['POINT'],
        'amount': 'ANY',
    },
    'Angle': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'Ratio': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'LinAngle.quick': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'cyl': {
        'arg-0': ['POINT'],
        'amount': 'ANY',
    },
    '_col_': {
        'arg-0': ['POINT'],
        'amount': 'ANY',
    },
    'citer': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'inter': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'mdp': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'cir': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'prl': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'eql': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'ort': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'ORT': {
        'arg-0': ['Line', 'Line'],
        'amount': '1',
    },
    'PRL': {
        'arg-0': ['Line', 'Line'],
        'amount': '1',
    },
    'ELA': {
        'arg-0': ['ANGLE', 'Angle'],
        'amount': '1',
    },
    'eqa': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'etr': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'ctr': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'eqr': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'Relation': {
        'arg-0': ['Line', 'Line', 'NUMBER'],
        'arg-1': ['Angle', 'Angle', 'NUMBER'],
        'arg-2': ['Relation', 'Relation', 'NUMBER'],
        'amount': '3',
    },
    'LinearCombination': {
        'arg-0': ['DICT'],
        'amount': 'ANY',
    },
    'SetValue': {
        'arg-0': ['Line', 'NUMBER'],
        'arg-1': ['Angle', 'NUMBER'],
        'arg-2': ['Relation', 'NUMBER'],
        'amount': '3',
    },
    'Sum': {
        'arg-0': ['LIST', 'NUMBER'],
        'amount': '1',
    },
    'Triangle': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'IsoTriangle': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'OrtTriangle': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'DescribedTriangle': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'Circle': {
        'arg-0': ['POINT'],
        'amount': 'ANY',
    },
    'InscribedCircle': {
        'arg-0': ['POINT'],
        'amount': 'ANY',
    },
    'Bisect': {
        'arg-0': ['POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
    'Quadrangle': {
        'arg-0': ['POINT', 'POINT', 'POINT', 'POINT'],
        'amount': '1',
    },
}

ALLOWED_NAMES = set([
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z'
])


WRONG_AMOUNT_PARAMS = 'WRONG_AMOUNT_PARAMS'
UNKNOWN_COMMAND = 'UNKNOWN_COMMAND'
WRONG_TYPE_PARAM = 'WRONG_TYPE_PARAM'
LOST_BRACKET = 'LOST_BRACKET'


def error_dict(where: str = '', command: str = '', typeof: str = '', correction: str = '') -> dict:
    return {
        'where': where,
        'command': command,
        'typeof': typeof,
        'correction': correction,
    }


def check_dict(str_: str) -> bool:
    if str_[0] != '{' and str_[len(str_) - 1] != '}':
        return False
    arr = str_.split(':')
    if len(arr) != 2:
        return False
    if not check_command(arr[0]) and not arr[0].isdigit() and arr[0] not in ALLOWED_NAMES or not arr[1].isdigit():
        return False
    return True


def check_definite_command(str_: str, expected_: str) -> bool:
    if not len(str_):
        return False
    s, e = str_.find('('), len(str_) - 1
    if s == -1 or str_[e] != ')' or s + 1 == e:
        return False
    return str_[:s] == expected_ and check_command(str_)


def split_command(str_: str) -> list:
    if str_.find('(') == -1:
        return str_.split(',')
    s, num = 0, 0
    arr = []
    for i in range(len(str_)):
        if str_[i] == ',' and num == 0:
            if len(str_[s:i]) == 0:
                return ['ERROR']
            arr.append(str_[s:i])
            s = i + 1
            continue
        if str_[i] == '(':
            num += 1
        if str_[i] == ')':
            if num - 1 < 0:
                return ['ERROR']
            num -= 1
    arr.append(str_[s:len(str_)])
    if len(arr[len(arr) - 1]) == 0 or num != 0:
        return ['ERROR']
    return arr


def check_list(str_: str) -> bool:
    if not len(str_):
        return False
    if str_[0] != '(' or str_[-1] != ')':
        return False
    str_ = str_[1:-1]
    arr = split_command(str_)
    num = 0
    for type_ in ALL_TYPES:
        for arg in arr:
            print(arg, type_)
            if not check_definite_command(arg, type_):
                num += 1
                break
    print(num, len(ALL_TYPES))
    return num < len(ALL_TYPES)


def check_arg(real_: str, expected_: str) -> bool:
    if expected_ == 'POINT':
        return real_ in ALLOWED_NAMES
    if expected_ == 'DICT':
        return check_dict(real_)
    if expected_ == 'LIST':
        return check_list(real_)
    if expected_ == 'NUMBER':
        return real_.isdigit()
    return check_definite_command(real_, expected_)


def check_command(str_: str) -> dict:
    if not len(str_):
        return error_dict()
    s, e = str_.find('('), len(str_) - 1
    if s == -1 or str_[e] != ')':
        return error_dict(command=str_, typeof=LOST_BRACKET)
    if str_[:s] not in ALLOWED_COMMANDS:
        return error_dict(command=str_[:s], typeof=UNKNOWN_COMMAND)
    if s + 1 == e:
        return error_dict(command=str_, typeof=WRONG_AMOUNT_PARAMS,
                          correction=str(len(ALLOWED_COMMANDS[str_[:s]]['arg-0'])))

    arr = split_command(str_[s + 1:e])

    print(arr)

    if ALLOWED_COMMANDS[str_[:s]]['amount'] != 'ANY':
        amount = 0
        for i in range(int(ALLOWED_COMMANDS[str_[:s]]['amount'])):
            if len(arr) != len(ALLOWED_COMMANDS[str_[:s]]['arg-' + str(i)]):
                amount += 1
        if amount == int(ALLOWED_COMMANDS[str_[:s]]['amount']):
            return error_dict(command=str_[:s], typeof=WRONG_AMOUNT_PARAMS,
                              correction=str(len(ALLOWED_COMMANDS[str_[:s]]['arg-0'])))
        amount = 0
        last_wrong_arg = ''
        for i in range(int(ALLOWED_COMMANDS[str_[:s]]['amount'])):
            if len(arr) != len(ALLOWED_COMMANDS[str_[:s]]['arg-' + str(i)]):
                amount += 1
                continue
            num = 0
            for j in range(len(ALLOWED_COMMANDS[str_[:s]]['arg-' + str(i)])):
                ans = check_arg(arr[j], ALLOWED_COMMANDS[str_[:s]]['arg-' + str(i)][j])
                if ans:
                    num += 1
                else:
                    last_wrong_arg = arr[j]
            if num != len(ALLOWED_COMMANDS[str_[:s]]['arg-' + str(i)]):
                amount += 1
        if amount == int(ALLOWED_COMMANDS[str_[:s]]['amount']):
            return error_dict(command=str_[:s], typeof=WRONG_TYPE_PARAM, correction=last_wrong_arg)
    else:
        for arg in arr:
            if not check_arg(arg, ALLOWED_COMMANDS[str_[:s]]['arg-0'][0]):
                return error_dict(command=str_[:s], typeof=WRONG_TYPE_PARAM, correction=arg)
    return error_dict()


def check_syntax(str_: str) -> dict:
    str_ = str_.replace(' ', '').replace('\t', '').replace('\n', '')
    for word in str_.split(';'):
        response = check_command(word)
        if response != error_dict():
            return response
    return error_dict()


def check_linear_obj(str_: str) -> dict:
    if not len(str_):
        return error_dict()
    if str_[0] != '[' or str_[len(str_) - 1] != ']':
        return error_dict(command=str_, typeof=LOST_BRACKET)
    inside = str_[1:len(str_) - 1]
    if len(inside) == 1 and inside in ALLOWED_NAMES:
        return error_dict()
    arr = inside.split(',')
    if len(arr) != 2:
        return error_dict(command=str_, typeof=WRONG_AMOUNT_PARAMS, correction='2')
    if len(arr[0]) != 2 and arr[0][0] not in ALLOWED_NAMES and \
            arr[0][1] not in ALLOWED_NAMES:
        return error_dict(command=str_, typeof=WRONG_TYPE_PARAM, correction=arr[0])
    if len(arr[1]) != 2 and arr[1][0] not in ALLOWED_NAMES and \
            arr[1][1] not in ALLOWED_NAMES:
        return error_dict(command=str_, typeof=WRONG_TYPE_PARAM, correction=arr[1])
    return error_dict()


def check_syntax_linear_angles(str_: str) -> dict:
    str_ = str_.replace(' ', '').replace('\t', '').replace('\n', '')
    print('linear angles: ', str_)
    for obj in str_.split(';'):
        print(obj)
        response = check_linear_obj(obj)
        if response != error_dict():
            print(response)
            return response
    return error_dict()
