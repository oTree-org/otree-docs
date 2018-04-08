from . import quiz_solutions as q



people = [
    {'name': 'Alice', 'gender': 'F', 'age': 15},
    {'name': 'Bob', 'gender': 'M', 'age': 20},
    {'name': 'Claire', 'gender': 'F', 'age': 25},
    {'name': 'David', 'gender': 'M', 'age': 30},
    # etc....
]

assert q.double(10) == 20
assert q.double_list([1,2]) == [2, 4]
assert q.double_list_v2([1,2]) == [2, 4]
assert q.filter_adult(people) == [{'age': 20, 'gender': 'M', 'name': 'Bob'},
                                  {'age': 25, 'gender': 'F', 'name': 'Claire'},
                                  {'age': 30, 'gender': 'M', 'name': 'David'}]
assert q.names(people) == ['Alice', 'Bob', 'Claire', 'David']
assert q.sum_age_by_gender(people) == {'M': 50, 'F': 40}
assert q.sum_age_by_gender_v2(people) == {'M': 50, 'F': 40}
print('ok')