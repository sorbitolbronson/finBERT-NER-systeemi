from functools import reduce

import requests
import json
import pandas as pd


# jsonista taulukko

def join_b_organisations(org_list):
    orgs = []
    for org in org_list:
        name, org = org.split('\t')
        if org == 'I-ORG':
            if len(orgs) > 0:
                orgs[-1] = orgs[-1][0] + name, orgs[-1][1]
            else:
                orgs.append((name, org))
        if org == 'B-ORG':
            orgs.append((name, org))
    return orgs


def main():
    df = pd.read_csv('S-ryhmä_tweet_sentiments.csv')

    # taulukosta otetaan 100 kpl otos

    df2: pd.DataFrame = df.iloc[:99, :]
    df2['B-ORG'] = None

    pd.set_option('display.max_rows', df2.shape[0] + 1)

    l = []

    # l�het�n otoksen tekstit localhostiin

    for index, row in df2.iterrows():
        text = row['cleanContent']

        response = requests.get('http://localhost:5000/', data=text.encode())

        x = response.text.split("\n")

        def filter_organisations(ent):
            if 'B-ORG' in ent:
                return True
            if 'I-ORG' in ent:
                return True
            return False

        oganizations = filter(filter_organisations, x)
        joined = join_b_organisations(oganizations)

        df2.at[index, 'B-ORG'] = joined

    print(df2[['cleanContent', 'B-ORG']])


if __name__ == '__main__':
    main()
