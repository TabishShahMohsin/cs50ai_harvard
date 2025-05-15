import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prod = 1
    for i in people:

        # Getting the gene of the person in consideration
        if i in one_gene:
            gene = 1
        elif i in two_genes:
            gene = 2
        else:
            gene = 0

        # Getting the trait of the person in consideration
        if i in have_trait:
            trait = True
        else:
            trait = False

        # If parental info isn't provided
        if people[i]["father"] == None and people[i]["mother"] == None:
            prod *= PROBS["gene"][gene] * PROBS["trait"][gene][trait]
        # If parental info is provided for the person i
        else:
            
            # Getting the mother's mutated gene count
            mother = people[i]["mother"]
            if mother in one_gene:
                mother_gene = 1
            elif mother in two_genes:
                mother_gene = 2
            else:
                mother_gene = 0
        
            # Getting the father's mutated gene count
            father = people[i]["father"]
            if father in one_gene:
                father_gene = 1
            elif father in two_genes:
                father_gene = 2
            else:
                father_gene = 0

            m = PROBS["mutation"]
            nm = 1 - PROBS["mutation"]

            # Always need to mutltiply this at the end
            # This is prob of going from gene to trait, now we need to get the prob of getting the gene in the variale gene
            prod *= PROBS["trait"][gene][trait]
    
            # Making a gene combination list
            inherited_genes = list()
            count_to_genes = {1: ["NM", "M"], 0: ["NM", "NM"], 2: ["M", "M"]}
            for k in count_to_genes[mother_gene]:
                for j in count_to_genes[father_gene]:
                    inherited_genes.append((k, j))

            prob = 0
            child_genes = count_to_genes[gene]
            for genes in inherited_genes:
                if genes[0] == child_genes[0]:
                    x = nm
                else:
                    x = m
                if genes[1] == child_genes[1]:
                    y = nm
                else:
                    y = m

                # If mutated gene count is 1, then the genes can be made in the opposite fashion as well
                if gene == 1:
                    z = m * nm * m * nm / (x * y)
                else:
                    z = 0

                prob += 0.25 * (x * y + z)

            prod *= prob  
    return prod


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for i in one_gene:
        probabilities[i]["gene"][1] += p
    for i in two_genes:
        probabilities[i]["gene"][2] += p
    for i in set(probabilities) - one_gene - two_genes:
        probabilities[i]["gene"][0] += p

    for i in have_trait:
        probabilities[i]["trait"][True] += p
    for i in set(probabilities) - have_trait:
        probabilities[i]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for i in probabilities:
        sum = probabilities[i]["trait"][True] + probabilities[i]["trait"][False]
        probabilities[i]["trait"][True] /= sum 
        probabilities[i]["trait"][False] /= sum 

    for i in probabilities:
        sum = probabilities[i]["gene"][1] + \
        probabilities[i]["gene"][2] + \
        probabilities[i]["gene"][0]
        probabilities[i]["gene"][0] /= sum 
        probabilities[i]["gene"][1] /= sum 
        probabilities[i]["gene"][2] /= sum 


if __name__ == "__main__":
    main()
