import math
import sys
 
 # import re
 # import pyparsing - available if you need it!
 # import lark - available if you need it!
 
 
def find_first_match_index(
     input_line: str, pattern: str, start_flag: bool = False, end_flag: bool = False
 ) -> int:
     """
     Finds the index of the first match of the given pattern in the input_line.
     If no match is found, returns -1.
 
     Parameters:
         input_line (str): The text to search in.
         pattern (str): The pattern to search for.
 
     Returns:
         int: The index of the first match, or -1 if no match is found.
     """
 
     # Check of end of line.
     if pattern == "$" and input_line == "":
         return 0
 
     # Check for patterns like \\d and \\w
     if pattern in ("\\d", "\\w"):
         for idx, char in enumerate(input_line):
             if (pattern == "\\d" and char.isdigit()) or (
                 pattern == "\\w" and (char.isalpha() or char.isdigit())
             ):
                 if not (start_flag) or (start_flag and idx == 0):
                     return idx + 1
     # Check for patterns like [abc] or [^abc]
     elif pattern[0] == "[" and pattern[-1] == "]":
         if pattern[1] == "^":
             negative_pattern = pattern[2:-1]
             for idx, c in enumerate(negative_pattern):
                 if c in input_line:
                     if not (start_flag) or (start_flag and idx == 0):
                         return -1
             else:
                 return 0
         else:
             positive_pattern = pattern[1:-1]
             for idx, c in enumerate(positive_pattern):
                 idx = input_line.find(c)
                 if idx != -1:
                     if not (start_flag) or (start_flag and idx == 0):
                         return idx + 1
     # Check for regular characters
     else:
         idx = input_line.find(pattern)
         if idx >= 0:
             if not (start_flag) or (start_flag and idx == 0):
                 return idx + 1
 
     return -1
 
 
def match_pattern_sequence(input_line: str, pattern: str) -> bool:
     """
     Check if input_line matches pattern. This method is called recursively.
 
     Parameters:
         input_line (str): Text to check.
         pattern (str): patterns.
 
     Returns:
         bool: True if input_line matches pattern, False otherwise.
     """
 
     start_flag = False
     end_flag = False
     while pattern:
 
         # Check for start flag
         if pattern[0] == "^":
             start_flag = True
             pattern = pattern[1:]
 
         # Check for end flag
         if pattern[-1] == "$":
             end_flag = True
 
         # Check for alternation
         if pattern[0] == "(":
             closing_index = pattern.find(")")
             pipe_index = pattern.find("|")
             if closing_index == -1:
                 raise ValueError(f"Alternation is not closed.{pattern}")
             if pipe_index == -1:
                 break
 
             alternations_str, pattern = (
                 pattern[1:closing_index],
                 pattern[closing_index + 1 :],
             )
             alternations = alternations_str.split("|")
             print(alternations)
             for alt in alternations:
                 if match_pattern_sequence(input_line, alt):
                     break
             else:
                 return False
 
         if len(pattern) == 0:
            return True

         # Get the current pattern to match
         if pattern[0] == "\\":
             current_pattern, pattern = pattern[:2], pattern[2:]
         elif pattern[0] == "[":
             closing_index = pattern.find("]") + 1
             if closing_index == 0:
#                raise ValueError("Closing not found")
                raise ValueError(f"Character group is not closed.{pattern}")
             current_pattern, pattern = pattern[:closing_index], pattern[closing_index:]
         else:
             current_pattern, pattern = pattern[:1], pattern[1:]
 
         if pattern and pattern[0] in ("+", "?", "."):
             q_mode, pattern = pattern[0], pattern[1:]
             match_len = 0
             while True:
                 input_start_pos = find_first_match_index(
                     input_line, current_pattern, start_flag, end_flag
                 )
 
                 if input_start_pos < 0:
                     if q_mode == "+":
                         if match_len > 0:
                             break
                         else:
                             return False
                     elif q_mode == "?":
                         break
                 else:
                     match_len += 1
                     input_line = input_line[input_start_pos:]
 
                     if q_mode in (".", "?") and match_len == 1:
                         break
 
         else:
             input_start_pos = find_first_match_index(
                 input_line, current_pattern, start_flag, end_flag
             )
 
             if input_start_pos < 0:
                 return False
             input_line = input_line[input_start_pos:]
 
     # Return True once whole pattern is checked without returning False
     return True
 
 
def main():
     pattern = sys.argv[2]
     input_line = sys.stdin.read()
 
     if sys.argv[1] != "-E":
         print("Expected first argument to be '-E'")
         exit(1)
 
     if match_pattern_sequence(input_line, pattern):
         exit(0)
     else:
         exit(1)
 
 
def main():
     pattern = sys.argv[2]
     input_line = sys.stdin.read()
 
     if sys.argv[1] != "-E":
         print("Expected first argument to be '-E'")
         exit(1)
 
     if match_pattern_sequence(input_line, pattern):
         exit(0)
     else:
         exit(1)
 
 
if __name__ == "__main__":
    main()

