# import time
from .syntax import check_syntax, check_syntax_linear_angles, error_dict
import sys
sys.path.append(sys.path[0] + '..\\..\\algorithm')
# sys.path.append('home/proga/nproject/algorithm')
from deductive.solver import run_solver
from educational.recommend import formRecommends
from tskmanager import Task
from backwardLA.strategy import LAReductor
import config as cf


UNKNOWN_RUNTIME_ERROR = 'UNKNOWN_RUNTIME_ERROR'
MISSING_KEYS_IN_THE_REQUEST = 'MISSING_KEYS_IN_THE_REQUEST'
EMPTY_CONDITION = 'EMPTY_CONDITION'
SYNTAX_ERROR_IN_THE_CONDITION = 'SYNTAX_ERROR_IN_THE_CONDITION'
EMPTY_QUESTION = 'EMPTY_QUESTION'
SYNTAX_ERROR_IN_THE_QUESTION = 'SYNTAX_ERROR_IN_THE_QUESTION'
EMPTY_LINEAR_ANGLES = 'EMPTY_LINEAR_ANGLES'
SYNTAX_ERROR_IN_THE_LINEAR_ANGLES = 'SYNTAX_ERROR_IN_THE_LINEAR_ANGLES'

LIMIT_HINTS_AMOUNT = (1, 10)
LIMIT_VARIABLES_LIMIT = (10, 200)
LIMIT_MAX_ITER_AMOUNT = (5, 15)


def get_empty_dict() -> dict:
    return {
        'task_data': {
            'answer': '',
            'answer_full': '',
            'error_message': UNKNOWN_RUNTIME_ERROR,
            'error_dict': error_dict()
        },
    }


def check_int(some_) -> bool:
    if isinstance(some_, int):
        return True
    if isinstance(some_, str):
        if some_.isdigit():
            return True
    return False


def check_keys(data_: dict) -> bool:
    if 'task_data' not in data_ or 'settings' not in data_:
        return False
    if not isinstance(data_['task_data'], dict) or not isinstance(data_['settings'], dict):
        return False
    if 'condition' not in data_['task_data'] or \
            'question' not in data_['task_data'] or \
            'linear_angles' not in data_['task_data']:
        return False
    if not isinstance(data_['task_data']['condition'], str) or \
            not isinstance(data_['task_data']['question'], str) or \
            not isinstance(data_['task_data']['linear_angles'], str):
        return False
    if 'is_full_searching' not in data_['settings'] or \
            'variables_limit' not in data_['settings'] or \
            'max_iter_amount' not in data_['settings'] or \
            'use_linear_angle_method' not in data_['settings'] or \
            'beta' not in data_['settings'] or \
            'hints_amount' not in data_['settings']:
        return False
    if not isinstance(data_['settings']['is_full_searching'], bool) or \
            not isinstance(data_['settings']['use_linear_angle_method'], bool) or \
            not isinstance(data_['settings']['beta'], bool):
        return False
    if not check_int(data_['settings']['variables_limit']) or \
            not check_int(data_['settings']['max_iter_amount']) or \
            not check_int(data_['settings']['hints_amount']):
        return False

    c_variables_limit = int(data_['settings']['variables_limit'])
    c_max_iter_amount = int(data_['settings']['max_iter_amount'])
    c_hints_amount = int(data_['settings']['hints_amount'])
    if not (LIMIT_VARIABLES_LIMIT[0] <= c_variables_limit <= LIMIT_VARIABLES_LIMIT[1]) or \
            not (LIMIT_MAX_ITER_AMOUNT[0] <= c_max_iter_amount <= LIMIT_MAX_ITER_AMOUNT[1]) or \
            not (LIMIT_HINTS_AMOUNT[0] <= c_hints_amount <= LIMIT_HINTS_AMOUNT[1]):
        return False
    return True


def set_settings(settings_: dict):
    # conf = open('/home/proga/nproject/algorithm/config.py', 'w')
    # conf = open('..\\config.py', 'w')
    # conf.write('from collections import namedtuple\n')
    # conf.write("evalMode = namedtuple('EvalMode', ['angle', 'segment', 'ratio', 'square'])\n\n")
    #
    # conf.write('FULL_EXPLORATION = ' + str(settings_['is_full_searching']) + '\n')
    # conf.write('FUN = False\n')
    # conf.write('MAX_ITERS = ' + str(settings_['max_iter_amount']) + '\n')
    # conf.write('DEVMODE = False\n')
    # conf.write('VARIABLE_LIMIT = ' + str(int(settings_['variables_limit']) + 1) + '\n')
    # conf.write('WRITE_DOWN_DF_TO_CSV = False\n')
    # conf.write('EVALUATION_MODE = evalMode(angle=True, segment=True, ratio=True, square=False)\n')
    # conf.write('CHAOS_MOD = False\n')
    # conf.write('BETA = ' + str(settings_['beta']) + '\n')
    # conf.write('HOWMANYHINTS = ' + str(settings_['hints_amount']) + '\n')
    #
    # conf.close()
    cf.FULL_EXPLORATION = settings_['is_full_searching']
    cf.VARIABLE_LIMIT = int(settings_['variables_limit']) + 1
    cf.MAX_ITERS = int(settings_['max_iter_amount'])
    cf.BETA = settings_['beta']
    cf.HOWMANYHINTS = int(settings_['hints_amount'])
    cf.FUN = True
    cf.DEVMODE = False


def to_algorithm(data_: dict) -> dict:
    print(data_)
    response = get_empty_dict()

    if not check_keys(data_):
        response['task_data']['error_message'] = MISSING_KEYS_IN_THE_REQUEST
        return response

    if not len(data_['task_data']['condition'].replace(' ', '').replace('\t', '').replace('\n', '')):
        response['task_data']['error_message'] = EMPTY_CONDITION
        return response

    syntax_error_dict = check_syntax(data_['task_data']['condition'])
    if syntax_error_dict != error_dict():
        response['task_data']['error_message'] = SYNTAX_ERROR_IN_THE_CONDITION
        syntax_error_dict['where'] = 'CONDITION'
        response['task_data']['error_dict'] = syntax_error_dict
        return response

    if not len(data_['task_data']['question'].replace(' ', '').replace('\t', '').replace('\n', '')):
        response['task_data']['error_message'] = EMPTY_QUESTION
        return response

    syntax_error_dict = check_syntax(data_['task_data']['question'])
    if syntax_error_dict != error_dict():
        response['task_data']['error_message'] = SYNTAX_ERROR_IN_THE_QUESTION
        syntax_error_dict['where'] = 'QUESTION'
        response['task_data']['error_dict'] = syntax_error_dict
        return response

    if not len(data_['task_data']['linear_angles'].replace(' ', '').replace('\t', '').replace('\n', '')) and \
            data_['settings']['use_linear_angle_method']:
        response['task_data']['error_message'] = EMPTY_LINEAR_ANGLES
        return response

    syntax_error_dict = check_syntax_linear_angles(data_['task_data']['linear_angles'])
    if data_['settings']['use_linear_angle_method'] and \
            syntax_error_dict != error_dict():
        response['task_data']['error_message'] = SYNTAX_ERROR_IN_THE_LINEAR_ANGLES
        syntax_error_dict['where'] = 'LINEAR_ANGLES'
        response['task_data']['error_dict'] = syntax_error_dict
        return response

    data_['task_data']['condition'] = data_['task_data']['condition'].replace(',', ', ').strip(';').replace(';', '; ')
    data_['task_data']['question'] = data_['task_data']['question'].replace(',', ', ').strip(';').replace(';', '; ')
    data_['task_data']['linear_angles'] = data_['task_data']['linear_angles']\
        .replace(',', ', ').strip(';').replace(';', '; ')

    set_settings(data_['settings'])
    try:
        response['task_data']['answer_full'] = \
            run_solver((data_['task_data']['condition'], data_['task_data']['question']))
        if data_['settings']['use_linear_angle_method']:
            print('INSIDE LINEAR ANGLES')
            LAReductor(data_['task_data']['linear_angles'])
            response['task_data']['answer_full'] += '<br>' + Task.Instance().getLAProof()
        print(response['task_data']['answer_full'])
        response['task_data']['answer'] = formRecommends()
        print(formRecommends())
    except Exception:
        return get_empty_dict()

    response['task_data']['error_message'] = ''
    return response
