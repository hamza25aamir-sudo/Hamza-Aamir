grocery_list = {}
try:
    while True:
        item = input().upper
        if item in grocery_list:
            grocery_list[item] += 1 
        else:
            grocery_list[item] = 1
except EOFError:
    print()
for item in sorted(grocery_list):
    print(grocery_list[item], item)

