from NBAPropFinder.NBAPropFinder import NBAPropFinder
from WNBAPropFinder.WNBAPropFinder import WNBAPropFinder
from NFLPropFinder.NFLPropFinder import NFLPropFinder
"""
Reccomended to run one prop finder at a time by commenting all the other ones.
"""

# nba_props = NBAPropFinder()
wnba_props = WNBAPropFinder()
wnba_props.save_to_json()
# nfl_props = NFLPropFinder()