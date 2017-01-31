import kb, sys
from kb import KB, Boolean, Integer, Constant

# Define our symbols
x = Integer('x')
y = Integer('y')
z = Integer('z')

# Create a new knowledge base
kb = KB()


a = x >= z
b = y >= x
c = y == 1
d = z == 2



# Add clauses
kb.add_clause(a)
kb.add_clause(b)
kb.add_clause(c)
kb.add_clause(d)


# Print all models of the knowledge base
for model in kb.models():
    print model

# Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print kb.satisfiable()
print kb.satisfiable()
