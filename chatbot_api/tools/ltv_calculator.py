import random
import time

def get_advertiser_ltv_value(advertiser) -> int | str:
    """Dummy function to generate ltv value"""

    # if advertiser not in ["A", "B", "C", "D"]:
        # return f"advertiser {advertiser} does not exist"

    # Simulate API call delay
    time.sleep(1)

    return random.randint(0, 10000)