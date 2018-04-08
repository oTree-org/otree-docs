def double(number):
    return number*2


def double_list(numbers):
    return [number*2 for number in numbers]

# equivalent to double_list,
# just a different style
def double_list_v2(numbers):
    new_list = []
    for number in numbers:
        new_list.append(number*2)
    return new_list


def filter_adult(people):
    return [p for p in people if p['age'] >= 18]


def names(people):
    return [p['name'] for p in people]


def sum_age_by_gender(people):
    age_sums = {'M': 0, 'F': 0}
    for p in people:
        gender = p['gender']
        age = p['age']
        age_sums[gender] += age
    return age_sums

# equivalent to sum_age_by_gender,
# just a different style
def sum_age_by_gender_v2(people):
    male_sum = 0
    female_sum = 0
    for p in people:
        if p['gender'] == 'M':
            male_sum += p['age']
        else:
            female_sum += p['age']
    return {'M': male_sum, 'F': female_sum}
