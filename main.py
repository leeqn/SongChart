import argparse
from visualisation import get_info
from sqlalchemy import create_engine
import settings

def main():
    parser = argparse.ArgumentParser(description='Sorting function')
    parser.add_argument('-d','--days',help='Number of days to sort',type=int,default=None)
    parser.add_argument('-m','--module',help='track, tag',type=str,default=None)
    args = parser.parse_args()

    engine = create_engine(settings.POSTGRES)
    get_info(engine, days=args.days,module=args.module)

if __name__ == '__main__':
    main()