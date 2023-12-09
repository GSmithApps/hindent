# %%

from hindent import Hindent
from pathlib import Path
from scheme_execution import execute_scheme_code
hindent = Hindent(
    Path('./first.hin'), 
    execute_scheme_code
)

# %%

output, error = hindent.run()
print(output)