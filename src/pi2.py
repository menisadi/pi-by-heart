import os
import time
import mpmath
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

console = Console()

TITLE_TEXT = "The Pi Game!"


def _calculate_pi(num_digits):
    mpmath.mp.dps = num_digits + 2  # Set precision
    return str(mpmath.pi)[:-1]


def add_space_every_four_chars(input_string):
    # For demonstration, unchanged
    result = ""
    for i in range(0, len(input_string), 4):
        result += input_string[i : i + 4] + " "
    return result.strip()


def learn_digits(num_digits, delay=None):
    pi_digits = _calculate_pi(num_digits)
    pi_after_decimal_point = add_space_every_four_chars(pi_digits[2:])
    pi_digits = pi_digits[:2] + " " + pi_after_decimal_point

    console.print(Text("\nLearning digits of Pi...\n", style="bold cyan"))
    if delay:
        for digit in pi_digits:
            console.print(digit, end="", style="bold green")
            time.sleep(delay / 1000)
        console.print()  # new line
    else:
        console.print(Text(pi_digits, style="bold green"))


def score(corrections):
    # Simple scoring function
    hits_list = [int(c == " ") for c in corrections[2:]]
    base = 1
    multi = 1
    return sum(
        i**multi * h * base**i for i, h in enumerate(hits_list, start=2)
    ) + int(corrections[0] == " ")


def check(num):
    length_after_point = len(num) - 2
    true_pi = _calculate_pi(length_after_point)
    checked_digits = ""
    correction = ""

    # Use Rich for color-coding correctness
    for input_d, true_d in zip(num, true_pi):
        if input_d == true_d:
            checked_digits += f"[bold green]{input_d}[/bold green]"
            correction += " "
        else:
            checked_digits += f"[bold red]{input_d}[/bold red]"
            correction += true_d

    console.print(Text("Enter the digits you know:", style="bold underline"))
    console.print(checked_digits)  # Print the color-coded input
    console.print(Text(correction, style="italic dim"))

    correct_count = sum(1 for d in correction if d == " ")
    console.print(
        f"\nYou got [bold]{correct_count - 1}[/bold] out of [bold]{len(num) - 1}[/bold] right!"
    )
    console.print(f"Score: [bold magenta]{score(correction)}[/bold magenta]")


def test():
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Text(TITLE_TEXT, style="bold cyan"), justify="center")
    user_input = Prompt.ask("[bold]Enter the digits you know[/bold]")
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Text(TITLE_TEXT, style="bold cyan"), justify="center")
    check(user_input)


def learn():
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Text(TITLE_TEXT, style="bold cyan"), justify="center")
    num_digits = int(Prompt.ask("Enter the number of digits you want to learn"))
    input_delay = Prompt.ask(
        "Choose the delay in ms between digits or press Enter for 0", default="0"
    )
    delay = int(input_delay)

    learn_digits(num_digits, delay)


def help_info():
    console.print(
        """[bold cyan]
Welcome to The Pi Game!

In this game, you can choose to learn or test your knowledge of the digits of Pi.
To choose a mode, enter the corresponding number:

1. Learn: View a specified number of digits of Pi.
2. Test: Test your knowledge by testing the digits of Pi you remember.

You can exit the game at any time by choosing the 'Exit' option.
[/bold cyan]"""
    )


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        console.print(Text(TITLE_TEXT, style="bold cyan"), justify="center")
        console.print("[bold]Choose mode:[/bold]")
        console.print("1. Learn\n2. Test\n3. Help\n4. Exit")

        choice = Prompt.ask("Enter your choice")

        if choice == "1" or choice.lower() == "learn":
            learn()
        elif choice == "2" or choice.lower() == "test":
            test()
        elif choice == "3" or choice.lower() == "help":
            help_info()
        elif choice == "4" or choice.lower() == "exit" or choice.lower() == "q":
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        Prompt.ask("Press Enter to continue...")


if __name__ == "__main__":
    main()
