import random
from datetime import datetime
import math
from statistics import mean

def time_check(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args,**kwargs)
        print(datetime.now() - start_time)
        return result
    return wrapper

def generate_candidate(min_val=0,max_val=100):
    while True:
        yield random.randint(min_val,max_val)

def make_choice(num_of_candidates=100, ceil_round=False):
    candidates_stream = generate_candidate()
    best_value, current_best_value, choice = 0, 0, 0
    stop_value_float = num_of_candidates / math.exp(1)
    stop_num = math.ceil(stop_value_float) if ceil_round else math.floor(stop_value_float)

    # поиск лучшего кандидата из первых n / e
    for _ in range(0, stop_num):
        candidate = next(candidates_stream)
        if candidate > current_best_value:
            current_best_value = candidate
    best_value = current_best_value

    # выбор первого лучшего, чем лучший из первых n / e
    for _ in range(stop_num, num_of_candidates-1):
        candidate = next(candidates_stream)
        if not choice and candidate > current_best_value:
            choice = candidate
        if candidate > best_value:
            best_value = candidate

    # отдельно рассматриваем последнего
    last_candidate = next(candidates_stream)
    # выбираем его, если не выбрали до этого
    if not choice:
        choice = last_candidate
    # проверяем, является ли он самым лучшим из всего набора
    if last_candidate > best_value:
        best_value = last_candidate

    return {'choice':choice, 'best_candidate':best_value}



if __name__ == '__main__':
    num_of_tests = 1000
    expected_probability = 1 / math.exp(1)
    right_choice_counter_floor, right_choice_counter_ceil = 0, 0
    actual_probabilities_floor, actual_probabilities_ceil = [], []
    for _ in range(10):
        for _ in range(num_of_tests):
            choice_res_floor = make_choice()
            choice_res_ceil = make_choice(ceil_round=True)
            # print(choice_res)
            if choice_res_floor['choice'] == choice_res_floor['best_candidate']:
                right_choice_counter_floor += 1
            if choice_res_ceil['choice'] == choice_res_ceil['best_candidate']:
                right_choice_counter_ceil += 1
        actual_probabilities_floor.append(right_choice_counter_floor / num_of_tests)
        actual_probabilities_ceil.append(right_choice_counter_ceil / num_of_tests)
        right_choice_counter_floor, right_choice_counter_ceil = 0, 0

    print(f'expected probability: {expected_probability}')
    print(f'actual probability with down rounding: {actual_probabilities_floor}')
    print(f'mean value: {mean(actual_probabilities_floor)}')
    print(f'actual probability with up rounding: {actual_probabilities_ceil}')
    print(f'mean value: {mean(actual_probabilities_ceil)}')
