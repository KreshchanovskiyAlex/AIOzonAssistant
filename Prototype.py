import streamlit as st
import pandas as pd
import requests
from prophet import Prophet
from prophet.plot import plot_plotly

# Настройки Ozon API (демо-режим)
DEMO_MODE = st.sidebar.checkbox("Демо-режим (без API)")
API_URL = "https://api.ozon.ru/v2"
API_KEY = "ваш_API_ключ" if not DEMO_MODE else "demo"
CLIENT_ID = "ваш_Client_ID" if not DEMO_MODE else "demo"
HEADERS = {"Client-Id": CLIENT_ID, "Api-Key": API_KEY}

def get_products():
    """Получение списка товаров"""
    if DEMO_MODE:
        # Демо-данные для товаров
        return [{"id": i, "name": f"Товар {i}", "price": 1000 + i * 100} for i in range(1, 6)]
    try:
        response = requests.get(f"{API_URL}/product/list", headers=HEADERS)
        return response.json().get("result", {}).get("items", [])
    except Exception as e:
        return {"error": str(e)}

def forecast_demand():
    """Прогнозирование спроса с использованием Prophet"""
    # Демо-данные: сезонность + тренд
    dates = pd.date_range(start="2024-01-01", periods=365)
    data = pd.DataFrame({
        "ds": dates,
        "y": [100 + (i % 30) * 5 + i * 0.2 for i in range(365)]
    })
    
    model = Prophet(seasonality_mode="multiplicative")
    model.fit(data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(30), model, forecast

# Интерфейс
st.title("🛍 AI-ассистент для Ozon")
st.markdown("""
**Основные функции:**
- Управление товарами
- Прогнозирование спроса (AI)
- Генерация описаний (в разработке)
""")

# Блок 1: Управление товарами
st.header("📦 Товары")
products = get_products()

if isinstance(products, dict) and "error" in products:
    st.error(products["error"])
else:
    for product in products:
        with st.expander(f"{product['name']} (ID: {product['id']})"):
            st.write(f"Цена: {product['price']} ₽")
            if st.button("Обновить цену", key=f"price_{product['id']}"):
                st.success("Цена обновлена!")

# Блок 2: Прогнозирование спроса (AI)
st.header("📈 Прогноз спроса")
if st.button("Сгенерировать прогноз"):
    forecast, model, full_forecast = forecast_demand()
    
    # График прогноза
    st.subheader("Прогноз спроса на 30 дней")
    fig = plot_plotly(model, full_forecast)
    st.plotly_chart(fig)

    # Рекомендации на основе прогноза
    last_date = forecast["ds"].max()
    predicted_demand = forecast[forecast["ds"] == last_date]["yhat"].values[0]

    st.subheader("Рекомендации AI:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Прогнозируемый спрос", f"{predicted_demand:.0f} ед.")
    with col2:
        st.write("""
        **Советы:**
        - Увеличьте запас на 15% в пиковые даты.
        - Запустите рекламную кампанию за 2 недели до всплеска спроса.
        """)
