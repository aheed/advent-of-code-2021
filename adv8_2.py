from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line for line in infile]

@dataclass
class Entry:
    digits: list[set[str]]
    output: list[set[str]]

def create_entry(instring: str) -> Entry:
    parts = instring.strip().split(" | ")
    digit_strings = parts[0].split(" ")
    digits = [set(charac) for charac in digit_strings]
    output_strings = parts[1].split(" ")
    output = [set(charac) for charac in output_strings]
    return Entry(digits, output)


entries = [create_entry(line) for line in lines]



def calc_value(entry: Entry) -> int:
    
    
    position_dict: dict[int, int] = {}

    #populate position_dict with 1,4,7,8
    index1 = next((i for i in range(10) if len(entry.digits[i]) == 2))
    position_dict[index1] = 1
    one_set = entry.digits[index1]
    print(index1)

    index4 = next((i for i in range(10) if len(entry.digits[i]) == 4))
    position_dict[index4] = 4
    four_set = entry.digits[index4]
    print(index4)

    index7 = next((i for i in range(10) if len(entry.digits[i]) == 3))
    position_dict[index7] = 7
    print(index7)

    index8 = next((i for i in range(10) if len(entry.digits[i]) == 7))
    position_dict[index8] = 8
    print(index8)

    ##populate segments_dict with 1,4,7,8
    ##print(segments_dict)
    
    

    #populate position_dict with 9,6
    index6 = next((i for i in range(10) if (i not in position_dict) and (len(entry.digits[i]) == 6) and (not one_set.issubset(entry.digits[i]) ) ))
    position_dict[index6] = 6
    six_set = entry.digits[index6]
    print(index6)
    
    index9 = next((i for i in range(10) if (i not in position_dict) and (len(entry.digits[i]) == 6) and (four_set.issubset(entry.digits[i]) ) ))
    position_dict[index9] = 9
    print(index9)

    index0 = next((i for i in range(10) if (i not in position_dict) and (len(entry.digits[i]) == 6)))
    position_dict[index0] = 0
    print(index0)

    #3
    index3 = next((i for i in range(10) if (i not in position_dict) and (len(entry.digits[i]) == 5) and (one_set.issubset(entry.digits[i]) ) ))
    position_dict[index3] = 3
    print(index3)

    #5
    index5 = next((i for i in range(10) if (i not in position_dict) and (len(entry.digits[i]) == 5) and (six_set.issuperset(entry.digits[i]) ) ))
    position_dict[index5] = 5
    print(index5)

    #2
    index2 = next((i for i in range(10) if (i not in position_dict)))
    position_dict[index2] = 2
    print(index2)

    print(position_dict)

    # set_dict: dict[set[str], int] = {}
    # for output_value, index in position_dict.items():
    #     set_dict[entry.digits[index]] =  output_value
    # print(set_dict)


    # for each output digit: get digit value and multiply
    x1000_set = entry.output[0]
    x1000_index = next((i for i in range(10) if entry.digits[i] == x1000_set))
    x1000_digit_val = position_dict[x1000_index]

    x100_set = entry.output[1]
    x100_index = next((i for i in range(10) if entry.digits[i] == x100_set))
    x100_digit_val = position_dict[x100_index]

    x10_set = entry.output[2]
    x10_index = next((i for i in range(10) if entry.digits[i] == x10_set))
    x10_digit_val = position_dict[x10_index]

    x1_set = entry.output[3]
    x1_index = next((i for i in range(10) if entry.digits[i] == x1_set))
    x1_digit_val = position_dict[x1_index]

    #x1000 = set_dict[entry.output[0]]
    print(x1000_digit_val)
    print(x100_digit_val)
    print(x10_digit_val)
    print(x1_digit_val)

    # def calc_digit_value() -> int:

    #
    return x1000_digit_val * 1000 + x100_digit_val * 100 + x10_digit_val * 10 + x1_digit_val

a = calc_value(entries[0])
print(a)

res = sum([calc_value(entry) for entry in entries])
print(res)