import os
import sys
import re

PREFIX = ["", "- ", " " * 4 + "- ", " " * 8 + "- ", " " * 12 + "- ", " " * 16 + "- ", " " * 20 + "- ",
          " " * 24 + "- ", " " * 28 + "- ", " " * 32 + "- ", " " * 36 + "- ", " " * 40 + "- ", ]

DOUBLE_SQUARE_BRACKET_PATTERN = r"\[\[(.*?)\]\]"
ALIAS_PATTERN = r"{{alias:\s*\[\[.*\]\]\s*(.*?)}}"
HIGHLIGHT_PATTERN = r"\^\^(.*?)\^\^"
ITALICS_PATTERN = r"__(.*?)__"

code_format = "inherit"


def alias(line):
    """提取alias文字出来"""
    res = re.findall(ALIAS_PATTERN, line)
    if not res:
        return line
    while len(res) > 0:
        line = re.sub(ALIAS_PATTERN, res[0], line, count=1)
        res = re.findall(ALIAS_PATTERN, line)
    return line


def remove_double_square_bracket(line):
    """删除双中括号"""
    res = re.findall(DOUBLE_SQUARE_BRACKET_PATTERN, line)
    if not res:
        return line
    while len(res) > 0:
        line = re.sub(DOUBLE_SQUARE_BRACKET_PATTERN, res[0], line, count=1)
        res = re.findall(DOUBLE_SQUARE_BRACKET_PATTERN, line)
    return line


def equation(line):
    """行间公式不替换，行内公式前后的$$换成$"""
    if len(line) <= 4:
        return line
    if line.startswith("$$") and line.endswith("$$"):
        # 若中间还存在$$说明不是行间公式
        if "$$" in line[2:-2]:
            return inline_equation(line)
        return line
    elif line.startswith('"$$') and line.endswith('$$"'):
        # 支持引用的行间公式
        if "$$" in line[3:-3]:
            return inline_equation(line)
        return line[1:-1]
    else:
        return inline_equation(line)


def inline_equation(line):
    """行内公式，把前后的$$换成$"""
    if line.find("$$") == -1:
        return line
    split_list = line.split("$$")
    # 只能匹配到奇数个$$
    if len(split_list) % 2 == 0:
        return line
    for i, item in enumerate(split_list):
        if i % 2 == 1 and item:
            split_list[i] = "$" + item + "$"
    return "".join(split_list)


def basic_inline_format(line, PATTERN, style_name):
    res = re.findall(PATTERN, line)
    if not res:
        return line
    while len(res) > 0:
        content = f'{style_name}{res[0]}{style_name}'
        line = re.sub(PATTERN, content, line, count=1)
        res = re.findall(PATTERN, line)
    return line


def highlight(line):
    """替换高亮"""
    return basic_inline_format(line, HIGHLIGHT_PATTERN, "==")


def italics(line):
    """"替换斜体"""
    return basic_inline_format(line, ITALICS_PATTERN, "*")


def split_prefix_content(line):
    """提取前缀，文字，级别"""
    for prefix in PREFIX[::-1]:
        if line.startswith(prefix):
            if len(prefix) == 0:
                level = 0
            else:
                level = (len(prefix) - 2) // 4 + 1
            return prefix, line[len(prefix):], level
    assert "Can't be here"


def main(file_path, level):
    output = ""
    prefix = ""
    current_level = 0
    add_header = ""
    multiline_code = False
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if not multiline_code:
                # 仅在非多行公式中更新前缀、行、等级
                # 若在多行公式内保持与之前一致
                prefix, line, current_level = split_prefix_content(line)
                if current_level == 0:
                    add_header = ""
                elif current_level <= level:
                    prefix = ""
                    add_header = "\n" + "#" * current_level + " "
                else:
                    add_header = ""
                    prefix = prefix[level * 4:]
                if prefix == "- ":
                    prefix = "\n- "
            if not line.strip():
                continue
            if not multiline_code and line.startswith("```"):
                # 多行公式开始
                multiline_code = True
                add_header = ""
                codename = line[3:].strip()
                if code_format == "inherit":
                    output += prefix + f"```{codename}\n\n"
                else:
                    output += prefix + f"```{code_format}\n\n"
                prefix = " " * len(prefix)
                continue
            elif multiline_code and line.endswith("```"):
                # 多行公式结束
                rest_code = line[:-3]
                if rest_code:
                    output += prefix + rest_code + "\n" + prefix + "```" + "\n\n"
                else:
                    output += prefix + "```" + "\n\n"
                multiline_code = False
                continue
            if not multiline_code:
                line = remove_double_square_bracket(alias(highlight(italics(equation(line)))))
            output += prefix + add_header + line + '\n'

    output_path = file_path.replace(".txt", ".md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)


def print_help_and_exit():
    print("Usage: python roam2md.py LEVEL CODE FILE/DIR ...")
    exit(1)


if __name__ == '__main__':
    # main("example/example.txt", 2)
    # exit(0)
    if len(sys.argv) <= 3:
        print_help_and_exit()

    level = int(sys.argv[1])
    code_format = sys.argv[2]

    for path in sys.argv[3:]:
        if not os.path.exists(path):
            print(path, "not exists")
            print_help_and_exit()
        if os.path.isfile(path):
            if not path.endswith(".txt"):
                print_help_and_exit()
            main(path, level)
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                full_path = os.path.join(path, filename)
                if os.path.isfile(full_path) and full_path.endswith(".txt"):
                    main(full_path, level)
        else:
            print(path, "not exists")
            print_help_and_exit()
