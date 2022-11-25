from pyClever import Clever

# addr = "Center Alle 1, 7400"
# addr = "Marsvej 43, 8960"
# addr = "Gasværksvej 5, 8660"
# addr = "Lerchesvej 9, Svendborg"
addr = "Nowhere 1, Unknown"

if __name__ == "__main__":
    clever = Clever(addr)

    total = clever.chargepoint_total
    available = clever.chargepoint_available
    occupied = clever.chargepoint_occupied

    print("\033c", end="")
    print(clever.name)
    print(clever.directions)
    print(clever.address["address"])
    print(
        f"{clever.address['countryCode']}{clever.address['postalCode']} {clever.address['city']}"
    )
    print()
    print(clever.coordinates)
    print()
    print(f"Tilgængelige: {available}")
    print(f"Optaget: {occupied}")
    print(f"Totalt: {total}")
    print()
    print(f"Socket types at location: {clever.plug_types}")
