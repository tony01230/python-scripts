"""
  tl; dr: asks you to convert a random decimal into binary or hex. says if you are correct or not.
"""
from random import randint
def generate_binary(number):
    if number == 0:
        return 0
    else:
        return number % 2 + 10 * generate_binary(int(number // 2))

def generate_hex(number):
    hex = ["0","1","2","3","4","5","6","7","8","9",'A','B','C','D','E','F']
    if number == 0:
        return ""
    return generate_hex(number // 16) + hex[number % 16]

def generate_problem(difficulty):
    decimal = randint(0, ((difficulty + 1) * 1000 / 3))
    if randint(0,1):
        result = generate_hex(decimal)
        mode = "Hex"
    else:
        result = generate_binary(decimal)
        mode = "Binary"

    x = False
    print("Convert Decimal " + str(decimal) + " to " + mode)
    while x != True:
        if input("Answer: ") == str(result):
            if input("Correct, Continue? (\"\" or \"No\") ") == "": generate_problem(difficulty)
            else: x = True
        else:
            if input("Incorrect, Try Again? (\"\" or \"No\") ") == "No": x = True

difficulty = input("Easy, Medium or Hard? Word Please: ")
difficulties = ["Easy", "Medium", "Hard"]
while difficulty not in difficulties:
    print("Incorrect Option.")
    difficulty = input("What Difficulty? *(Easy, Medium or Hard): ")
generate_problem(difficulty)
