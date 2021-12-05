import utils

ints = utils.get_ints_from_in_file_lines(2)

def oxy_criterion(inarr: list[int], pos: int) -> bool:
    sum = 0
    
    for entry in inarr:
        sum += (entry >> pos) % 2
    
    if (sum == len(inarr) / 2 ):
        return True
    
    return sum > len(inarr) / 2

def oxy_number_ok(inarr: list[int], pos: int, number: int) -> bool:
    bit_val = (number >> pos) % 2
    return oxy_criterion(inarr, pos) == bit_val

def criterion_at_pos(inarr: list[int], pos: int, co2: bool):
    def f(number: int):
        return co2 ^ oxy_number_ok(inarr, pos, number)
    return f

def get_rate(co2: bool) -> int:
    pos = 11
    modarr = ints
    while(len(modarr) > 1):
        modarr = list(filter(criterion_at_pos(modarr, pos, co2), modarr))
        pos -= 1
    return modarr[0]    

oxy_res = get_rate(False)
#print("oxy", oxy_res)

co2_res = get_rate(True)
#print("co2", co2_res)

print(oxy_res * co2_res)
