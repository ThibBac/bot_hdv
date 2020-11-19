from functions import *

if __name__ == '__main__':

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S")

    if os.path.isfile('out_1x.xlsx'):
        price_1x_df = pd.read_excel('out_1x.xlsx', index_col=0)
        price_1x_df = price_1x_df.append(pd.Series(name=timestampStr))
    else:
        price_1x_df = pd.DataFrame()
        price_1x_df = price_1x_df.append(pd.Series(name=timestampStr))

    if os.path.isfile('out_10x.xlsx'):
        price_10x_df = pd.read_excel('out_10x.xlsx', index_col=0)
        price_10x_df = price_10x_df.append(pd.Series(name=timestampStr))
    else:
        price_10x_df = pd.DataFrame()
        price_10x_df = price_10x_df.append(pd.Series(name=timestampStr))

    if os.path.isfile('out_100x.xlsx'):
        price_100x_df = pd.read_excel('out_100x.xlsx', index_col=0)
        price_100x_df = price_100x_df.append(pd.Series(name=timestampStr))
    else:
        price_100x_df = pd.DataFrame()
        price_100x_df = price_100x_df.append(pd.Series(name=timestampStr))

    with keyboard.Listener(on_press=on_press) as listener:

        price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_ressources[:2], vendeur_ressources[2],
                                                            price_1x_df, price_10x_df, price_100x_df)
        change_HDV(pos_transpo_ressource, 6)

        price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_bucheron[:2], vendeur_bucheron[2],
                                                            price_1x_df, price_10x_df, price_100x_df)
        change_HDV(pos_transpo_bucheron, 9)

        price_1x_df, price_10x_df, price_100x_df = scan_hdv(vendeur_mineur[:2], vendeur_mineur[2],
                                                            price_1x_df, price_10x_df, price_100x_df)
        # change_HDV(pos_transpo_bucheron, 9)

    writer = pd.ExcelWriter('out.xlsx', engine='xlsxwriter')
    price_1x_df.to_excel(writer, sheet_name='1x')
    price_10x_df.to_excel(writer, sheet_name='10x')
    price_100x_df.to_excel(writer, sheet_name='100x')
    writer.save()
