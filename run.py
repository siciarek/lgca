
n = 6

step = round(0xFF / n)

color = 0xFF

while color > 0:
    print(f"#{color:02X}{color:02X}{color:02X}")
    color -= step


# from collections import defaultdict
# from pprint import pprint
# from lgca import settings
# import yaml
#
# fhpi = defaultdict(dict)
#
# for i in range(2 ** 6):
#
#     key = f"{i | 0b1000_0000:08b}"
#     val = key
#
#     fhpi["obstacle"][key] = val
#
#     key = f"{i:06b}"
#     val = key
#
#     fhpi["particle"][key] = val
#
# ddata = dict(sorted(fhpi.items(), reverse=True, key=lambda x: x[0]))
#
# (settings.BASE_PATH / "lgca" / "config" / "temp.yaml").write_text(yaml.dump(ddata, sort_keys=False))
