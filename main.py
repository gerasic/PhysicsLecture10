import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Класс для точечного заряда
class Point:
    def __init__(self, charge, position):
        self.charge = charge
        self.position = np.array(position)
        
    def E(self, point):
        """ Напряженность поля для точечного заряда в точке point """
        r = np.array(point) - self.position
        r_magnitude = np.linalg.norm(r)
        r_hat = r / r_magnitude
        return self.charge * r_hat / r_magnitude**2  # Формула напряженности поля

# Класс для поля
class ElectricField:
    def __init__(self, charges):
        self.charges = charges
    
    def vector(self, point):
        """ Суммирует все векторы поля от всех зарядов в точке point """
        # Если нет зарядов, возвращаем нулевой вектор
        if not self.charges:
            return np.array([0.0, 0.0])
        return np.sum([charge.E(point) for charge in self.charges], axis=0)
    
    def magnitude(self, point):
        """ Длина вектора поля в точке point """
        return np.linalg.norm(self.vector(point))
    
    def angle(self, point):
        """ Угол вектора поля относительно оси X в точке point """
        vector = self.vector(point)
        # Если вектор пустой, возвращаем 0 (или можно добавить какое-то другое поведение)
        if np.all(vector == 0):
            return 0
        return np.arctan2(*(vector.T[::-1]))

# Список зарядов
charges = []

def add_charge():
    try:
        # Получаем значения с UI
        charge = float(entry_charge.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        
        # Создаем новый заряд
        new_charge = Point(charge, [x, y])
        charges.append(new_charge)
        
        # Обновляем поле
        update_field()
        status_label.config(text="Заряд добавлен!", foreground="green")
    except ValueError:
        status_label.config(text="Ошибка: Проверьте введённые данные", foreground="red")

def clear_charges():
    # Очищаем список зарядов
    charges.clear()
    update_field()
    status_label.config(text="Все заряды удалены.", foreground="blue")

def update_field():
    # Создаем поле для отображения
    field = ElectricField(charges)
    
    x, y = np.meshgrid(np.linspace(-10, 10, 40), np.linspace(-10, 10, 30))
    u, v = np.zeros_like(x), np.zeros_like(y)

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            point = [x[i, j], y[i, j]]
            mag = field.magnitude(point)
            
            # Если точка близка к одному из зарядов, игнорируем (E = 0)
            if any(np.linalg.norm(np.array(point) - charge.position) < 1 for charge in charges):
                u[i, j] = v[i, j] = None
            else:
                a = field.angle(point)
                u[i, j], v[i, j] = mag * np.cos(a), mag * np.sin(a)

    # Отображаем на графике
    ax.clear()
    ax.quiver(x, y, u, v, scale=50, color="blue")
    for charge in charges:
        ax.scatter(charge.position[0], charge.position[1], color='red' if charge.charge > 0 else 'green', s=100)

    ax.set_title("Электростатическое поле")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    canvas.draw()

# Создание окна
root = tk.Tk()
root.title("Моделирование электростатического поля")

# Обработчик для закрытия окна
def on_close():
    root.quit()

# Устанавливаем обработчик на закрытие окна
root.protocol("WM_DELETE_WINDOW", on_close)

# Фрейм для ввода параметров
frame_inputs = ttk.Frame(root)
frame_inputs.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

ttk.Label(frame_inputs, text="Заряд (Q):").grid(row=0, column=0, padx=5, pady=5)
entry_charge = ttk.Entry(frame_inputs)
entry_charge.grid(row=0, column=1, padx=5, pady=5)
entry_charge.insert(0, "1")

ttk.Label(frame_inputs, text="X заряда:").grid(row=1, column=0, padx=5, pady=5)
entry_x = ttk.Entry(frame_inputs)
entry_x.grid(row=1, column=1, padx=5, pady=5)
entry_x.insert(0, "0")

ttk.Label(frame_inputs, text="Y заряда:").grid(row=2, column=0, padx=5, pady=5)
entry_y = ttk.Entry(frame_inputs)
entry_y.grid(row=2, column=1, padx=5, pady=5)
entry_y.insert(0, "0")

add_button = ttk.Button(frame_inputs, text="Добавить заряд", command=add_charge)
add_button.grid(row=3, column=0, padx=5, pady=5)

clear_button = ttk.Button(frame_inputs, text="Очистить заряды", command=clear_charges)
clear_button.grid(row=3, column=1, padx=5, pady=5)

# Фрейм для графика
frame_plot = ttk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Статус бар
status_label = ttk.Label(root, text="Добавьте заряды и нажмите 'Добавить заряд'.", anchor="center")
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Запуск приложения
root.mainloop()
