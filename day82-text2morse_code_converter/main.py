from collections import defaultdict
from contextlib import suppress

morse_code_dict = defaultdict(lambda: '(UnknownChar)', {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--.', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
})


def text2morse(input_text):
    output_code = []
    input_text = input_text.upper()
    for n, char in enumerate(input_text):
        if char == ' ':
            output_code.append('(7dit)')
        else:
            if n > 0 and input_text[n - 1] != ' ':
                output_code.append('(3dit)')
            code = morse_code_dict[char]
            output_code.append(code)
    return ''.join(output_code)


def main():
    try:
        while True:
            text_to_translate = input("Type text to be translated to a morse code:\n")
            output = text2morse(text_to_translate)
            print(f"Output:\n{output}")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == '__main__':
    main()
