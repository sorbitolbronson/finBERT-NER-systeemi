import requests
import pandas as pd
import re


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


def join_annotations(ann_list):
    """Joins different types of annotations to list of tuples [('<annotation>', '<type>')]"""

    i_reg = re.compile(r'(.*)\tI-([A-Z]*)')
    b_reg = re.compile(r'(.*)\tB-([A-Z]*)')

    annotations = []
    last_cat = None

    for org in ann_list:
        if match := b_reg.search(org):
            name = match.group(1)
            last_cat = cat = match.group(2)
            annotations.append((name, cat))
        elif match := i_reg.search(org):
            name = match.group(1)
            cat = match.group(2)
            if last_cat == cat:
                annotations[-1] = f'{annotations[-1][0]} {name}', annotations[-1][1]
            else:
                annotations.append((name, cat))

    return annotations


def main():
    df = pd.read_csv('S-ryhmä_tweet_sentiments.csv')

    # taulukosta otetaan 100 kpl otos
    df2: pd.DataFrame = df
    #   df2: pd.DataFrame = df.iloc[:10]

    df2['annotations'] = None

    pd.set_option('display.max_rows', df2.shape[0] + 1)

    # regex for matching B-*** and I-*** annotations, used later
    i_reg = re.compile(r'(.*)\tI-([A-Z]*)')
    b_reg = re.compile(r'(.*)\tB-([A-Z]*)')

    for index, row in df2.iterrows():
        text = row['cleanContent']

        # Query Finbert-NER
        response = requests.get('http://localhost:5000/', data=text.encode())

        words = response.text.split("\n")

        # filter entities that have annotations
        def filter_organisations(ent):
            return any([b_reg.match(ent), i_reg.match(ent)])

        annotations = filter(filter_organisations, words)

        joined = join_annotations(annotations)

        df2.at[index, 'annotations'] = joined

    print(df2[['cleanContent', 'annotations']])

    df2[['cleanContent', 'annotations']].to_csv('test.csv')


if __name__ == '__main__':
    main()
