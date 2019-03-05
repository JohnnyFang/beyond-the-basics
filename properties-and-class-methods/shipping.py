import iso6346


class ShippingContainer:
    next_serial = 11337 # class attribute

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code,
                              serial=str(serial).zfill(6))

    @staticmethod
    def _get_next_serial():
        result = ShippingContainer.next_serial
        ShippingContainer.next_serial += 1
        return result

    # the following is a factory method /function or named constructors
    @classmethod
    def create_empty(cls, owner_code):
        return cls(owner_code, contents=None)

    # the following is a factory method /function or named constructors
    @classmethod
    def create_with_items(cls, owner_code, items):
        return cls(owner_code, contents=list(items))

    def __init__(self, owner_code, contents):
        self.owner_code = owner_code
        self.contents = contents
        self.bic = ShippingContainer._make_bic_code(
            owner_code=owner_code,
            serial=ShippingContainer._get_next_serial())
        # ShippingContainer.next_serial += 1
        # using self.next_serial += 1 will not have the desired effect bc assignment to attributes
        # (e.g. self.attr = something) always create an instance attribute, never a class attribute
