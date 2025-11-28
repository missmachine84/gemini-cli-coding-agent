import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output

def main():
    if len(sys.argv) < 2:
        print("Error: You must provide an expression as a command line argument.")
        print('Example: uv run calculator/main.py "3 + 5"')
        sys.exit(1)

    expression = sys.argv[1]
    calc = Calculator()

    try:
        result = calc.evaluate(expression)
        to_print = format_json_output(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
