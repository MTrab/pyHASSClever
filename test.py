from pyClever import Clever

if __name__ == "__main__":
    clever = Clever()

    # loc = clever.get_location("17053")
    # loc = clever.get_location("50600132-60bf-ea11-a812-000d3ad97943")
    # uid = clever.get_uid("Marsvej 43, 8960 Randers SØ")
    # loc = clever.get_location("17053")
    # uid = clever.get_uid("17053")

    addr = "Center Alle 1, 7400"
    # addr = "Marsvej 43, 8960"

    loc = clever.get_location(addr)
    uid = clever.get_uid(addr)

    identifiers = clever.get_identification(uid)
    clever.load_chargepoints(identifiers)
    total = clever.chargepoint_total
    available = clever.chargepoint_available
    occupied = clever.chargepoint_occupied

    print(loc)
    print()
    print(identifiers)
    print()
    print(f"Tilgængelige: {available}")
    print(f"Optaget: {occupied}")
    print(f"Totalt: {total}")
    print()
    for ident in identifiers:
        print(clever.chargepoints.get_chargepoint_detail(ident))
