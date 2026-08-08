import ast
import sys


try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass


try:
    import gmpy2
except ImportError:
    gmpy2 = None


USE_GMPY2 = gmpy2 is not None
BIGINT = gmpy2.mpz if USE_GMPY2 else int
FULL_DISPLAY = "--full" in sys.argv or "-f" in sys.argv
MAX_FULL_DISPLAY_DIGITS = 80
STEP_WIDTH = 8


def format_number(number):
    if FULL_DISPLAY:
        return str(number)

    if USE_GMPY2:
        digits = gmpy2.num_digits(number, 10)
        if digits <= MAX_FULL_DISPLAY_DIGITS:
            return str(number)
        return f"{digits} digits"

    digits = int(number.bit_length() * 0.3010299956639812) + 1
    if digits <= MAX_FULL_DISPLAY_DIGITS:
        return str(number)
    return f"{digits} digits"


def print_hailstone_sequence(start):
    current = start
    step = 0
    max_value = current
    write = sys.stdout.write
    fmt = format_number

    write("\n开始验证：\n")
    write(f"[{step:0{STEP_WIDTH}d}] 起始 = {fmt(current)}\n")

    while current != 1:
        if current & 1:
            current = current * 3 + 1
            operation = "*3+1 -> "
        else:
            current >>= 1
            operation = "/2 -> "

        step += 1
        if current > max_value:
            max_value = current
        write(f"[{step:0{STEP_WIDTH}d}] {operation}{fmt(current)}\n")

    write("\n验证结束，最终到达 1。\n")
    write(f"总步数：{step}\n")
    write(f"过程中出现的最大值：{fmt(max_value)}\n")


def evaluate_integer_expression(node):
    if isinstance(node, ast.Expression):
        return evaluate_integer_expression(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, int):
            raise ValueError
        return BIGINT(node.value)

    if isinstance(node, ast.UnaryOp):
        value = evaluate_integer_expression(node.operand)
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
        raise ValueError

    if isinstance(node, ast.BinOp):
        left = evaluate_integer_expression(node.left)
        right = evaluate_integer_expression(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Pow):
            if right < 0:
                raise ValueError
            return left**right

    raise ValueError


def parse_positive_integer(user_input):
    text = user_input.replace(" ", "").replace("^", "**")
    if not text:
        raise ValueError

    try:
        expression = ast.parse(text, mode="eval")
    except SyntaxError:
        raise ValueError

    return evaluate_integer_expression(expression)


def read_positive_integer():
    while True:
        user_input = input("请输入正整数表达式，例如 2^100001-1（输入 q 退出）：").strip()

        if user_input.lower() == "q":
            return None

        try:
            number = parse_positive_integer(user_input)
        except ValueError:
            print("输入错误：只支持整数、+、-、*、^、** 和括号。")
            continue
        except MemoryError:
            print("输入错误：这个数太大，当前电脑内存不够计算。")
            continue

        if number <= 0:
            print("输入错误：请输入大于 0 的正整数。")
            continue

        return number


def main():
    print("冰雹猜想验证程序")
    print("规则：偶数除以 2，奇数乘以 3 再加 1。\n")
    if USE_GMPY2:
        print("大数默认极速显示；输入 --full 可看完整数字（会慢很多）。")
    print("支持输入：27、2^100001、2^100001-1、(3+5)*7。")

    while True:
        number = read_positive_integer()
        if number is None:
            break

        print_hailstone_sequence(number)
        print()

    print("\n程序已退出。")
    input("按回车键关闭窗口...")


if __name__ == "__main__":
    main()
