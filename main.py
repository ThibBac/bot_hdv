from functions import *

if __name__ == '__main__':
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("'%m/%d/Y-%H:%M'")

    price_1x_df = check_if_file_exist('ressources_1x.csv', timestampStr)
    price_10x_df = check_if_file_exist('ressources_10x.csv', timestampStr)
    price_100x_df = check_if_file_exist('ressources_100x.csv', timestampStr)
    price_item_df = check_if_file_exist('items.csv', timestampStr)

    with keyboard.Listener(on_press=on_press) as listener:
        # price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_ressources[:2], vendeur_ressources[2],
        #                                                     price_1x_df, price_10x_df, price_100x_df)
        # change_HDV(pos_transpo_ressource, 6)
        #
        # price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_bucheron[:2], vendeur_bucheron[2],
        #                                                     price_1x_df, price_10x_df, price_100x_df)
        # change_HDV(pos_transpo_bucheron, 9)
        #
        # price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_mineur[:2], vendeur_mineur[2],
        #                                                     price_1x_df, price_10x_df, price_100x_df)
        change_HDV(pos_transpo_mineur, 2)

        price_item_df, _, _ = scan_hdv(vendeur_bijou[:2], vendeur_bijou[2],
                                       price_item_df, price_10x_df, price_100x_df)
        change_HDV(pos_transpo_bijou, 6)

        price_item_df, _, _ = scan_hdv(vendeur_cordo[:2], vendeur_cordo[2],
                                       price_item_df, price_10x_df, price_100x_df)
        change_HDV(pos_transpo_cordo, 16)

        price_item_df, _, _ = scan_hdv(vendeur_tailleur[:2], vendeur_tailleur[2],
                                       price_item_df, price_10x_df, price_100x_df)

    price_1x_df.to_csv('ressources_1x.csv')
    price_10x_df.to_csv('ressources_10x.csv')
    price_100x_df.to_csv('ressources_100x.csv')

    price_item_df.to_csv('items.csv')
