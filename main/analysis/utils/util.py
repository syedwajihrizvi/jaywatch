def get_list_from_numbered_list(numbered_list):
    next = 2
    i = numbered_list.index("1.") + 2
    industry = ""
    res = []

    while i < len(numbered_list):
        if numbered_list[i] != str(next):
            industry += numbered_list[i]
        else:
            res.append(industry.lstrip().rstrip())
            industry = ""
            next += 1
            i += 1
        i += 1
    print(res)
    return res


def get_value_from_object(object, key, type):
    v = object.get(key)
    return v.get(type) if v else v


def percentage_difference(x, y):
    return ((x-y)/y)*100


def percentage_change(a1):
    return [percentage_difference(x, y) for x, y in list(zip(a1, a1[1:]))]


def get_year(date):
    return int(date[:4])


def get_month(date):
    return int(date[5:7])


def get_day(date):
    return int(date[8:])
