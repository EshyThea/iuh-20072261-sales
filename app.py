from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

import dash_bootstrap_components as dbc


# TẢI DỮ LIỆU TỪ FIRESTORE
#iuh-20072261-78278-firebase-adminsdk-3p9wr-b5414c48e1.json
cred = credentials.Certificate("./iuh-20072261-c1a3b-firebase-adminsdk-zd6f7-4322928f62.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20072261').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
#doanh so
doanhSoSale = round(df[['SALES']].agg('sum'),2)
#Loi nhuan
df["Total"] =df['SALES'] - df["PRICEEACH"] * df["QUANTITYORDERED"]


loiNhuan = round(df[['SALES']].agg('sum')-np.sum(df["PRICEEACH"] * df["QUANTITYORDERED"]),2)

# Top doanh so
topDoanhSo = df.groupby(['CATEGORY'])['SALES'].sum().max()

# Top Loi Nhuan
topLoiNhuan = df.groupby(['CATEGORY'])['Total'].sum().max()


# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Xây dựng danh mục sản phẩm tìm năng"
# doanh thu theo năm
figDoanhSo = px.histogram(df, x="YEAR_ID", y="SALES", 
barmode="group", color="YEAR_ID", title='Doanh số bán hàng theo năm', histfunc = "sum",
labels={'YEAR_ID':'Từ năm 2003, 2004 và 2005', 'SALES':'Doanh số'})
# doanh số theo danh mục trong năm
figDoanhSoTheoDanhMucTheoNam = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Danh mục','SALES':'Doanh số'},
title='Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm')


listLoiNhuan = df.groupby(['YEAR_ID'])['Total'].agg(['sum'])
dfGroup = df.groupby('YEAR_ID').sum('SALES')
dfGroup = dfGroup.reset_index()
#lợi nhuận theo năm
figLoiNhuanTheoNam = px.line(
    dfGroup, x='YEAR_ID', y='Total', title='Lợi nhuận bán hàng theo năm')


# lợi nhuận theo danh mục trong năm
figLoiNhuanTheoDanhMucTheoNam = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='Total',
color='Total',
labels={'parent':'Năm', 'labels':'Danh mục','Total':'Lợi nhuận'},
title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm')



app.layout = html.Div(
    html.Div(
    children=[
        html.Div([
            html.Div(
                dbc.Row(
                    [
                    dbc.Col(html.Div(html.H5("XÂY DỰNG DANH MỤC SẢN PHẨM TIỀM NĂNG"))),
                    dbc.Col(html.Div(html.H5("IUH-DHKTPM16A-20072261-Trần Bảo Trúc"))),
                    ]
                ),
                className="row header pt-3 pb-3",
                
            ),
            html.Div(
                html.Div(
                    [
                    html.Div(html.Div([html.P("DOANH SỐ SALE",className="text-center"), html.Div([html.Div(html.H4(doanhSoSale,className="text-center"),className="col-6"), html.Div(html.H4("$",className="text-left"),className="col-6")],className="row")],className=" ",),className="view bg-white col-3",),
                    html.Div(html.Div([html.P("LỢI NHUẬN",className="text-center"), html.Div([html.Div(html.H4(loiNhuan,className="text-center"),className="col-6"), html.Div(html.H4("$",className="text-left"),className="col-6")],className="row")],className=" bg-white ",),className="view  col-3",),
                    html.Div(html.Div([html.P("TOP DOANH SỐ",className="text-center"), html.Div([html.Div(html.H4(topDoanhSo,className="text-center"),className="col-6"), html.Div(html.H4("$",className="text-left"),className="col-6")],className="row")],className="bg-white",),className="view col-3",),
                    html.Div(html.Div([html.P("TOP LỢI NHUẬN",className="text-center"), html.Div([html.Div(html.H4(topLoiNhuan,className="text-center"),className="col-6"), html.Div(html.H4("$",className="text-left"),className="col-6")],className="row")],className=" ",),className="view bg-white col-3",),
                    
                    ],
                    className="row p-2"
                ),
                
            ),
            dbc.Row(
                [
                dbc.Col(html.Div([
                    html.Div(
                        children=dcc.Graph(
                        id='doanhSoTheoNam-graph',
                        figure=figDoanhSo,
                        className="hist bg-white")
                    )
                    ]),
                    className="card col-md-6 col-sm-12",
                ),
                dbc.Col(html.Div([
                    html.Div(
                        children=dcc.Graph(
                        id='doanhSoTheoDoanhMuc-graph',
                        figure=figDoanhSoTheoDanhMucTheoNam,
                        className="hist bg-white"),)
                    ])
                    ,className="card col-md-6 col-sm-12",),
                ]
                ,className="row"),
            dbc.Row(
                [
                dbc.Col(html.Div([
                    html.Div(
                        children=dcc.Graph(
                        id='LoiNhuanTheoNam-graph',
                        figure=figLoiNhuanTheoNam,
                        className="hist bg-white"),),

                ])
                    ,className="card col-md-6 col-sm-12",
                ),
                dbc.Col(html.Div([
                    html.Div(
                        children=dcc.Graph(
                        id='LoiNhuanTheoDanhMucTheoNam-graph',
                        figure=figLoiNhuanTheoDanhMucTheoNam,
                        className="hist bg-white"),),
                    
                ])
                
                ,className="card col-md-6 col-sm-12",),
                ]
            ,className="row"),
        ])
     
    ],
    className="color row",
    ),
    className="container"
)
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
