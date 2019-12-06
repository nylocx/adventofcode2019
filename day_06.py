# %% Part 1 and 2
def sample_path(data, obj, counter=0):
    while obj in data.keys():
        yield (obj := data[obj]), counter
        counter += 1


with open("day_06.input", "r") as input_data:
    parent_map = dict(reversed(line.strip().split(")")) for line in input_data)

print(
    f"Part 1: Total number of orbits is "
    f"{sum(len(list(sample_path(parent_map, obj))) + 1 for obj in parent_map.values())}"
)
my_path = {obj: count for obj, count in sample_path(parent_map, "YOU")}
for obj, count in sample_path(parent_map, "SAN"):
    if obj in my_path:
        print(f"Part 2: Path from YOU to SAN needs {my_path[obj] + count} hops")
        break
