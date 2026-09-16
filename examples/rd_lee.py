"""Regression-discontinuity example: incumbency advantage in U.S. Senate races.

``sp.datasets.lee_2008_senate()`` returns the Senate extract distributed with
R's ``rdrobust`` (Lee's close-election design; not Lee's House data):
``x`` is the vote-share margin at election t, ``y`` the vote share at t+2.
"""

import statspai as sp


def main() -> None:
    data = sp.datasets.lee_2008_senate()
    result = sp.rdrobust(data=data, y="y", x="x", c=0)
    print(result.summary())


if __name__ == "__main__":
    main()
