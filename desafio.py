import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout='wide', page_title='Dashboard Global', page_icon='🌍')


def base_dados():
    dataset = pd.read_csv('Complex_Sales_Data.csv')
    dataset['Month'] = pd.to_datetime(
        dataset['Date'], format='%Y-%m-%d'
    ).dt.month
    dataset['Year'] = pd.to_datetime(
        dataset['Date'], format='%Y-%m-%d'
    ).dt.year
    dataset['Year'] = dataset['Year'].astype(int)
    return dataset

def filtros_dashbord(dados):
    regiao = st.sidebar.multiselect(
        'Filtro de Região',
        dados['Region'].unique(),
        default=dados['Region'].unique(),
    )

    produto = st.sidebar.multiselect(
        'Filtro de Produto',
        dados['Product'].unique(),
        default=dados['Product'].unique(),
    )

    ano = st.sidebar.multiselect(
        'Filtro de Ano',
        dados['Year'].unique(),
        default=dados['Year'].unique(),
    )
    return regiao, produto, ano

def base_localizacao(dados, filtro_regiao):
    faturamento = dados.groupby('Region')['Total Sales'].sum().reset_index()
    faturamento_produto = (
        dados.groupby(['Product', 'Region'])['Total Sales']
        .sum()
        .reset_index()
    )

    localizacao = []

    for r in filtro_regiao:
        vendas_total = faturamento.loc[
            faturamento['Region'] == r, 'Total Sales'
        ].sum()

        if r == 'North America':
            coordenadas = [37.0902, -95.7129]
        elif r == 'Europe':
            coordenadas = [49.5260, 14.2551]
        elif r == 'South America':
            coordenadas = [-8.7832, -55.4915]
        elif r == 'Asia':
            coordenadas = [34.0479, 80.6197]
        elif r == 'Africa':
            coordenadas = [5.7832, 24.5085]
        elif r == 'Oceania':
            coordenadas = [-25.2744, 133.7751]
        else:
            coordenadas = [0, 0]

        localizacao.append(
            {
                'regiao': r,
                'location': coordenadas,
                'vendas': vendas_total,
                'Desktop': faturamento_produto.loc[
                    (faturamento_produto['Region'] == r)
                    & (faturamento_produto['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                'Laptop': faturamento_produto.loc[
                    (faturamento_produto['Region'] == r)
                    & (faturamento_produto['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                'Smartphone': faturamento_produto.loc[
                    (faturamento_produto['Region'] == r)
                    & (faturamento_produto['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                'Smartwatch': faturamento_produto.loc[
                    (faturamento_produto['Region'] == r)
                    & (faturamento_produto['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                'Tablet': faturamento_produto.loc[
                    (faturamento_produto['Region'] == r)
                    & (faturamento_produto['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
            }
        )
    return localizacao

def mapa(localizacao):
    coordenadas_centro = [0, 0]

    mapa = folium.Map(
        location=coordenadas_centro,
        zoom_start=2,
        min_zoom=2,
        max_zoom=3,
        max_bounds=True,
        tiles='Cartodb Positron',
    )

    for loc in localizacao:
        popup_html = f"""
            <h1 style="margin:0;padding:0;"><b>{loc['regiao']}</b></h1>
            <h4 style="margin:0;padding:0;">Vendas Totais: <b>{loc['vendas']:.2f}</b></h4>
            <h5 style="margin:0;padding:0;"><b>Faturamento detalhado por produto</b></h5>
            <p style="margin:0;padding:0;">Desktop: <b>{loc['Desktop']:.2f}</b></p>
            <p style="margin:0;padding:0;">Laptop: <b>{loc['Laptop']:.2f}</b></p>
            <p style="margin:0;padding:0;">Smartphone: <b>{loc['Smartphone']:.2f}</b></p>
            <p style="margin:0;padding:0;">Smartwatch: <b>{loc['Smartwatch']:.2f}</b></p>
            <p style="margin:0;padding:0;">Tablet: <b>{loc['Tablet']:.2f}</b></p>
        """
        folium.Marker(
            location=loc['location'],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='darkblue', icon='info-sign'),
        ).add_to(mapa)

    mapa_html = 'mapa.html'
    mapa.save(mapa_html)
    return None

def main():
    st.title('Dashboard de Faturamento Global 🌍')
    st.sidebar.title('Filtros')

    # Base de dados
    dataset = base_dados()

    # Filtros
    regiao, produto, ano = filtros_dashbord(dataset)

    if regiao and produto and ano:
        filtros = dataset[
            dataset['Region'].isin(regiao)
            & dataset['Product'].isin(produto)
            & dataset['Year'].isin(ano)
        ]
    else:
        filtros = dataset

    # Base de dados para o folium
    localizacao = base_localizacao(filtros, regiao)

    # Criando mapa
    coordenadas_centro = [0, 0]

    mapa = folium.Map(
        location=coordenadas_centro,
        zoom_start=2,
        min_zoom=2,
        max_zoom=3,
        max_bounds=True,
        tiles='Cartodb Positron',
    )

    for loc in localizacao:
        popup_html = f"""
            <h1 style="margin:0;padding:0;"><b>{loc['regiao']}</b></h1>
            <h4 style="margin:0;padding:0;">Vendas Totais: <b>{loc['vendas']:.2f}</b></h4>
            <h5 style="margin:0;padding:0;"><b>Faturamento detalhado por produto</b></h5>
            <p style="margin:0;padding:0;">Desktop: <b>{loc['Desktop']:.2f}</b></p>
            <p style="margin:0;padding:0;">Laptop: <b>{loc['Laptop']:.2f}</b></p>
            <p style="margin:0;padding:0;">Smartphone: <b>{loc['Smartphone']:.2f}</b></p>
            <p style="margin:0;padding:0;">Smartwatch: <b>{loc['Smartwatch']:.2f}</b></p>
            <p style="margin:0;padding:0;">Tablet: <b>{loc['Tablet']:.2f}</b></p>
        """
        folium.Marker(
            location=loc['location'],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='darkblue', icon='info-sign'),
        ).add_to(mapa)

    mapa_html = 'mapa.html'
    mapa.save(mapa_html)

    st.components.v1.html(mapa._repr_html_(), height=400, width=900)

    # Outros gráficos
    c1, c2 = st.columns(2)

    barra = px.bar(filtros, x='Product', y='Total Sales', color='Product')
    barra.update_layout(
        showlegend=False,
        title='Faturamento por Produto',
        xaxis_title='Produtos',
        yaxis_title='Total de Vendas',
    )
    c1.plotly_chart(barra)

    dados = filtros.groupby('Month')['Total Sales'].sum().reset_index()
    meses = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Nov',
        'Dez',
    ]
    faturamento = dados['Total Sales']

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=meses,
            y=faturamento,
            mode='lines+markers',
            name='Faturamento',
            line=dict(color='#4b8aff'),
        )
    )
    fig.update_layout(
        title='Evolução do Faturamento Mensal',
        xaxis_title='Meses',
        yaxis_title='Faturamento',
        template='plotly',
    )
    c2.plotly_chart(fig)


if __name__ == '__main__':
    main()
