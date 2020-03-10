#!/usr/local/bin/python3
#
# LaunchBar Action Script
#
"""LaunchBar Action Script for changing Wechat Pay csv to MoneyWiz style."""
import sys
import os
import pandas as pd
import csv

# Your account name for Wechat Pay in MoneyWiz
wechat_account_name = '微信'

# %%
for index, arg in enumerate(sys.argv[1:]):
    cash_flow_df = pd.read_csv(arg,
                               header=16,
                               usecols=range(6),
                               parse_dates=[0],
                               infer_datetime_format=True,
                               na_values='/')
    # cash_flow_df = cash_flow_df.convert_dtypes()

    # %%
    cash_flow_df = cash_flow_df.rename(
        columns={
            '交易时间': 'Date',
            '交易类型': 'TradeType',
            '交易对方': 'Payee',
            '商品': 'Description',
            '收/支': 'Direction',
            '金额(元)': 'Amount'
        })

    # %%
    # Change to the correct data type.
    cash_flow_df['Date'] = cash_flow_df['Date'].dt.strftime('%d-%m-%Y')
    cash_flow_df['Amount'] = cash_flow_df['Amount'].apply(
        lambda x: pd.to_numeric(x.replace('¥', '')))
    cash_flow_df['Direction'] = cash_flow_df['Direction'].astype('category')

    # %%
    # change sign to the expense.
    cash_flow_df['Amount'] = cash_flow_df.apply(
        lambda row: -row['Amount']
        if row['Direction'] == '支出' else row['Amount'],
        axis=1)

    # %%
    # select red evenlope
    red_envelope: pd.DataFrame = cash_flow_df.loc[cash_flow_df.TradeType ==
                                                  '微信红包'].copy(False)

    # %%
    # add Accounts and Category.
    red_envelope.Description = red_envelope.TradeType
    red_envelope['Account'] = wechat_account_name
    red_envelope['Category'] = '其他 > 红包'

    # %%
    # set file name.
    origin_file_path = os.path.dirname(arg)
    if index == 0:
        saved_file_name = origin_file_path + '/moneyWiz_style.csv'
    else:
        saved_file_name = origin_file_path + '/moneyWiz_style(' + str(
            index) + ').csv'

    # %%
    red_envelope.to_csv(path_or_buf=saved_file_name,
                        columns=[
                            'Date', 'Description', 'Payee', 'Amount',
                            'Account', 'Category'
                        ],
                        index=False,
                        quoting=csv.QUOTE_ALL,
                        quotechar='"')
