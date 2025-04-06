import requests
import streamlit as st

# Настройки Ozon API (замените на свои)
API_URL = "https://api.ozon.ru/v2"
API_KEY = "ваш_API_ключ"
CLIENT_ID = "ваш_Client_ID"
HEADERS = {"Client-Id": CLIENT_ID, "Api-Key": API_KEY}

def get_products():
    """Получение списка товаров"""
    try:
        response = requests.get(f"{API_URL}/product/list", headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()["result"]["items"]
    except Exception as e:
        return {"error": str(e)}

def update_price(product_id: str, new_price: float):
    """Обновление цены товара"""
    try:
        payload = {"product_id": product_id, "price": str(new_price)}
        response = requests.post(f"{API_URL}/product/update", json=payload, headers=HEADERS)
        response.raise_for_status()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

# Интерфейс Streamlit
st.set_page_config(page_title="Ozon Seller Assistant", layout="wide")

# Сайдбар с настройками
with st.sidebar:
    st.header("Настройки API")
    api_key = st.text_input("API Key", value=API_KEY)
    client_id = st.text_input("Client ID", value=CLIENT_ID)

# Основной интерфейс
st.title("🎯 AI-помощник для продавцов Ozon")
st.markdown("""
### Основные функции:
- Просмотр списка товаров
- Обновление цен в реальном времени
- Анализ конкурентов (в разработке)
- Генерация описаний (в разработке)
""")

# Раздел управления товарами
st.header("📦 Управление товарами")
if st.button("Обновить список товаров"):
    with st.spinner("Получаем данные..."):
        products = get_products()
        
    if "error" in products:
        st.error(f"Ошибка: {products['error']}")
    else:
        st.success(f"Найдено товаров: {len(products)}")
        for product in products[:15]:
            with st.expander(f"{product['name']} (ID: {product['id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Текущая цена:** {product['price']} ₽")
                with col2:
                    with st.form(key=f"form_{product['id']}"):
                        new_price = st.number_input(
                            "Новая цена", 
                            value=float(product['price']),
                            key=f"price_{product['id']}"
                        )
                        if st.form_submit_button("Обновить"):
                            result = update_price(product['id'], new_price)
                            if "success" in result:
                                st.success("Цена обновлена!")
                            else:
                                st.error(f"Ошибка: {result['error']}")
