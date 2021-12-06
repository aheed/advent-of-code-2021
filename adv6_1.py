import utils

with utils.get_in_file() as infile:
    lines = [line for line in infile]
#print(lines[0])

input = [int(time_left) for time_left in lines[0].split(",")]
#print(input)

def get_empty_population() -> list[int]:
    return [0] * 9

start_population = get_empty_population()
for fish in input:
    start_population[fish] += 1
#print(start_population)

def new_fish_timer(fish_timer: int) -> int:
    if (fish_timer == 0):
        return 6
    return fish_timer - 1

def spawn(fish_timer: int) -> bool:
    return fish_timer == 0

def merge_two_populations(population1: list[int], population2: list[int]) -> list[int]:
    res_list = [sum(i) for i in zip(population1, population2)]
    return res_list

def merge_populations(populations: list[list[int]]) -> list[int]:
    res = get_empty_population()
    for pop in populations:
        res = merge_two_populations(res, pop)
    return res

def multiply_population(start_population: list[int], multiplyer: int) -> list[int]:
    return [multiplyer * num_fish for num_fish in start_population]

def population_from_population(start_population: list[int], days: int) -> list[int]:
    populations = [multiply_population(population_from_fish(fish_timer, days), start_population[fish_timer]) for fish_timer in range(9)]
    res = merge_populations(populations)
    return res

def population_from_fish(fish_timer: int, days: int) -> list[int]:
    one_day_population = get_empty_population()
    if (days == 0):
        one_day_population[fish_timer] = 1
        return one_day_population

    original_fish_population = population_from_fish(new_fish_timer(fish_timer), days - 1)
    if (not spawn(fish_timer)):
        return original_fish_population

    spawned_population = population_from_fish(8, days - 1)
    res = merge_two_populations(original_fish_population, spawned_population)
    return res

#start_population = [0,1,1,2,1,0,0,0,0] #TEMP!!!
#days_left = 18 #TEMP!!!

days_left = 80
result = population_from_population(start_population, days_left)
#print(result)
print(sum(result))

    
