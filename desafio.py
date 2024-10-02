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


def main():
    st.title('Dashboar de Faturamento Global 🌍')
    st.sidebar.title('Filtros')

    # Base de dados
    dataset = base_dados()

    # Filtros
    regiao = st.sidebar.multiselect(
        'Filtro de Região',
        dataset['Region'].unique(),
        default=dataset['Region'].unique(),
    )

    produto = st.sidebar.multiselect(
        'Filtro de Produto',
        dataset['Product'].unique(),
        default=dataset['Product'].unique(),
    )

    ano = st.sidebar.multiselect(
        'Filtro de Ano',
        dataset['Year'].unique(),
        default=dataset['Year'].unique(),
    )

    if regiao:
        filtros = dataset[
            dataset['Region'].isin(regiao)
            & dataset['Product'].isin(produto)
            & dataset['Year'].isin(ano)
        ]
    else:
        filtros = dataset

    # Base de dados para o folium
    df = (
        dataset[['Region', 'Quantity Sold']]
        .groupby('Region')
        .sum()
        .reset_index()
    )
    df_p = (
        dataset.groupby(['Product', 'Region'])['Total Sales']
        .sum()
        .reset_index()
    )

    localizacao = localizacao = [
        {
            'regiao': df.iloc[3, 0],
            'location': [37.0902, -95.7129],
            'vendas': df.iloc[3, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'North America')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'North America')
                    & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'North America')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'North America')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'North America')
                    & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
        {
            'regiao': df.iloc[5, 0],
            'location': [-8.7832, -55.4915],
            'vendas': df.iloc[5, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'South America')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'South America')
                    & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'South America')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'South America')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'South America')
                    & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
        {
            'regiao': df.iloc[2, 0],
            'location': [49.5260, 14.2551],
            'vendas': df.iloc[2, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'Europe')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'Europe')
                    & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'Europe')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'Europe')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'Europe')
                    & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
        {
            'regiao': df.iloc[1, 0],
            'location': [34.0479, 80.6197],
            'vendas': df.iloc[1, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'Asia')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'Asia') & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'Asia')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'Asia')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'Asia') & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
        {
            'regiao': df.iloc[0, 0],
            'location': [5.7832, 24.5085],
            'vendas': df.iloc[0, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'Africa')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'Africa')
                    & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'Africa')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'Africa')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'Africa')
                    & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
        {
            'regiao': df.iloc[4, 0],
            'location': [-25.2744, 133.7751],
            'vendas': df.iloc[4, 1],
            'Desktop': round(
                df_p.loc[
                    (df_p['Region'] == 'Oceania')
                    & (df_p['Product'] == 'Desktop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Laptop': round(
                df_p.loc[
                    (df_p['Region'] == 'Oceania')
                    & (df_p['Product'] == 'Laptop'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartphone': round(
                df_p.loc[
                    (df_p['Region'] == 'Oceania')
                    & (df_p['Product'] == 'Smartphone'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Smartwatch': round(
                df_p.loc[
                    (df_p['Region'] == 'Oceania')
                    & (df_p['Product'] == 'Smartwatch'),
                    'Total Sales',
                ].sum(),
                2,
            ),
            'Tablet': round(
                df_p.loc[
                    (df_p['Region'] == 'Oceania')
                    & (df_p['Product'] == 'Tablet'),
                    'Total Sales',
                ].sum(),
                2,
            ),
        },
    ]

    coordenadas_centro = [0, 0]

    mapa = folium.Map(
        location=coordenadas_centro,
        zoom_start=2,
        min_zoom=2,
        max_zoom=2,
        max_bounds=True,
        tiles='Cartodb Positron',
    )

    for loc in localizacao:
        popup_html = f"""
            <h4 style="margin:0;padding:0;">{loc['regiao']}</h4>
            <p style="margin:0;padding:0;">Total de Produtos Vendidos: {loc['vendas']}</p>
            <p style="margin:0;padding:0;">Faturamento Desktop: {loc['Desktop']}</p>
            <p style="margin:0;padding:0;">Faturamento Laptop: {loc['Laptop']}</p>
            <p style="margin:0;padding:0;">Faturamento Smartphone: {loc['Smartphone']}</p>
            <p style="margin:0;padding:0;">Faturamento Smartwatch: {loc['Smartwatch']}</p>
            <p style="margin:0;padding:0;">Faturamento Tablet: {loc['Tablet']}</p>
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
