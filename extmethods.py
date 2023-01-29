from entities import seg, Line, RLM
import itertools as it
import varbank as vb


def seg_index(X, Y):
    try:
        return seg.index(str(Line(X, Y)))
    except ValueError:
        return None


def send(string):  # Функция, которая будет выводить факт пользователю, в случае успешного применения.
    print(string)


# потенциально, если мы вызваем метод для Line с тремя точками и больше, то он выведет сумму отрезков? Но measure устанавливает однозначную длину!
def measure(name, value):
    n = seg.index(name)
    RLM[n][n] = value


def str_list(lst):
    return [str(x) for x in lst]


def gen_predicates_dict(pure_predicates):
    titles = [x.ttl for x in pure_predicates]
    d = dict.fromkeys(titles)
    for k in d.keys():
        d[k] = []
    for t in d.keys():
        for p in pure_predicates:
            if p.ttl == t:
                d[t] += [p]
            else:
                continue
    return d


def add_string(database, lst):
    database.loc[len(database.index)] = lst

def pprint_dict(my_dict):
    print({str(x): y for x, y in zip(my_dict.keys(), my_dict.values())})

def find_fact(df, fact_name):
    return df['Факт'][df['Факт'] == fact_name].index[0]


def gen_comb(num,
             pure_points):  # [x for x in it.product(pure_points, repeat=num) if all([False for m in list(Counter(x).values()) if m > 2])]
    lst = [[y for y in it.permutations(x, len(x))] for x in it.combinations(pure_points, num)]
    return list(it.chain(*lst))


def transitive_predicates(pure_predicates):  # словарь сделан, но ты от него отказался
    for p in it.combinations(pure_predicates, 2):
        if p[0].ttl in ['eql', 'prl', 'ort'] and p[1].ttl in ['eql', 'prl', 'ort']:
            p[0] * p[1]
    # Для правильной работы col и cyl.

    for ln in it.combinations(vb.lines, 2):  # Опасная фигня, но починил.
        ln[0].intersect(ln[1])
    for ln in it.combinations(vb.circ_lines, 2):
        ln[0].intersect(ln[1])
    return 0


def gen_only_right_perm(pr):
    return [pr.__class__(*y) for y in it.permutations(pr.lst) if pr.__class__(*y) == pr]


def stringify(list):
    return ''.join(str_list(list))
