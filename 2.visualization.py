import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных из Excel
df = pd.read_excel("data/weather_forecast.xlsx")

# Очистка данных
df["Макс. температура"] = df["Макс. температура"].astype(str).str.replace("°C", "").str.replace("−", "-").str.replace(",", ".").astype(float)
df["Мин. температура"] = df["Мин. температура"].astype(str).str.replace("°C", "").str.replace("−", "-").str.replace(",", ".").astype(float)
df["Порывы ветра, м/c"] = df["Порывы ветра, м/c"].astype(str).str.replace(" м/с", "").str.replace("−", "-").str.replace(",", ".").astype(float)
df["Осадки"] = df["Осадки"].astype(str).str.replace(" мм", "").str.replace("−", "-").str.replace(",", ".").astype(float)

# Создание фигуры с тремя графиками
plt.figure(figsize=(12, 14))

# Тепловая карта для температуры
plt.subplot(3, 1, 1)  # 3 строки, 1 столбец, первый график
heatmap_data = df.pivot_table(index="Дата", values=["Макс. температура", "Мин. температура"])
heatmap = sns.heatmap(
    heatmap_data.T,  # Транспонируем данные для удобства
    cmap="coolwarm",  # Градиент от синего к красному
    annot=True,       # Показывать значения в ячейках
    fmt=".1f",        # Формат чисел (одна десятичная точка)
    linewidths=0.5,   # Ширина линий между ячейками
    vmin=-30,         # Минимальное значение для градиента
    vmax=30,          # Максимальное значение для градиента
    cbar=False        # Отключаем стандартную цветовую шкалу
)
plt.title("Тепловая карта температуры", fontsize=16)
plt.xlabel("Дата", fontsize=12)
plt.ylabel("Температура", fontsize=12)
plt.xticks(rotation=45)  # Поворот подписей дат для удобства

# Добавление горизонтальной цветовой шкалы
cbar_ax = plt.gcf().add_axes([0.25, 0.45, 0.5, 0.02])  # Положение и размеры шкалы
plt.colorbar(heatmap.get_children()[0], cax=cbar_ax, orientation="horizontal")
cbar_ax.set_xlabel("Температура (°C)", fontsize=12)  # Подпись шкалы

# График порывов ветра
plt.subplot(3, 1, 2)  # 3 строки, 1 столбец, второй график
plt.plot(df["Дата"], df["Порывы ветра, м/c"], label="Порывы ветра", marker="o", color="green")
plt.title("Порывы ветра", fontsize=16)
plt.xlabel("Дата", fontsize=12)
plt.ylabel("Порывы ветра, м/c", fontsize=12)
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1)  # Легенда снизу
plt.grid()

# График осадков
plt.subplot(3, 1, 3)  # 3 строки, 1 столбец, третий график
plt.plot(df["Дата"], df["Осадки"], label="Осадки", marker="o", color="blue")
plt.title("Осадки", fontsize=16)
plt.xlabel("Дата", fontsize=12)
plt.ylabel("Осадки, мм", fontsize=12)
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1)  # Легенда снизу
plt.grid()

# Сохранение графиков
plt.tight_layout()
plt.savefig("data/weather_visualization.png", bbox_inches="tight")  # Сохраняем с учетом легенды
plt.show()