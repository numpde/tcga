# RA, 2020-06-18

import json
from tcga.refs import annotations
from tcga.data.sa_aa_ref_chart import properties as aa_properties

print(aa_properties)
print(json.dumps(annotations[aa_properties], indent=2))
