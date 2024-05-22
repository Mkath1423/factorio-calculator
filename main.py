import json

recipies  = json.load(open("recipies.json", 'r'))


def print_summary(name, recipies):
    data = recipies[name]

    print(f"{name}:")
    print("\tinputs:")
    for name, quantity in data['inputs'].items():
        print(f"\t\t{quantity} x {name}")

    print("\toutputs:")
    for name, quantity in data['inputs'].items():
        print(f"\t\t{quantity} x {name}")

    print(f"\tcrafting time {data['crafting time']}s")

print_summary('transport belt', recipies)
