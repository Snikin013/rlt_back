import uuid
import pandas as pd
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import FileResponse

from os import getcwd, listdir

from starlette import status

from app.models import connect_db# User#, Stream, AuthToken, StreamStatus
from app.forms import check_inn

import numpy as np

router = APIRouter()

#---------------------------------------------------------------------------------------

# @router.options('/login', name='CHECKRULS', )
# def checkcorp( ):
#     print('chekup')
#     return {}

#---------------------------------------------------------------------------------------

@router.post('/data', name='user:takeData')
def take_data_second(user_form: check_inn = Body(..., embed=True), database=Depends(connect_db)):

    result = {}
    INN = user_form.innform

    sql = '''
        select 
            include_reason, 
            EXTRACT(YEAR from cast(exclude_date as date)) as year, 
            EXTRACT(MONTH  from cast(exclude_date as date)) as month
        from public.rnp
        where inn = \'{}\'
        limit 1
        ;'''.format(INN)

    sql_egrul = '''
        select 
            extract(year from now()) - extract(year from cast(registration_date as date)) as year, 
            capital_size, okved_basic_code,  
            now()::date -  cast(registration_date as date) as day_dif
        from public.egrul_info
        where inn = \'{}\'
        limit 1'''.format(INN)

    sql_contr = '''
        select customer_inn, count(*)
        from public.contract_main_info
        where customer_inn = \'{}\'
        group by customer_inn
        '''.format(INN)

    df = pd.read_sql(sql, connect_db())
    egrul = pd.read_sql(sql_egrul, connect_db())
    egrul['capital_size'].fillna(0, inplace=True)
    if egrul['capital_size'].values == ['']:
        egrul['capital_size'] = 0
    contr = pd.read_sql(sql_contr, connect_db())
 

    if egrul.shape[0] == 1:
        result['found'] = True
        result['inn'] = INN
        result['name'] = INN
#-----------------------TIMELIFE-----------------------------------------------------------------
        if int(egrul['year'].iloc[0]) < 1:
            result['years'] = {'status': 1, 'value': '{} years'.format(int(int(egrul['day_dif']) / 365))}
        elif int(egrul['year'].iloc[0]) >= 1 and int(egrul['year']) < 3:
            result['years'] = {'status': 2, 'value': '{} years'.format(int(int(egrul['day_dif']) / 365))}
        elif int(egrul['year'].iloc[0]) >= 3 and int(egrul['year']) < 10:
            result['years'] = {'status': 3, 'value': '{} years'.format(int(int(egrul['day_dif']) / 365))}
        elif int(egrul['year'].iloc[0]) >= 10:
            result['years'] = {'status': 4, 'value': '{} years'.format(int(int(egrul['day_dif']) / 365))}
#-----------------------CAPITAL-------------------------------------------------------------------
        if int(egrul['capital_size'].iloc[0]) < 10**6:
            result['capital'] = {'status': 1, 'value': '{} rub'.format(int(egrul['capital_size']))}
        elif int(egrul['capital_size'].iloc[0]) >= 10**6 and int(egrul['capital_size']) < 10**9 * 2:
            result['capital'] = {'status': 2, 'value': '{} rub'.format(int(egrul['capital_size']))}
        elif int(egrul['capital_size'].iloc[0]) >= 10**9 * 2 and int(egrul['capital_size']) < 10**10:
            result['capital'] = {'status': 3, 'value': '{} rub'.format(int(egrul['capital_size']))}
        elif int(egrul['capital_size'].iloc[0]) >= 10**10:
            result['capital'] = {'status': 4, 'value': '{} rub'.format(int(egrul['capital_size']))}
#-----------------------CONTRACTS-----------------------------------------------------------------
        if int(contr['count'].iloc[0]) <= 5:
            result['contracts'] = {'status': 1, 'value': '{} контрактов'.format(int(contr['count']))}
        elif int(contr['count'].iloc[0]) > 5 and int(contr['count']) < 50:
            result['contracts'] = {'status': 2, 'value': '{} контрактов'.format(int(contr['count']))}
        elif int(contr['count'].iloc[0]) >= 50 and int(contr['count']) < 500:
            result['contracts'] = {'status': 3, 'value': '{} контрактов'.format(int(contr['count']))}
        elif int(contr['count'].iloc[0]) >= 500:
            result['contracts'] = {'status': 4, 'value': '{} контрактов'.format(int(contr['count']))}

    else:
        result['found'] = False


    if df.shape[0] == 1:
        if int(df['year']) < pd.datetime.now().year:
            result['badlist'] = {'status': 1, 'value': df['include_reason']}
    else:
        result['badlist'] = {'status': 0, 'value': "Чист как белый лист"}

    return result


    #list(pd.read_sql(sql, connect_db()).to_dict('index').values())

    # return {
    #         'found': True,
    #         'inn': INN,
    #         'name': 'ООО Ромашка',
    #         'years': {'status': 1, 'value': "3 месяца"},
    #         'capital': {'status': 3, 'values': "10 млрд"},
    #         'contracts': {'status': 1, 'value': "2 контракта"},
    #         'badlist': {'status': 1, 'value': "Потому-что негодяй"}
    #         }

#-----------------------------------------------------------------------------------------

# {
# found: True or False,
# inn: "1234567890",

# years: {status: 1 или 2 или 3 или 4 будет,
#             value: "3 месяца"
#             },
# capital: {status: 1 или 2 или 3 или 4 будет,
#               values: "10млрд"},
# contracts: {status: 1 или 2 или 3 или 4 будет,
#                    value: "200 контрактов"},
# badlist: {status: 1 or 2,
#               value: "причина постановки"
# }




# @router.get('/get_recomendation', name='user:recomendation')
# def get_recomendation(database=Depends(connect_db)):


#     sql = '''
#             select td.tnved_cat, o.napr, 
#                  sum(case when o."year" = 2019 then o.stoim end) as "2019",
#                  sum(case when o."year" = 2020 then o.stoim end) as "2020",
#                  sum(case when o."year" = 2021 then o.stoim end) as "2021"

#             from operations o 
#                  join tnved_desc td 
#                  on o.tnved = td.tnved_id

#             group by td.tnved_cat, 
#                      o.napr;

#             '''


#     piv = pd.read_sql(sql, connect_db())


#     return list(result.head(100).to_dict('index').values())

#-----------------------------------------------------------------------------------------

# @router.get('/download/{name_file}', name='user:file_of_recomendation')
# def get_file_rec(name_file: str):

#     return FileResponse(path=getcwd() + "/" + name_file, media_type='application/octet-stream', filename=name_file)










