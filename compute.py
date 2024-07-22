import json

recipes  = json.load(open("recipies.json", 'r'))


def compute_rates(item_to_make, production_rate, recipes, rates):
    recipe = recipes[item_to_make]
    print(f"{item_to_make} needs:")
    if recipe == None:
        return

    for item, count in recipe['inputs'].items():
        if item not in rates:
            rates[item] = 0

        consumption_rate = production_rate * float(count) / float(recipe['outputs'][item_to_make])
        print(f"{item}: {consumption_rate}")
        rates[item] += consumption_rate
        compute_rates(item, consumption_rate, recipes, rates)

rates = {}
compute_rates('utility science pack', 1000/60, recipes, rates)
compute_rates('production science pack', 1000/60, recipes, rates)
compute_rates('chemical science pack', 1000/60, recipes, rates)
compute_rates('military science pack', 1000/60, recipes, rates)
compute_rates('logistic science pack', 1000/60, recipes, rates)
compute_rates('automation science pack', 1000/60, recipes, rates)
print({k:v*60 for k, v in rates.items() if k in ["iron plate", "copper plate", "plastic bar"]})
