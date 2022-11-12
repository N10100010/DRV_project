from world_rowing import api
import pandas as pd


def main():
    # the current result is always 1000 rows long. Why is that?
    races = api.get_races()
    events = api.get_events()
    comps = api.get_competitions()

    races_rsc = races.rsccode.unique()
    #events_rsc = events.rsccode.unique()

    def merge_events_races(races: pd.DataFrame, events: pd.DataFrame):
        # todo: find out who with who with what

        # todo: the rsccodes of races is more profane. The starting substring of the rsccode from races and events are the same
        #pd.concat([races[['eventid', 'rsccode']], events[['id', 'rsccode']]], axis=1)

        # todo: no connection seen between the following subparts
        #pd.concat(
        #    [
        #        comps[['id', 'competitioncode', 'competitiontypeid']],
        #        events[['id', 'competitionid', 'competitiontypeid']]
        #    ], axis=1)


        #merged = pd.merge(left=races, right=events, left_on='RscCode', right_on='RscCode')
        #return merged
        print()

    # merge_events_races(races=races, events=events)


    print()

if __name__ == "__main__":
    main()