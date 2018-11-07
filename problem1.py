import json

def solution(L):
    # write your code in Python 3.6
    splits = [str(v).split("@") for v in L]
    print(splits)
    email_dict = dict()
    ret_val = 0
    for lst in splits:
        if len(lst[0])>1 and lst[0].count("+"):
            nkey = lst[0][: lst[0].find("+")]
        else:
            nkey = lst[0]
        nkey = nkey.replace(".","")
        print(nkey)
        if lst[1] in email_dict:
            if nkey in email_dict[lst[1]]:
                email_dict[lst[1]][nkey] += 1
            else:
                email_dict[lst[1]][nkey] = 1
        else:
            email_dict[lst[1]] = dict()
            email_dict[lst[1]][nkey] = 1
        if email_dict[lst[1]][nkey] == 2:
            ret_val += 1
    print(L)
    print(json.dumps(email_dict, indent=4))
    return ret_val
        
    
    
if __name__ == "__main__":
    example = ['a.b@example.com', 'x@example.com', 'x@exa.mple.com', 'ab+1@example.com', 'y@example.com', 'y@example.com', 'y@example.com']
    solution(example)
