import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if pattern == "\d":
        return any(c.isdigit() for c in input_line)
    elif pattern == "\w":
        return any(c.isalnum() for c in input_line)
    elif pattern.startswith("[^"):
        characters_in_negative_character_group = pattern.split(']')[0][2:]
        return any(character not in characters_in_negative_character_group for character in input_line)
    elif pattern.startswith("["):
        characters_in_positive_character_group = pattern.split(']')[0][1:]
        return any(character in characters_in_positive_character_group for character in input_line)
    elif len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
     main()