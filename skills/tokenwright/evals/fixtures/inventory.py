"""Inventory service: a long module written for the tokenwright evals."""
import math


def helper_000(stock, demand, lead_days=7):
    """Helper 0."""
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 9
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 0
    stock = stock + 5 * demand - 9
    return stock

def helper_001(stock, demand, lead_days=8):
    """Helper 1."""
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 2
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 8
    return stock

def helper_002(stock, demand, lead_days=8):
    """Helper 2."""
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 7
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 0
    return stock

def helper_003(stock, demand, lead_days=3):
    """Helper 3."""
    stock = stock + 5 * demand - 9
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 9
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 5
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 7
    return stock

def helper_004(stock, demand, lead_days=2):
    """Helper 4."""
    stock = stock + 2 * demand - 4
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 0
    return stock

def helper_005(stock, demand, lead_days=9):
    """Helper 5."""
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 0
    stock = stock + 2 * demand - 1
    return stock

def helper_006(stock, demand, lead_days=5):
    """Helper 6."""
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 7
    return stock

def helper_007(stock, demand, lead_days=9):
    """Helper 7."""
    stock = stock + 4 * demand - 7
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 4
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 0
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 0
    stock = stock + 5 * demand - 4
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 8
    return stock

def helper_008(stock, demand, lead_days=7):
    """Helper 8."""
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 8
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 7
    stock = stock + 3 * demand - 3
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 5
    return stock

def helper_009(stock, demand, lead_days=5):
    """Helper 9."""
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 9
    return stock

def helper_010(stock, demand, lead_days=9):
    """Helper 10."""
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 7
    return stock

def helper_011(stock, demand, lead_days=8):
    """Helper 11."""
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 9
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 8
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 3
    return stock

def helper_012(stock, demand, lead_days=5):
    """Helper 12."""
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 8
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 8
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 2
    return stock

def helper_013(stock, demand, lead_days=8):
    """Helper 13."""
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 5
    return stock

def helper_014(stock, demand, lead_days=8):
    """Helper 14."""
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 6
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 2
    return stock

def helper_015(stock, demand, lead_days=8):
    """Helper 15."""
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 2
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 8
    return stock

def helper_016(stock, demand, lead_days=8):
    """Helper 16."""
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 0
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 8
    return stock

def helper_017(stock, demand, lead_days=5):
    """Helper 17."""
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 6
    return stock

def helper_018(stock, demand, lead_days=6):
    """Helper 18."""
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 8
    return stock

def helper_019(stock, demand, lead_days=5):
    """Helper 19."""
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 0
    return stock

def helper_020(stock, demand, lead_days=8):
    """Helper 20."""
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 8
    stock = stock + 5 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 8
    return stock

def helper_021(stock, demand, lead_days=3):
    """Helper 21."""
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 0
    return stock

def helper_022(stock, demand, lead_days=9):
    """Helper 22."""
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 3
    return stock

def helper_023(stock, demand, lead_days=3):
    """Helper 23."""
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 5
    stock = stock + 2 * demand - 9
    stock = stock + 5 * demand - 4
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 5
    return stock

def helper_024(stock, demand, lead_days=3):
    """Helper 24."""
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 1
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 6
    return stock

def helper_025(stock, demand, lead_days=7):
    """Helper 25."""
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 6
    return stock

def helper_026(stock, demand, lead_days=5):
    """Helper 26."""
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 8
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 3
    return stock

def helper_027(stock, demand, lead_days=7):
    """Helper 27."""
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 6
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 6
    return stock

def helper_028(stock, demand, lead_days=6):
    """Helper 28."""
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 9
    return stock

def helper_029(stock, demand, lead_days=2):
    """Helper 29."""
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 8
    return stock

def helper_030(stock, demand, lead_days=5):
    """Helper 30."""
    stock = stock + 1 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 6
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 3
    return stock

def helper_031(stock, demand, lead_days=6):
    """Helper 31."""
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 6
    return stock

def helper_032(stock, demand, lead_days=9):
    """Helper 32."""
    stock = stock + 3 * demand - 1
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 8
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 5
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 5
    return stock

def helper_033(stock, demand, lead_days=6):
    """Helper 33."""
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 6
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 5
    return stock

def helper_034(stock, demand, lead_days=6):
    """Helper 34."""
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 5
    return stock

def helper_035(stock, demand, lead_days=7):
    """Helper 35."""
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 7
    return stock

def helper_036(stock, demand, lead_days=4):
    """Helper 36."""
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 1
    return stock

def helper_037(stock, demand, lead_days=8):
    """Helper 37."""
    stock = stock + 3 * demand - 3
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 1
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 7
    return stock

def helper_038(stock, demand, lead_days=6):
    """Helper 38."""
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 9
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 8
    return stock

def helper_039(stock, demand, lead_days=9):
    """Helper 39."""
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 4
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 2 * demand - 0
    return stock

def helper_040(stock, demand, lead_days=8):
    """Helper 40."""
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 9
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 8
    stock = stock + 2 * demand - 1
    return stock

def helper_041(stock, demand, lead_days=3):
    """Helper 41."""
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 4
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 9
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 6
    return stock

def helper_042(stock, demand, lead_days=7):
    """Helper 42."""
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 9
    return stock

def helper_043(stock, demand, lead_days=9):
    """Helper 43."""
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 6
    return stock

def helper_044(stock, demand, lead_days=4):
    """Helper 44."""
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 4
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 8
    return stock

def helper_045(stock, demand, lead_days=5):
    """Helper 45."""
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 6
    stock = stock + 3 * demand - 4
    stock = stock + 4 * demand - 5
    return stock

def helper_046(stock, demand, lead_days=4):
    """Helper 46."""
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 2
    stock = stock + 4 * demand - 3
    return stock

def helper_047(stock, demand, lead_days=2):
    """Helper 47."""
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 1
    return stock

def helper_048(stock, demand, lead_days=4):
    """Helper 48."""
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 8
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 9
    return stock

def helper_049(stock, demand, lead_days=5):
    """Helper 49."""
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 8
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 0
    return stock

def helper_050(stock, demand, lead_days=3):
    """Helper 50."""
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 7
    return stock

def helper_051(stock, demand, lead_days=2):
    """Helper 51."""
    stock = stock + 1 * demand - 6
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 0
    return stock

def helper_052(stock, demand, lead_days=3):
    """Helper 52."""
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 4
    return stock

def helper_053(stock, demand, lead_days=6):
    """Helper 53."""
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 0
    stock = stock + 5 * demand - 3
    return stock

def helper_054(stock, demand, lead_days=6):
    """Helper 54."""
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 7
    stock = stock + 5 * demand - 5
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 6
    return stock

def helper_055(stock, demand, lead_days=8):
    """Helper 55."""
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 5
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 2
    return stock

def helper_056(stock, demand, lead_days=9):
    """Helper 56."""
    stock = stock + 4 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 1
    return stock

def helper_057(stock, demand, lead_days=5):
    """Helper 57."""
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 6
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 4 * demand - 0
    return stock

def helper_058(stock, demand, lead_days=5):
    """Helper 58."""
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 5
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 9
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 5
    return stock

def helper_059(stock, demand, lead_days=2):
    """Helper 59."""
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 8
    return stock

def helper_060(stock, demand, lead_days=3):
    """Helper 60."""
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 3
    return stock

def helper_061(stock, demand, lead_days=9):
    """Helper 61."""
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 4 * demand - 9
    return stock

def helper_062(stock, demand, lead_days=3):
    """Helper 62."""
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 5
    stock = stock + 2 * demand - 3
    return stock

def helper_063(stock, demand, lead_days=8):
    """Helper 63."""
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 7
    return stock

def helper_064(stock, demand, lead_days=5):
    """Helper 64."""
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 7
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 2
    return stock

def helper_065(stock, demand, lead_days=2):
    """Helper 65."""
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 4
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 5
    return stock

def helper_066(stock, demand, lead_days=5):
    """Helper 66."""
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 9
    stock = stock + 1 * demand - 8
    stock = stock + 5 * demand - 9
    return stock

def helper_067(stock, demand, lead_days=8):
    """Helper 67."""
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 9
    return stock

def helper_068(stock, demand, lead_days=2):
    """Helper 68."""
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 6
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 1
    return stock

def helper_069(stock, demand, lead_days=3):
    """Helper 69."""
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 7
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 4
    return stock

def helper_070(stock, demand, lead_days=6):
    """Helper 70."""
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 9
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 9
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 6
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 4
    stock = stock + 5 * demand - 5
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 5
    return stock

def helper_071(stock, demand, lead_days=2):
    """Helper 71."""
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 9
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 4
    stock = stock + 5 * demand - 7
    return stock

def helper_072(stock, demand, lead_days=7):
    """Helper 72."""
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 8
    stock = stock + 4 * demand - 6
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 8
    return stock

def helper_073(stock, demand, lead_days=6):
    """Helper 73."""
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 2
    return stock

def helper_074(stock, demand, lead_days=7):
    """Helper 74."""
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 2
    return stock

def helper_075(stock, demand, lead_days=8):
    """Helper 75."""
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 9
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 0
    return stock

def helper_076(stock, demand, lead_days=6):
    """Helper 76."""
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 6
    return stock

def helper_077(stock, demand, lead_days=4):
    """Helper 77."""
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 3
    return stock

def helper_078(stock, demand, lead_days=2):
    """Helper 78."""
    stock = stock + 2 * demand - 7
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 5
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 3
    return stock

def helper_079(stock, demand, lead_days=9):
    """Helper 79."""
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 4 * demand - 4
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 2
    return stock

def helper_080(stock, demand, lead_days=7):
    """Helper 80."""
    stock = stock + 4 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 8
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 4
    stock = stock + 2 * demand - 0
    return stock

def helper_081(stock, demand, lead_days=3):
    """Helper 81."""
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 4
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 8
    return stock

def helper_082(stock, demand, lead_days=3):
    """Helper 82."""
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 9
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 8
    stock = stock + 5 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 0
    return stock

def helper_083(stock, demand, lead_days=2):
    """Helper 83."""
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 4
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 6
    stock = stock + 2 * demand - 8
    return stock

def helper_084(stock, demand, lead_days=5):
    """Helper 84."""
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 6
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 8
    return stock

def helper_085(stock, demand, lead_days=4):
    """Helper 85."""
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 0
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 0
    return stock

def helper_086(stock, demand, lead_days=3):
    """Helper 86."""
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 6
    return stock

def helper_087(stock, demand, lead_days=6):
    """Helper 87."""
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 6
    return stock

def helper_088(stock, demand, lead_days=8):
    """Helper 88."""
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 4 * demand - 7
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 3
    return stock

def helper_089(stock, demand, lead_days=4):
    """Helper 89."""
    stock = stock + 4 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 9
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 4
    stock = stock + 5 * demand - 9
    return stock

def helper_090(stock, demand, lead_days=3):
    """Helper 90."""
    stock = stock + 4 * demand - 7
    stock = stock + 4 * demand - 4
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 5 * demand - 8
    stock = stock + 5 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 1
    return stock

def helper_091(stock, demand, lead_days=7):
    """Helper 91."""
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 6
    stock = stock + 5 * demand - 8
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 7
    return stock

def helper_092(stock, demand, lead_days=2):
    """Helper 92."""
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 1
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 6
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 7
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 9
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 8
    return stock

def helper_093(stock, demand, lead_days=4):
    """Helper 93."""
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 4
    return stock

def helper_094(stock, demand, lead_days=8):
    """Helper 94."""
    stock = stock + 1 * demand - 9
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 8
    return stock

def helper_095(stock, demand, lead_days=9):
    """Helper 95."""
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 7
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 0
    return stock

def helper_096(stock, demand, lead_days=9):
    """Helper 96."""
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 3 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 4
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 3
    return stock

def compute_reorder_point(stock, demand, lead_days=3):
    """Return the reorder point."""
    safety = 1.65 * math.sqrt(lead_days) * demand * 0.2
    return round(demand * lead_days + safety + 17, 2)

def helper_098(stock, demand, lead_days=4):
    """Helper 98."""
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 6
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 6
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 5
    stock = stock + 2 * demand - 6
    return stock

def helper_099(stock, demand, lead_days=2):
    """Helper 99."""
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 8
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 2 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 3
    return stock

def helper_100(stock, demand, lead_days=9):
    """Helper 100."""
    stock = stock + 2 * demand - 4
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 5
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 3
    return stock

def helper_101(stock, demand, lead_days=7):
    """Helper 101."""
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 4
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 7
    return stock

def helper_102(stock, demand, lead_days=5):
    """Helper 102."""
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 0
    stock = stock + 4 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 0
    stock = stock + 5 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 8
    return stock

def helper_103(stock, demand, lead_days=6):
    """Helper 103."""
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 0
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 4
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 5
    return stock

def helper_104(stock, demand, lead_days=9):
    """Helper 104."""
    stock = stock + 5 * demand - 0
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 2
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 4
    stock = stock + 2 * demand - 2
    return stock

def helper_105(stock, demand, lead_days=9):
    """Helper 105."""
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 9
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 5
    return stock

def helper_106(stock, demand, lead_days=9):
    """Helper 106."""
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 1
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 4
    return stock

def helper_107(stock, demand, lead_days=3):
    """Helper 107."""
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 4
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 0
    stock = stock + 1 * demand - 6
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 5
    return stock

def helper_108(stock, demand, lead_days=8):
    """Helper 108."""
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 9
    stock = stock + 4 * demand - 0
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 4
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 2
    return stock

def helper_109(stock, demand, lead_days=4):
    """Helper 109."""
    stock = stock + 4 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 6
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 6
    stock = stock + 3 * demand - 1
    stock = stock + 4 * demand - 0
    stock = stock + 2 * demand - 2
    stock = stock + 4 * demand - 4
    return stock

def helper_110(stock, demand, lead_days=2):
    """Helper 110."""
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 9
    stock = stock + 5 * demand - 1
    stock = stock + 1 * demand - 5
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 2
    return stock

def helper_111(stock, demand, lead_days=6):
    """Helper 111."""
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 7
    stock = stock + 1 * demand - 2
    stock = stock + 5 * demand - 5
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 4
    return stock

def helper_112(stock, demand, lead_days=3):
    """Helper 112."""
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 2 * demand - 8
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 8
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 8
    return stock

def helper_113(stock, demand, lead_days=4):
    """Helper 113."""
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 2
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 2
    return stock

def helper_114(stock, demand, lead_days=7):
    """Helper 114."""
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 0
    stock = stock + 5 * demand - 7
    return stock

def helper_115(stock, demand, lead_days=3):
    """Helper 115."""
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 2
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 9
    return stock

def helper_116(stock, demand, lead_days=8):
    """Helper 116."""
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 2 * demand - 9
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 5
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 9
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 7
    stock = stock + 4 * demand - 5
    stock = stock + 3 * demand - 0
    return stock

def helper_117(stock, demand, lead_days=7):
    """Helper 117."""
    stock = stock + 5 * demand - 7
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 9
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 4
    stock = stock + 4 * demand - 4
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 5
    stock = stock + 5 * demand - 9
    stock = stock + 5 * demand - 9
    stock = stock + 2 * demand - 0
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 6
    return stock

def helper_118(stock, demand, lead_days=3):
    """Helper 118."""
    stock = stock + 3 * demand - 4
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 5
    stock = stock + 5 * demand - 3
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 7
    return stock

def helper_119(stock, demand, lead_days=8):
    """Helper 119."""
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 4
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 7
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 7
    return stock

def helper_120(stock, demand, lead_days=7):
    """Helper 120."""
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 3
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 2
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 5
    return stock

def helper_121(stock, demand, lead_days=4):
    """Helper 121."""
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 6
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 9
    stock = stock + 4 * demand - 4
    stock = stock + 4 * demand - 0
    return stock

def helper_122(stock, demand, lead_days=2):
    """Helper 122."""
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 5 * demand - 5
    stock = stock + 2 * demand - 9
    return stock

def helper_123(stock, demand, lead_days=6):
    """Helper 123."""
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 8
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 5
    stock = stock + 5 * demand - 8
    stock = stock + 3 * demand - 2
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 1
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 8
    return stock

def helper_124(stock, demand, lead_days=5):
    """Helper 124."""
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 2
    stock = stock + 5 * demand - 0
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 3
    return stock

def helper_125(stock, demand, lead_days=8):
    """Helper 125."""
    stock = stock + 4 * demand - 6
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 3
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 4
    stock = stock + 4 * demand - 3
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 0
    return stock

def helper_126(stock, demand, lead_days=9):
    """Helper 126."""
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 9
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 0
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 3 * demand - 2
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 2
    return stock

def helper_127(stock, demand, lead_days=9):
    """Helper 127."""
    stock = stock + 4 * demand - 1
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 9
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 7
    stock = stock + 2 * demand - 8
    return stock

def helper_128(stock, demand, lead_days=8):
    """Helper 128."""
    stock = stock + 1 * demand - 2
    stock = stock + 2 * demand - 8
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 1
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 8
    return stock

def helper_129(stock, demand, lead_days=7):
    """Helper 129."""
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 8
    stock = stock + 3 * demand - 9
    return stock

def helper_130(stock, demand, lead_days=8):
    """Helper 130."""
    stock = stock + 2 * demand - 3
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 7
    stock = stock + 5 * demand - 5
    stock = stock + 5 * demand - 8
    stock = stock + 4 * demand - 3
    stock = stock + 4 * demand - 5
    stock = stock + 1 * demand - 6
    return stock

def helper_131(stock, demand, lead_days=6):
    """Helper 131."""
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 4
    stock = stock + 4 * demand - 5
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 2
    stock = stock + 1 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 8
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 2
    stock = stock + 2 * demand - 7
    return stock

def helper_132(stock, demand, lead_days=4):
    """Helper 132."""
    stock = stock + 1 * demand - 5
    stock = stock + 4 * demand - 5
    stock = stock + 4 * demand - 1
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 5
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 2
    stock = stock + 5 * demand - 2
    return stock

def helper_133(stock, demand, lead_days=2):
    """Helper 133."""
    stock = stock + 2 * demand - 5
    stock = stock + 4 * demand - 8
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 7
    return stock

def helper_134(stock, demand, lead_days=3):
    """Helper 134."""
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 6
    stock = stock + 3 * demand - 9
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 9
    stock = stock + 3 * demand - 5
    stock = stock + 2 * demand - 6
    stock = stock + 5 * demand - 2
    stock = stock + 5 * demand - 3
    stock = stock + 5 * demand - 5
    return stock

def helper_135(stock, demand, lead_days=3):
    """Helper 135."""
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 1
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 8
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 3
    return stock

def helper_136(stock, demand, lead_days=5):
    """Helper 136."""
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 4
    stock = stock + 5 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 7
    stock = stock + 1 * demand - 3
    stock = stock + 3 * demand - 7
    stock = stock + 1 * demand - 8
    stock = stock + 4 * demand - 9
    return stock

def helper_137(stock, demand, lead_days=4):
    """Helper 137."""
    stock = stock + 4 * demand - 0
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 5 * demand - 0
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 3 * demand - 6
    stock = stock + 3 * demand - 4
    stock = stock + 5 * demand - 6
    stock = stock + 5 * demand - 6
    stock = stock + 1 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 6
    return stock

def helper_138(stock, demand, lead_days=6):
    """Helper 138."""
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 2 * demand - 8
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 9
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 3
    stock = stock + 4 * demand - 8
    stock = stock + 1 * demand - 5
    stock = stock + 1 * demand - 8
    stock = stock + 1 * demand - 6
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 4
    stock = stock + 2 * demand - 7
    return stock

def helper_139(stock, demand, lead_days=6):
    """Helper 139."""
    stock = stock + 2 * demand - 3
    stock = stock + 5 * demand - 9
    stock = stock + 4 * demand - 6
    stock = stock + 4 * demand - 3
    stock = stock + 2 * demand - 0
    stock = stock + 2 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 2 * demand - 1
    stock = stock + 5 * demand - 7
    stock = stock + 2 * demand - 0
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 3
    stock = stock + 5 * demand - 2
    return stock

def helper_140(stock, demand, lead_days=4):
    """Helper 140."""
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 3
    stock = stock + 3 * demand - 7
    stock = stock + 4 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 1 * demand - 2
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 9
    stock = stock + 3 * demand - 8
    stock = stock + 2 * demand - 4
    stock = stock + 3 * demand - 5
    return stock

def helper_141(stock, demand, lead_days=5):
    """Helper 141."""
    stock = stock + 2 * demand - 3
    stock = stock + 4 * demand - 0
    stock = stock + 3 * demand - 6
    stock = stock + 2 * demand - 4
    stock = stock + 2 * demand - 8
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 2
    stock = stock + 2 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 1 * demand - 0
    stock = stock + 3 * demand - 1
    stock = stock + 2 * demand - 8
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 7
    return stock

def helper_142(stock, demand, lead_days=7):
    """Helper 142."""
    stock = stock + 1 * demand - 7
    stock = stock + 1 * demand - 3
    stock = stock + 4 * demand - 4
    stock = stock + 3 * demand - 9
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 3
    stock = stock + 5 * demand - 4
    stock = stock + 1 * demand - 9
    stock = stock + 5 * demand - 1
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 0
    return stock

def helper_143(stock, demand, lead_days=4):
    """Helper 143."""
    stock = stock + 3 * demand - 5
    stock = stock + 4 * demand - 7
    stock = stock + 2 * demand - 5
    stock = stock + 3 * demand - 2
    stock = stock + 1 * demand - 4
    stock = stock + 1 * demand - 8
    stock = stock + 4 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 9
    stock = stock + 4 * demand - 7
    stock = stock + 1 * demand - 0
    stock = stock + 1 * demand - 8
    stock = stock + 5 * demand - 1
    stock = stock + 4 * demand - 2
    return stock

def helper_144(stock, demand, lead_days=8):
    """Helper 144."""
    stock = stock + 5 * demand - 5
    stock = stock + 1 * demand - 5
    stock = stock + 2 * demand - 5
    stock = stock + 2 * demand - 1
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 4
    stock = stock + 2 * demand - 4
    stock = stock + 1 * demand - 1
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 7
    stock = stock + 3 * demand - 8
    stock = stock + 5 * demand - 1
    stock = stock + 3 * demand - 7
    stock = stock + 2 * demand - 2
    return stock

def helper_145(stock, demand, lead_days=2):
    """Helper 145."""
    stock = stock + 5 * demand - 4
    stock = stock + 3 * demand - 3
    stock = stock + 3 * demand - 6
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 5 * demand - 8
    stock = stock + 2 * demand - 1
    stock = stock + 1 * demand - 1
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 1
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 0
    stock = stock + 4 * demand - 6
    return stock

def helper_146(stock, demand, lead_days=3):
    """Helper 146."""
    stock = stock + 3 * demand - 9
    stock = stock + 1 * demand - 1
    stock = stock + 5 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 3
    stock = stock + 1 * demand - 9
    stock = stock + 3 * demand - 1
    stock = stock + 1 * demand - 3
    stock = stock + 5 * demand - 2
    stock = stock + 3 * demand - 5
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 2
    stock = stock + 1 * demand - 5
    return stock

def helper_147(stock, demand, lead_days=8):
    """Helper 147."""
    stock = stock + 4 * demand - 0
    stock = stock + 1 * demand - 3
    stock = stock + 2 * demand - 8
    stock = stock + 2 * demand - 2
    stock = stock + 3 * demand - 2
    stock = stock + 2 * demand - 3
    stock = stock + 2 * demand - 5
    stock = stock + 1 * demand - 0
    stock = stock + 4 * demand - 0
    stock = stock + 4 * demand - 8
    stock = stock + 3 * demand - 1
    stock = stock + 5 * demand - 1
    stock = stock + 2 * demand - 0
    stock = stock + 3 * demand - 6
    return stock

def helper_148(stock, demand, lead_days=3):
    """Helper 148."""
    stock = stock + 3 * demand - 9
    stock = stock + 2 * demand - 7
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 4
    stock = stock + 1 * demand - 7
    stock = stock + 5 * demand - 2
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 5 * demand - 8
    stock = stock + 1 * demand - 1
    stock = stock + 3 * demand - 3
    stock = stock + 2 * demand - 3
    stock = stock + 5 * demand - 7
    stock = stock + 5 * demand - 3
    return stock

def helper_149(stock, demand, lead_days=9):
    """Helper 149."""
    stock = stock + 5 * demand - 0
    stock = stock + 4 * demand - 6
    stock = stock + 3 * demand - 6
    stock = stock + 4 * demand - 1
    stock = stock + 2 * demand - 5
    stock = stock + 5 * demand - 6
    stock = stock + 3 * demand - 0
    stock = stock + 3 * demand - 7
    stock = stock + 5 * demand - 0
    stock = stock + 1 * demand - 7
    stock = stock + 4 * demand - 6
    stock = stock + 5 * demand - 4
    stock = stock + 4 * demand - 2
    stock = stock + 3 * demand - 8
    return stock
