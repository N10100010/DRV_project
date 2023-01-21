import subprocess

# try:
#     subprocess.check_call(args=["railway", "run"])
# except subprocess.CalledProcessError:
#     pass

# subprocess.check_call(args=["railway", "run"])

import os

vars = [
    "PGHOST",
    "PGPORT",
    "PGUSER",
    "PGPASSWORD",
    "PGDATABASE",
    "DATABASE_URL",
]

for k in vars:
    print(k, os.environ.get(k))