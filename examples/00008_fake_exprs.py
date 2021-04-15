# RA, 2021-04-15

from tcga.fake import GammaNB
fake = GammaNB(phi=0.5, mu_shape=1, mu_scale=10, random_state=43)

print(fake.generate(nsamples=3, ngenes=20))

# Gene       Gene00000  Gene00001  Gene00002  ...  Gene00017  Gene00018  Gene00019
# Sample                                      ...
# 000000000          1          0          0  ...          6          2         29
# 000000001          0          0          0  ...          0         49         16
# 000000002          0          0          0  ...          9         13          2
