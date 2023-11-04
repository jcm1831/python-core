import json
from on_demand_stops_check import check_on_demand_stops


if __name__ == '__main__':

    def main():
        database = json.loads(input())
        check_on_demand_stops(database)


    main()
