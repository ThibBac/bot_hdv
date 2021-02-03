from functions import *

if __name__ == '__main__':

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("'%d/%m/%y-%H:%M'")
    # create_all_csv(timestampStr)

    price_1x_df = check_if_file_exist('ressources_1x.csv', timestampStr)
    price_10x_df = check_if_file_exist('ressources_10x.csv', timestampStr)
    price_100x_df = check_if_file_exist('ressources_100x.csv', timestampStr)
    price_item_df = check_if_file_exist('items.csv', timestampStr)

    with keyboard.Listener(on_press=on_press) as listener:

        for key, hdv in hdv_dict.items():
            if hdv['type'] == "ressource":
                price_1x_df, price_10x_df, price_100x_df = scan_hdv(hdv, key, price_1x_df, price_10x_df, price_100x_df)
                change_HDV(hdv['pos_transpo'], hdv['pos_next_hdv'])
            else:
                continue
                # price_item_df, _, _ = scan_hdv(hdv, key, price_item_df, None, None)
                # change_HDV(hdv['pos_transpo'], hdv['pos_next_hdv'])

    price_1x_df.to_csv('ressources_1x.csv')
    price_10x_df.to_csv('ressources_10x.csv')
    price_100x_df.to_csv('ressources_100x.csv')
    price_item_df.to_csv('items.csv')
