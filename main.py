from src.instance import Instance
from src.clarke_wright import ClarkeWright

instance = Instance('instances/solomon_25/C101.txt').load()

_, routes = ClarkeWright.run(instance, instance.vehicle_number)

print(routes)