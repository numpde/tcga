# RA, 2021-04-15

import numpy
import pandas


class GammaNB:
    """
    Dream up a single-cell expression table.
    The gene mean mu (across samples) is gamma-distributed (across genes).
    The expression of a gene is negative binomial with common dispersion phi and mean mu.

    Thus the parameters for the numpy/scipy negative_binomial function are
        n=phi  and  p=(1 / (1 + mu / phi)).

    The expression table is "samples as rows" x "genes as columns".

    Usage:
        faker = GammaNB(phi=0.5, mu_shape=1, mu_scale=1, random_state=0)
        exprs = faker.generate(nsamples, ngenes)
        faker.exprs    # nsamples x ngenes expression data frame (pandas.DataFrame)
        faker.mus      # gene's mu indexed by gene
        faker.genes    # series of gene names
        faker.samples  # series of sample names
    """

    def __init__(self, phi=0.5, mu_shape=1, mu_scale=1, random_state=0):
        """
        :param random_state: Random seed for RNG.
        :param phi: Common dispersion parameter for the negative binomial.
        :param mu_shape: Shape parameter for the gamma distribution of gene mean.
        :param mu_scale: Scale parameter for the gamma distribution of gene mean.
        """
        self.rng = numpy.random.default_rng(seed=random_state)
        self.phi = phi
        self.mu_shape = mu_shape
        self.mu_scale = mu_scale

    def generate(self, nsamples, ngenes):
        """
        :param nsamples: Number of samples/rows.
        :param ngenes: Number of genes/columns.
        :return: Expression data frame.
        """
        self.genes = pandas.Index([f"Gene{x:05}" for x in range(ngenes)], name="Gene")
        self.samples = pandas.Index([f"{x:09}" for x in range(nsamples)], name="Sample")

        self.mus = pandas.Series(
            index=self.genes,
            data=self.rng.gamma(shape=self.mu_shape, scale=self.mu_scale, size=ngenes),
            name="mu",
        )

        self.exprs = pandas.DataFrame(
            index=self.samples,
            columns=self.genes,
            data={
                g: self.rng.negative_binomial(n=self.phi, p=(1 / (1 + self.mus[g] / self.phi)), size=nsamples)
                for g in self.genes
            },
            dtype='int',
        )

        return self.exprs


if __name__ == '__main__':
    fake = GammaNB()
    print(fake.generate(9, 120))
    print(fake.genes)
    print(fake.samples)

    print(fake.mus)
    print(fake.exprs.mean(axis=0))

