import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xtrader.apis import rest

__all__ = ['rest']