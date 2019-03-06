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

    @staticmethod
    def _c_to_f(celsius):
        return celsius * 9/5 + 32

    @staticmethod
    def _f_to_c(fahrenheit):
        return (fahrenheit - 32) * 5/9

    # this overridden methods does 2 things
    # first, it calls the base class version of dunder-init forwarding the owner_code and contents arguments to the
    # base class initializer.
    # unlike other OO languages where constructors at every lvl inan inheritance hierarchy will be called automatically,
    # the same can't be said for initializes in Python.

    def __init__(self, owner_code, contents, celsius):
        super().__init__(owner_code, contents)  # we call super to get a reference  to the base class instance, we then
        # call dunder-init on the returned reference and forward the constructor arguments
        # if celsius > RefrigeratedShippingContainer.MAX_CELSIUS:
        #     raise ValueError("Temperature too hot!")
        # self._celsius = celsius  # renamed to indicate to no longer considered public interface
        # instead of using the code above, simply assign through the property attribute rather than directly to the
        # underlying attribute and get validation for free
        self.celsius = celsius

    # one possible solution to discourage meddling with the celsius attribute could be to rename it to  _celsius and
    # wrap the attribute with 2 methods called get_celsius and set_celsius with the setter performing validation against
    # the MAX_CELSIUS class attribute. this could work but is not PYTHONIC, remember Python != Java
    # also, it would required to adjust all uses of celsius to be adjusted to use the method call syntax
    # Instead, Python provides a far superior alternative to getter and setter methods - called properties
    # which allow getters and setter to be exposed to seemingly regular attributes performing a graceful upgrade in
    # capabilities. as with static and class methods, decorators are the bases of properties
    @property
    def celsius(self):
        """
        What's happened here is that the @property has converted our celsius method into something that when accessed
        behaves like an attribute. sufficient to understand that @property can be used to transform getter methods so
        they can be call as if they were attributes.
        :return:
        """
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """
        this time rather than using a built-in decorator, we use a decorator specific to this property, which is itself
        an attribute of the property of the object that was created when we defined the getter. this new decorator is
        always called setter and must be accessed via the property object. Decorating our setter function with the
        @p.setter decorator causes the property object to be modified associating it with our setter method in addition
        to the getter method.
        :param value:
        :return:
        """
        if value > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return RefrigeratedShippingContainer._c_to_f(self.celsius)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = RefrigeratedShippingContainer._f_to_c(value)
