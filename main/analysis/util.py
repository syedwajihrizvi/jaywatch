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


# test_str = "Question: Can you give me the industris in a numbered list? Response: Certainly! Here's a numbered list of the specific industries in which Amazon can be classified: 1. E-commerce Retail 2. Technology 3. Cloud Computing 4. Media and Entertainment 5. Advertising 6. Logistics and Fulfillment 7. Membership Programs"

# get_list_from_numbered_list(test_str)
