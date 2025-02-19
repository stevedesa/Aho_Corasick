test_cases = [
    # Test case 1: Overlapping patterns
    ("ATGATGATGA", ["ATG", "TGA", "GAT"], [
        (0, 2, 'ATG'), (1, 3, 'TGA'), (2, 4, 'GAT'), 
        (3, 5, 'ATG'), (4, 6, 'TGA'), (5, 7, 'GAT'), 
        (6, 8, 'ATG'), (7, 9, 'TGA')
    ]),
    
    # Test case 2: Nested patterns
    ("ATGCATGTGAACTG", ["ATG", "TG", "G"], [
        (0, 2, "ATG"), (1, 2, "TG"), (2, 2, "G"), 
        (4, 6, "ATG"), (5, 6, "TG"), (6, 6, "G"), 
        (7, 8, "TG"), (8, 8, "G"), (12, 13, 'TG'),
        (13, 13, 'G')
    ]),
    
    # Test case 3: Single character patterns
    ("GATTACA", ["G", "A", "T", "C"], [
        (0, 0, "G"), (1, 1, "A"), (2, 2, "T"), 
        (3, 3, "T"), (4, 4, "A"), (5, 5, "C"), (6, 6, "A")
    ]),
    
    # Test case 4: No matches
    ("GATTACA", ["XYZ", "PQR", "LMN"], []),
    
    # Test case 5: All possible overlapping matches
    ("ATATAT", ["ATA", "TAT"], [
        (0, 2, "ATA"), (1, 3, "TAT"), 
        (2, 4, "ATA"), (3, 5, "TAT")
    ]),
    
    # Test case 6: Empty pattern list
    ("ACGTACGTACGT", [], []),
    
    # Test case 7: Pattern longer than the sequence
    ("ACGT", ["ACGTA"], []),
    
    # Test case 8: Special characters
    ("A*T^G&C", ["A*T", "G&C", "^G"], [
        (0, 2, "A*T"), (3, 4, "^G"), (4, 6, "G&C")
    ]),
    
    # Test case 9: Repeated patterns
    ("ATGATGATG", ["ATG", "ATG", "TGA"], [
        (0, 2, 'ATG'), (1, 3, 'TGA'), (3, 5, 'ATG'),
        (4, 6, 'TGA'), (6, 8, 'ATG')
    ]),
    
    # Test case 10: Reverse complement patterns (literal match only)
    ("ATGCATGTGAACTGTAGCAGACCA", ["TAC", "ACG", "CAG"], [
        (17, 19, 'CAG')
    ]),
    
    # Test case 11: Mixed case patterns
    ("aTgCATGtGaAcT", ["atg", "CAT", "tgA"], [
        (3, 5, 'CAT')
    ]),
    
    # Test case 12: Exact sequence-pattern match
    ("ATGCATG", ["ATGCATG"], [
        (0, 6, "ATGCATG")
    ])
]