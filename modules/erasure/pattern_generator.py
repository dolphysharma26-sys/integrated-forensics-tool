"""
Erasure Pattern Generator
"""

import os
import logging

logger = logging.getLogger(__name__)

class PatternGenerator:
    """Generates erasure patterns"""
    
    def __init__(self):
        logger.info("Pattern Generator initialized")
    
    def get_zero_pattern(self):
        return b'\x00' * 512
    
    def get_one_pattern(self):
        return b'\xFF' * 512
    
    def get_random_pattern(self):
        return os.urandom(512)
    
    def get_patterns(self, standard="DoD_5220_22_M"):
        """Get patterns for erasure standard"""
        if standard == "DoD_5220_22_M":
            return [self.get_zero_pattern(), self.get_one_pattern(), self.get_random_pattern()]
        elif standard == "NIST_800_88":
            return [self.get_zero_pattern()]
        else:
            return [self.get_zero_pattern()]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pg = PatternGenerator()
    patterns = pg.get_patterns()
    print(f"Generated {len(patterns)} patterns")
