import sys

 # import pyparsing - available if you need it!
 # import lark - available if you need it!


# def match_pattern(input_line, pattern):
#     if pattern == "\\d":
#         return any(character.isdigit() for character in input_line)
#     elif pattern == "\\w":
#         return any(character.isalnum() for character in input_line)

def match_here(remaining_input, pattern, input_line):
    # Base case: empty pattern matches any input
    if pattern == "":
        return True

    # Base case: if there's no input remaining, the match failed
    if remaining_input == "":
        return False

    if pattern.startswith("\\d"):
        if remaining_input[0].isdigit():
            return match_here(remaining_input[1:], pattern[2:], input_line)
        else:
            return match_here(remaining_input[1:], pattern, input_line)

    elif pattern.startswith("\\w"):
        if remaining_input[0].isalnum():
            return match_here(remaining_input[1:], pattern[2:], input_line)
        else:
            return match_here(remaining_input[1:], pattern, input_line)

    elif pattern.startswith("[^"):
        characters_in_negative_character_group = pattern.split(']')[0][2:]
        return any(character not in characters_in_negative_character_group for character in input_line)

        if remaining_input[0] not in characters_in_negative_character_group:
            return match_here(remaining_input[1:], pattern[3+len(characters_in_negative_character_group):])
        else:
            return False
    elif pattern.startswith("["):
        characters_in_positive_character_group = pattern.split(']')[0][1:]
        return any(character in characters_in_positive_character_group for character in input_line)
    elif len(pattern) == 1:
        return pattern in input_line

        # if remaining_input[0] in characters_in_positive_character_group:
        #     return match_here(remaining_input[1:], pattern[2+len(characters_in_positive_character_group):])
        # else:
        #     return False
    else:
        if remaining_input[0] == pattern[0]:
            return match_here(remaining_input[1:], pattern[1:], input_line)
        else:
            return False


def match_pattern(input_line, pattern):
    if pattern[0] == "^":
        return match_here(input_line, pattern[1:], input_line)
    # Base case: if there's no input remaining, the match failed
    if input_line == "":
        return False

    if match_here(input_line, pattern, input_line):
        return True
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")
        return match_pattern(input_line[1:], pattern)


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read().splitlines()[0]

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()