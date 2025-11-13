def mirror_word(word: str) -> str:
    """
    Transform a word by:
    1. Flipping case (a->A, B->b)
    2. Reversing the whole string
    
    Non-alphabetic chars stay as-is.
    """
    # Swap case for each character
    case_flipped = ''.join(
        char.upper() if char.islower() else 
        char.lower() if char.isupper() else 
        char
        for char in word
    )
    
    # Reverse the string
    return case_flipped[::-1]
