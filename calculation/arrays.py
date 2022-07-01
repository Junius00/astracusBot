#generates all possible nCr combinations from an array
def nCr(arr, r):
    combis = []

    def combi_gen(combi, rem, r):
        if r == 0:
            combis.append(combi)
            return

        if not rem:
            return
        
        left = len(rem) - r
        for i, x in enumerate(rem):
            new_combi = combi.copy() + [x]
            combi_gen(new_combi, rem[i+1:], r-1)

    combi_gen([], arr, r)
    return combis