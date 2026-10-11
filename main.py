import requests
import pandas as pd
import argparse



BASE_URL = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='
MAX_XP = 13034431


def fetch_data(player_name):
    stat_dictionary = {}
    url = BASE_URL + player_name
    response = requests.get(url)
    data = response.text
    td = data.split('\n')
    for count, row in enumerate(td):
        row = row.split(',')
        if len(row) > 2:
            stat_dictionary[count] = row
    return stat_dictionary

def process_data(stat_dictionary):
    df = pd.DataFrame(stat_dictionary)
    df = df.transpose()
    df.columns = ['Rank','Level','XP']
    df.index = ['Total', 
                'Attack',
                'Defence',
                'Strength',
                'Hitpoints',
                'Ranged',
                'Prayer',
                'Magic',
                'Cooking',
                'Woodcutting',
                'Fletching',
                'Fishing',
                'Firemaking',
                'Crafting',
                'Smithing',
                'Mining',
                'Herblore',
                'Agility',
                'Thieving',
                'Slayer',
                'Farming',
                'Runecraft',
                'Hunter',
                'Contstruction',
                'Sailing']
    df.drop('Total', inplace =True)
    df['max_xp'] = MAX_XP
    df[['Level','Rank','XP']] = df[['Level','Rank','XP']].astype(int)
    df['xp_till_max'] = df.apply(lambda x: 0 if x['Level'] == 99 else MAX_XP - x['XP'], axis = 1)
    df['xp_towards_max'] = df.apply(lambda x: MAX_XP if x['Level'] == 99 else x['XP'], axis = 1)
    df.loc['Total'] = df.sum(numeric_only = True)
    df['Percent Finished'] = df['xp_towards_max']/df['max_xp'] * 100
    df.drop('max_xp', axis = 1, inplace = True)
    return df

def main():
    parser = argparse.ArgumentParser(description='Calculate max percentage for OSRS player')
    parser.add_argument('player_name', help='Name of the player')
    args = parser.parse_args()

    stat_dictionary = fetch_data(args.player_name)
    df = process_data(stat_dictionary)
    df.to_csv(f"{args.player_name}_stats.csv")
    for skill in df.loc[df['Percent Finished'] < 100].sort_values('Percent Finished').index:
        if skill != 'Total':
            print(f"{skill}: {df.loc[skill, 'XP']} {df.loc[skill, 'Percent Finished']:.2f}%")
    print(f"Total: {df.loc['Total', 'XP']} {df.loc['Total', 'Percent Finished']:.2f}%")

if __name__ == '__main__':
    main()