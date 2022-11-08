from pyClever import Clever

if __name__ == "__main__":
    clever = Clever()

    loc = clever.get_location_by_id("0262230b-c072-0979-967e-ad045a26af10")

    print(loc)