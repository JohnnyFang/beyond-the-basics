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
    def create_empty(cls, owner_code, *args, **kwargs):
        return cls(owner_code, contents=None, *args, **kwargs)

    # the following is a factory method /function or named constructors
    @classmethod
    def create_with_items(cls, owner_code, items, *args, **kwargs):
        return cls(owner_code, contents=list(items), *args, **kwargs)

    def __init__(self, owner_code, contents):
        self.owner_code = owner_code
        self.contents = contents
        # self.bic = ShippingContainer._make_bic_code(
        self.bic = self._make_bic_code(  # by changing this to self we get polymorphic BIC generation from the single
            # constructor implementation
            owner_code=owner_code,
            serial=ShippingContainer._get_next_serial())
        # ShippingContainer.next_serial += 1
        # using self.next_serial += 1 will not have the desired effect bc assignment to attributes
        # (e.g. self.attr = something) always create an instance attribute, never a class attribute

        # keep in mind that by calling static methods through the class we effectively prevent them being overridden,
        #  at least from the point of view of the base class.
        # if you need polymorphic dispatch of @staticmethod invocations, call through the self instance


class RefrigeratedShippingContainer(ShippingContainer):
    #  *args, **kwargs were added to both @classmethods to support inheritance
    MAX_CELSIUS = 4.0

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code,
                              serial=str(serial).zfill(6),
                              category='R')

    # this overridden methods does 2 things
    # first, it calls the base class version of dunder-init forwarding the owner_code and contents arguments to the
    # base class initializer.
    # unlike other OO languages where constructors at every lvl inan inheritance hierarchy will be called automatically,
    # the same can't be said for initializes in Python.

    def __init__(self, owner_code, contents, celsius):
        super().__init__(owner_code, contents)  # we call super to get a reference  to the base class instance, we then
        # call dunder-init on the returned reference and forward the constructor arguments
        if celsius > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot!")
        self.celsius = celsius
