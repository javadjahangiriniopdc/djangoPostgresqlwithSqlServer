from django.shortcuts import render

from MyApp.models import MaxSanad
from djangoPostgresqlwithSqlServer.SqlServerConnect import SqlServerConnect
import pyodbc


def connsql(request):
    server = 'localhost'
    database = 'otherdb'
    username = 'sa'
    password = '123'
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    cursor.execute("SELECT   max(id) FROM  Sanad ")
    max_id = cursor.fetchone()
    # return render(request, 'index.html', {'SqlServerConnect': result})

    max_sanad = MaxSanad.objects.get(id=1)
    if max_id[0] > max_sanad.max_sanad_id:
        # get diff data
        myquery = "SELECT   id, name FROM  Sanad where id > " + str(max_sanad.max_sanad_id) + ""
        cursor.execute(myquery)
        result = cursor.fetchall()

        # update in postgress
        max_sanad.max_sanad_id = max_id[0]
        max_sanad.save()

        return render(request, 'index.html', {'SqlServerConnect': result})
    else:
        return render(request, 'nochange.html', {'max_id': max_id[0]})
