from functions import *

if __name__ == '__main__':

    with keyboard.Listener(on_press=on_press) as listener:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")

        price_df = pd.DataFrame(columns=['type', 'name', '1x', '10x', '100x'])

        price_df = scan_hdv(vendeur_ressources[:2], vendeur_ressources[2], price_df)
        change_HDV(pos_transpo_ressource, 6)

        price_df = scan_hdv(vendeur_bucheron[:2], vendeur_bucheron[2], price_df)
        change_HDV(pos_transpo_bucheron, 9)

        price_df = scan_hdv(vendeur_mineur[:2], vendeur_mineur[2], price_df)
        # change_HDV(pos_transpo_bucheron, 9)

        price_df.drop_duplicates(subset='name', keep='last')

    if os.path.isfile('{}.xlsx'.format(timestampStr)):
        book = load_workbook('{}.xlsx'.format(timestampStr))
        writer = pd.ExcelWriter('{}.xlsx'.format(timestampStr), engine='openpyxl')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}

        for sheetname in writer.sheets:
            price_df.to_excel(writer, sheet_name=sheetname, startrow=writer.sheets[sheetname].max_row,
                              index=False,
                              header=False)
        writer.close()
    else:
        writer = pd.ExcelWriter('{}.xlsx'.format(timestampStr), engine='xlsxwriter')
        price_df.to_excel(writer, sheet_name='Ressources', index=False)
        writer.save()
