import textwrap
from numpy.random import RandomState

__all__ = ["Entropy"]

def _entropy_mk_method(name):
    orig_func = RandomState.__dict__[name]

    args = None
    if orig_func.__doc__:
        # Most functions have their signature in the first line of their
        # docstring (ex, "beta(a, b, size=None)"). Split that out so we can
        # copy it into our function so it will show the correct signature in,
        # ex, IPython.
        first_line = orig_func.__doc__.strip().splitlines()[0]
        _, args = first_line.split("(")
        args = args.rstrip(")")
        argnames = ", ".join(
            a.partition("=")[0].strip()
            for a in args.split(",")
        )

    if not args or "[" in args or "..." in args:
        # Don't use signatures like "d0, d1, ..., dn"
        args = "*a, **kw"
        argnames = "*a, **kw"

    to_eval = textwrap.dedent("""\
        def {name}(self, {args}):
            return RandomState(self.seed).{name}({argnames})
    """.format(name=name, args=args, argnames=argnames))
    l = {"RandomState": RandomState}
    exec to_eval in l, l
    func = l[name]
    func.__doc__ = orig_func.__doc__
    return func

EntropyBase = type("EntropyBase", (object, ), {
    name: _entropy_mk_method(name)
    for name in dir(RandomState)
    if not name.startswith("_")
})

class Entropy(EntropyBase):
    """ A deterministic, immutable entropy source with the same methods as
        NumPy's RandomState.

        For example::

            >>> e = Entropy()
            >>> e.random()
            0.374540118847
            >>> e.random()
            0.374540118847
            >>> e = e.reseed()
            >>> e.random()
            0.454701052221

        All methods accept a ``size`` argument which returns a numpy array with
        that size::

            >>> e.randint(1, 10, size=10)
            array([7, 4, 8, 5, 7, 3, 7, 8, 5, 4])
            >>> e.randint(1, 10, size=(3, 3))
            array([[7, 4, 8],
                   [5, 7, 3],
                   [7, 8, 5]])

        List of methods:
        http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html
    """

    def __init__(self, seed=42):
        self.seed = seed

    def random(self, size=None):
        if size is not None:
            try:
                iter(size)
            except TypeError:
                return self.rand(size)
            return self.rand(*size)
        return self.rand()

    def reseed(self):
        return Entropy(seed=self.randint(0xFFFFFFFF))
