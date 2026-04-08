_compound_factory = None
_reaction_factory = None

def set_compound_factory(fn):
    global _compound_factory
    _compound_factory = fn

def set_reaction_factory(fn):
    global _reaction_factory
    _reaction_factory = fn

def make_compound(eq, charge=0):
    """Create a compound without importing compound directly."""
    return _compound_factory(eq, charge)

def make_reaction(*args, **kwargs):
    """Create a reaction without importing reaction directly."""
    return _reaction_factory(*args, **kwargs)
