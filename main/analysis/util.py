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
