# RA, 2020-06-18

import json
from tcga.data.sa_aa_ref_chart import properties as aa_properties
from tcga.refs import annotations

print(aa_properties)
print(json.dumps(annotations[aa_properties], indent=2))
