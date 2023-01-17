import sys

 # import pyparsing - available if you need it!
 # import lark - available if you need it!

def match_here(remaining_input, pattern):
    # Base case: empty pattern matches any input
    if pattern == "":
        return True
    
    if pattern.startswith("\\d+"):
        for i in range(len(remaining_input)):
            if remaining_input[i].isdigit():
                return match_here(remaining_input[i+1:], pattern[3:])
            else:
                return False

    elif pattern.startswith("\\w+"):
        for i in range(len(remaining_input)):
            if remaining_input[i].isalnum():
                return match_here(remaining_input[i+1:], pattern[3:])
            else:
                return False

    elif pattern.startswith("[^"):
        characters_in_negative_character_group = pattern.split(']')[0][2:]
        for i in range(len(remaining_input)):
            if remaining_input[i] not in characters_in_negative_character_group:
                return match_here(remaining_input[i+1:], pattern[3+len(characters_in_negative_character_group):])
            else:
                return False

    elif pattern.startswith("["):
        characters_in_positive_character_group = pattern.split(']')[0][1:]
        for i in range(len(remaining_input)):
            if remaining_input[i] in characters_in_positive_character_group:
                return match_here(remaining_input[i+1:], pattern[2+len(characters_in_positive_character_group):])
            else:
                return False

    elif len(pattern) == 1:
        for i in range(len(remaining_input)):
            if remaining_input[i] == pattern[0]:
                return match_here(remaining_input[i+1:], pattern[1:])
            else:
                return False
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