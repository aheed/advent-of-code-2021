import utils

lines = utils.get_in_file()

ints = utils.get_ints_from_in_file_lines(2)

oxy = 0
co2 = 0

def oxy_criterion(inarr, pos) -> bool:
    sum = 0
    
    for entry in inarr:
        sum += (entry >> pos) % 2
    
    if (sum == len(inarr) / 2 ):
        return True
    
    return sum > len(inarr) / 2

def oxy_number_ok(inarr, pos, number) -> bool:
    bit_val = (number >> pos) % 2
    return oxy_criterion(inarr, pos) == bit_val

def co2_number_ok(inarr, pos, number) -> bool:
    bit_val = (number >> pos) % 2
    return (not oxy_criterion(inarr, pos)) == bit_val


def oxy_criterion_at_pos(inarr, pos):
    def f(number):
        return oxy_number_ok(inarr, pos, number)
    return f

def co2_criterion_at_pos(inarr, pos):
    def f(number):
        return co2_number_ok(inarr, pos, number)
    return f


pos = 11
modarr = ints
while(len(modarr) > 1):
    modarr = list(filter(oxy_criterion_at_pos(modarr, pos), modarr))
    pos -= 1
    #print(len(modarr))
oxy = modarr[0]
#print("oxy", oxy)

pos = 11
modarr = ints
while(len(modarr) > 1):
    modarr = list(filter(co2_criterion_at_pos(modarr, pos), modarr))
    pos -= 1
    #print(len(modarr))
co2 = modarr[0]
#print("co2", co2)

print(oxy * co2)
