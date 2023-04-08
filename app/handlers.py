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

    df = pd.read_sql(sql, connect_db())

    # if int(df['year']) < pd.datetime.now().year:
    #     result['badlist'] = {status: 1, value: df['include_reason']}
    #pd.datetime.now().month

    #list(pd.read_sql(sql, connect_db()).to_dict('index').values())

    return {
            'found': True,
            'inn': "1234567890",
            'name': 'ООО Ромашка',
            'years': {'status': 1, 'value': "3 месяца"},
            'capital': {'status': 3, 'values': "10 млрд"},
            'contracts': {'status': 1, 'value': "2 контракта"},
            'badlist': {'status': 1, 'value': "Потому-что негодяй"}
            }

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










