def print_rainbow_text(text, **kwargs):
    colors = [
        "\033[91m",  # 빨강
        "\033[93m",  # 노랑
        "\033[92m",  # 초록
        "\033[96m",  # 청록
        "\033[94m",  # 파랑
        "\033[95m",  # 보라
    ]
    reset_color = "\033[0m"
    colored_text = ""

    for i, char in enumerate(text):
        colored_text += colors[i % len(colors)] + char

    colored_text += reset_color
    print(colored_text, **kwargs)


def print_color_text(text, color, **kwargs):
    colors = {
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "cyan": "\033[96m",
        "blue": "\033[94m",
        "purple": "\033[95m",
    }
    reset_color = "\033[0m"
    colored_text = colors[color] + text + reset_color
    print(colored_text, **kwargs)
