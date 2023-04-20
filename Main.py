import time

from gtmetrix import *
from xlwt import Workbook
import xlwt
import telebot as telebot


bot_token = '5996815449:AAHzzYi51QJeXSG2hDJaLoltSpNWjh0a6P4'
chat_id = 174245202
channel_id = '-1001774709225'
telegram_bot = telebot.TeleBot(bot_token, parse_mode=None)

# Workbook is created
wb = Workbook()

# Assigning Max Column Width for XL file
max_length_url = [0]
max_length_pagespeed_issues = [0]
max_length_yslow_issues = [0]
tracking_rows_xl = [0, 0, 0, 0, 0]


def extract_data(url_name, location_name, location_id, email_id, api_key):
    """Here we are creating API data dictionary which consist of all information which we have to insert into XL regarding every URL"""
    gt = GTmetrixInterface(email_id, api_key)
    pagespeed_issue_object = interface.IdentifyingPageSpeedIssues(email_id, api_key)
    yslow_issue_object = interface.IdentifyingYslowIssues(email_id, api_key)
    my_test = gt.start_test(url_name, location_id)
    try:
        api_data = my_test.fetch_results()
    except:
        print('Error in fetching API data')
    api_data['pagespeed_issues'] = pagespeed_issue_object.fetch_results(api_data['pagespeed_url'])
    api_data['yslow_issues'] = yslow_issue_object.fetch_results(api_data['yslow_url'])
    api_data['url'] = url_name
    api_data['location_name'] = location_name
    inserting_data_into_xl(**api_data)


def init_xl_file():
    sheet1 = wb.add_sheet('London')
    # Sheet1 for London
    sheet1.write(0, 0, 'URL');
    sheet1.write(0, 1, 'Page Speed Score');
    sheet1.write(0, 2, 'Yslow Score');
    sheet1.write(0, 3, 'Fully Loaded Time');
    sheet1.write(0, 4, 'Total Page Size');
    sheet1.write(0, 5, 'Request');
    sheet1.write(0, 6, 'PageSpeed Issues');
    sheet1.write(0, 7, 'Yslow Issues')
    # Setting Column Width which will not change
    sheet1.col(1).width = len('Page Speed Score') * 256;
    sheet1.col(2).width = len('Yslow Score') * 256;
    sheet1.col(3).width = len('Fully Loaded Time') * 256;
    sheet1.col(4).width = len('Total Page Size') * 256;
    sheet1.col(5).width = (len('Requests') + 1) * 256


def inserting_data_into_xl(**api_data):
    sheet1 = wb.get_sheet(0)
    # Setting Column Width which vary with input
    if (len(api_data['url']) > max(max_length_url)):
        max_length_url.append(len(api_data['url']))
        sheet1.col(0).width = (max(max_length_url)) * 256
    if (len(api_data['pagespeed_issues']) > max(max_length_pagespeed_issues)):
        if ((len(api_data['pagespeed_issues'])) > 256):
            max_length_pagespeed_issues.append(255)
        elif ((len(api_data['pagespeed_issues'])) < 256):
            max_length_pagespeed_issues.append(len(api_data['pagespeed_issues']))
        sheet1.col(6).width = (max(max_length_pagespeed_issues)) * 256
    if (len(api_data['yslow_issues']) > max(max_length_yslow_issues)):
        if ((len(api_data['yslow_issues'])) > 256):
            max_length_yslow_issues.append(255)
        elif ((len(api_data['yslow_issues'])) < 256):
            max_length_yslow_issues.append(len(api_data['yslow_issues']))
        sheet1.col(7).width = (max(max_length_yslow_issues)) * 256
    # Inserting Data Into Sheetl for Dallas Location
    if api_data['location_name'] == sheet1.name:
        tracking_rows_xl[0] += 1
        # Specifying style
        style = xlwt.easyxf('align: horiz left')
        # Grading for Pagespeed Score
        if int(api_data['pagespeed_score']) >= 90:
            pagespeed_grade = '✅ A '
        elif (int(api_data['pagespeed_score']) >= 80) & (int(api_data['pagespeed_score']) < 90):
            pagespeed_grade = '🟩 B '
        elif (int(api_data['pagespeed_score']) >= 70) & (int(api_data['pagespeed_score']) < 80):
            pagespeed_grade = '🟧 C '
        elif (int(api_data['pagespeed_score']) >= 60) & (int(api_data['pagespeed_score']) < 70):
            pagespeed_grade = '🟥 D '
        elif int(api_data['pagespeed_score']) < 60:
            yslow_grade = '🟪 E'

        # Grrading For Yslow Score
        if int(api_data['yslow_score']) >= 90:
            yslow_grade = '✅ A '
        elif (int(api_data['yslow_score']) >= 80) & (int(api_data['yslow_score']) < 90):
            yslow_grade = '🟩 B '
        elif (int(api_data['yslow_score']) >= 70) & (int(api_data['yslow_score']) < 80):
            yslow_grade = '🟧 C '
        elif (int(api_data['yslow_score']) >= 60) & (int(api_data['yslow_score']) < 70):
            yslow_grade = '🟥 D '
        elif int(api_data['yslow_score']) < 60:
            yslow_grade = '🟪 E '

        total_page_size = round(api_data['total_page_size'] / 2 ** 20, 2)
        fully_loaded_time = round(api_data['fully_loaded_time'] / 1000, 2)
        # Inserting Data
        try:
            sheet1.write(tracking_rows_xl[0], 0, api_data['url'], style)
            sheet1.write(tracking_rows_xl[0], 1, (pagespeed_grade + '(' + str(api_data['pagespeed_score']) + '%' + ')'),
                         style)
            sheet1.write(tracking_rows_xl[0], 2, (yslow_grade + '(' + str(api_data['yslow_score']) + '%' + ')'), style)
            sheet1.write(tracking_rows_xl[0], 3, str(fully_loaded_time) + 's', style)
            sheet1.write(tracking_rows_xl[0], 4, str(total_page_size) + 'MB', style)
            sheet1.write(tracking_rows_xl[0], 5, api_data['requests'], style)
            sheet1.write(tracking_rows_xl[0], 6, api_data['pagespeed_issues'], style)
            sheet1.write(tracking_rows_xl[0], 7, api_data['yslow_issues'], style)
        except KeyError:
            print('Kindly close the open file and then rum it')

    message = f"<strong>{api_data['url']}</strong>\n"\
          f"<strong>Pagespeed:</strong> {pagespeed_grade + '(' + str(api_data['pagespeed_score']) + '%' + ')'}\n"\
          f"<strong>YSLOW:</strong> {yslow_grade + '(' + str(api_data['yslow_score']) + '%' + ')'}\n"\
          f"<strong>Full load:</strong> {str(fully_loaded_time) + 's'}\n"
    telegram_bot.send_message(channel_id, message, disable_notification=True, parse_mode="html", disable_web_page_preview=True)
    try:
        wb.save('Final_Output.xls')
    except PermissionError:
        print('Kindly close the open file and then rum it')


if __name__ == '__main__':
    email_id = 'webmaster@appbakery.it'
    api_key = 'd480bf26ceb7ceb651341b10618b137c'
    url_list = ['https://gicaelettronica.com/',
                'https://gicaelettronica.com/categoria-prodotto/telefonia-e-accessori/',
                'https://gicaelettronica.com/prodotto/apple-iphone-14-pro-256gb-silver/',
                'https://giuseppeconca.com/',
                'https://giuseppeconca.com/shop/',
                'https://giuseppeconca.com/shop/sandalo-rio-2623-in-raso-viola/',
                'https://www.maemiofficial.com/',
                'https://www.maemiofficial.com/negozio/?filter_taglia=43',
                'https://www.maemiofficial.com/prodotto/sandalo-in-lame-multicolor-rame-argento-platino/'
                ]

    location_with_id = {'London': '2'}
    # Initializing XL File
    init_xl_file()
    for location_name, location_id in location_with_id.items():
        for url in url_list:
            extract_data(url, location_name, location_id, email_id, api_key)
            time.sleep(30)
