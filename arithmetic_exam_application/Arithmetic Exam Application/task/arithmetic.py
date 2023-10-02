import random
from collections import OrderedDict

levels = OrderedDict(
    {1: "simple operations with numbers 2-9", 2: "integral squares of 11-29"}
)


def get_difficulty_level():
    incorrect_format = True
    while incorrect_format:
        print("Which level do you want? Enter a number:")
        for key, value in levels.items():
            print(f"{key} - {value}")
        level = int(input())
        if 0 < level < 3:
            return level
        else:
            print("Incorrect format.")


def generate_task(level):
    if level == 1:
        return generate_simple_task()
    elif level == 2:
        return generate_square_task()


def generate_simple_task():
    # generate random operator and operands
    max_int = 9
    op = random.choice(["+", "-", "*"])
    op1 = random.randint(2, max_int)
    op2 = random.randint(2, max_int)
    # calculate result
    result = 0
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
    }
    if op in operations:
        result = operations[op](op1, op2)
    else:
        print("Operation {} is not supported".format(op))
    # print task string to console
    task = " ".join([str(op1), op, str(op2)])
    print(task)
    return result


def generate_square_task():
    lower_bound, upper_bound = 11, 29
    num_int = random.randint(lower_bound, upper_bound)
    print(num_int)
    result = num_int * num_int
    return result


def check_answer(result):
    incorrect_format = True
    while incorrect_format:
        try:
            answer = int(input())
            if answer == result:
                print("Right!")
                return 1
            else:
                print("Wrong!")
                return 0
        except ValueError:
            print("Incorrect format.")


def main():
    # perform examination
    level = get_difficulty_level()
    num_tasks = 5
    correct_answers = 0
    for i in range(0, num_tasks):
        result = generate_task(level)
        correct_answers += check_answer(result)
    print(f"Your mark is {correct_answers}/{num_tasks}.")

    # save results from examination
    print("Would you like to save your result to the file? Enter yes or no.")
    save_to_file = input()
    if save_to_file in ["yes", "YES", "y", "Yes"]:
        user_name = input("What is your name?\n")
        filename = "results.txt"
        file = open(filename, mode="at", encoding="utf-8")
        file.write(
            f"{user_name}: {correct_answers}/{num_tasks} in level {level} ({levels[level]})\n"
        )
        file.close()
        print(f"The results are saved in {filename}.")
    else:
        print("Exit program without saving results!")


main()
