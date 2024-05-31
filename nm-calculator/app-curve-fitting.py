import tkinter as tk
from tkinter import messagebox
import numpy as np
import math

class NumericalMethodsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.resizable(0, 0)
        self.title('Calculadora de Metodos Numericos')
        self.create_main_menu()

    def create_main_menu(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(expand=True)

        options = [
            "Calcular polinomio interpolador por Newton",
            "Calcular polinomio interpolador por Newton-Gregory",
            "Ajustar os pontos tabelados em uma reta da forma y=a0+a1x",
            "Ajustar os pontos tabelados em um polinomio de grau desejado",
            "Ajustar os pontos tabelados em uma curva exponencial da forma y=ab^x"
        ]

        commands = [
            self.open_newton_window,
            self.open_newton_gregory_window,
            self.open_linear_fit_window,
            self.open_polynomial_fit_window,
            self.open_exponential_fit_window
        ]

        for option, command in zip(options, commands):
            button = tk.Button(self.menu_frame, text=option, command=command, font=('Calibri', 12), bg='LightBlue', fg='Red', width=60)
            button.pack(pady=10)

    def create_points_entries(self, window, num_points):
        frame = tk.Frame(window)
        frame.pack(fill='both', expand=True)

        if num_points >= 8:
            canvas = tk.Canvas(frame)
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            scrollable_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

            entries_frame = scrollable_frame
        else:
            entries_frame = frame

        entries = []
        for i in range(num_points):
            row_entries = []
            tk.Label(entries_frame, text=f"x{i+1}", font=('Calibri', 12)).grid(row=i, column=0, padx=5, pady=5)
            x_entry = tk.Entry(entries_frame, font=('Calibri', 12))
            x_entry.grid(row=i, column=1, padx=5, pady=5)
            tk.Label(entries_frame, text=f"y{i+1}", font=('Calibri', 12)).grid(row=i, column=2, padx=5, pady=5)
            y_entry = tk.Entry(entries_frame, font=('Calibri', 12))
            y_entry.grid(row=i, column=3, padx=5, pady=5)
            row_entries.append(x_entry)
            row_entries.append(y_entry)
            entries.append(row_entries)

        return entries

    def get_points(self, entries):
        points = []
        try:
            for entry_pair in entries:
                x = float(entry_pair[0].get())
                y = float(entry_pair[1].get())
                points.append((x, y))
            return points
        except ValueError:
            messagebox.showerror("Erro", "Input Invalido. Por favor, entre com numeros validos.")
            return None

    def calculate_r_squared(self, y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared

    def open_newton_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Polinomio Interpolador por Newton')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)
                tk.Label(window, text="Entre com o valor de x:", font=('Calibri', 12)).pack(padx=5, pady=5)
                x_entry = tk.Entry(window, font=('Calibri', 12))
                x_entry.pack(padx=5, pady=5)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)

                def calculate_newton():
                    try:
                        x = float(x_entry.get())
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        def divided_diff_table(points, n):
                            Y = np.zeros((n, n))
                            for i in range(n):
                                Y[i][0] = points[i][1]
                            for i in range(1, n):
                                for j in range(n - i):
                                    Y[j][i] = (Y[j + 1][i - 1] - Y[j][i - 1]) / (points[j + i][0] - points[j][0])
                            return Y

                        def newton_interpolation(Y, x, points, n):
                            result = Y[0][0]
                            product_term = 1.0
                            for i in range(1, n):
                                product_term *= (x - points[i - 1][0])
                                result += product_term * Y[0][i]
                            return result

                        Y = divided_diff_table(points, num_points)
                        result = newton_interpolation(Y, x, points, num_points)
                        result_label.config(text=f'f({x}) = {result:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(window, text="Calcular", command=calculate_newton, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Erro", "Numero invalido de pontos. Por favor entre com numero de 1 a 100.")

        num_points_label = tk.Label(window, text="Entre com o numero de pontos:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirmar", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

    def open_newton_gregory_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Polinomio Interpolador por Newton-Gregory')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)
                tk.Label(window, text="Entre com o valor de x :", font=('Calibri', 12)).pack(padx=5, pady=5)
                x_entry = tk.Entry(window, font=('Calibri', 12))
                x_entry.pack(padx=5, pady=5)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)

                def calculate_newton_gregory():
                    try:
                        x = float(x_entry.get())
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        def gregory_diff_table(points, n):
                            Y = np.zeros((n, n))
                            for i in range(n):
                                Y[i][0] = points[i][1]
                            for i in range(1, n):
                                for j in range(n - i):
                                    Y[j][i] = Y[j + 1][i - 1] - Y[j][i - 1]
                            return Y

                        def newton_gregory_interpolation(Y, x, points, n, h):
                            s = (x - points[0][0]) / h
                            result = Y[0][0]
                            product_term = 1.0
                            for i in range(1, n):
                                product_term *= (s - (i - 1))
                                result += (product_term * Y[0][i]) / math.factorial(i)
                            return result

                        h = round(points[1][0] - points[0][0], 5)
                        for i in range(1, num_points):
                            if round(points[i][0] - points[i - 1][0], 5) != h:
                                raise ValueError("Pontos não estão igualmente espaçados para a Interpolação de Newton-Gregory.")

                        Y = gregory_diff_table(points, num_points)
                        result = newton_gregory_interpolation(Y, x, points, num_points, h)
                        result_label.config(text=f'f({x}) = {result:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(window, text="Calcular", command=calculate_newton_gregory, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Erro", "Numero invalido de pontos. Por favor entre com numero de 1 a 100.")

        num_points_label = tk.Label(window, text="Entre com o número de pontos:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirmar", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

    def open_linear_fit_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Ajustar os pontos tabelados a uma reta da forma y=a0+a1x')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)
                r_squared_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                r_squared_label.pack(padx=5, pady=5)

                def calculate_linear_fit():
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])

                        A = np.vstack([x, np.ones(len(x))]).T
                        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

                        y_pred = m * x + c
                        r_squared = self.calculate_r_squared(y, y_pred)

                        result_label.config(text=f'y = {c:.4f} + {m:.4f}x')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(window, text="Calcular", command=calculate_linear_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Erro", "Numero invalido de pontos. Por favor entre com numero de 1 a 100.")

        num_points_label = tk.Label(window, text="Entre com o número de pontos:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirmar", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

    def open_polynomial_fit_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Ajustar os pontos tabelados a um polinomio de grau desejado')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                degree = int(degree_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                degree_label.pack_forget()
                degree_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)
                r_squared_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                r_squared_label.pack(padx=5, pady=5)

                def format_polynomial(coefficients):
                    terms = []
                    degree = len(coefficients) - 1
                    for i, coef in enumerate(coefficients):
                        coef = round(coef, 3)
                        if degree - i == 0:
                            terms.append(f'{coef}')
                        elif degree - i == 1:
                            terms.append(f'{coef}x')
                        else:
                            terms.append(f'{coef}x^{degree - i}')
                    return ' + '.join(terms)

                def calculate_polynomial_fit():
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])

                        coefficients = np.polyfit(x, y, degree)
                        polynomial = format_polynomial(coefficients)
                        y_pred = np.polyval(coefficients, x)
                        r_squared = self.calculate_r_squared(y, y_pred)

                        result_label.config(text=f'polinomio: {polynomial}')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(window, text="Calcular", command=calculate_polynomial_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Erro", "Input Invalido, por favor entre com numeros validos.")

        num_points_label = tk.Label(window, text="Entre com o número de pontos:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        degree_label = tk.Label(window, text="Entre com o grau desejado do polinômio:", font=('Calibri', 12))
        degree_label.pack(padx=5, pady=5)
        degree_entry = tk.Entry(window, font=('Calibri', 12))
        degree_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirmar", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

    def open_exponential_fit_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Ajustar os pontos tabelados a uma curva exponencial da forma y=ab^x')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)
                r_squared_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                r_squared_label.pack(padx=5, pady=5)

                def calculate_exponential_fit():
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])

                        log_y = np.log(y)
                        A = np.vstack([x, np.ones(len(x))]).T
                        m, c = np.linalg.lstsq(A, log_y, rcond=None)[0]
                        a = math.exp(c)
                        b = math.exp(m)

                        y_pred = a * np.power(b, x)
                        r_squared = self.calculate_r_squared(y, y_pred)

                        result_label.config(text=f'y = {a:.4f} * {b:.4f}^x')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(window, text="Calcular", command=calculate_exponential_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Erro", "Numero invalido de pontos. Por favor entre com número de 1 a 100.")

        num_points_label = tk.Label(window, text="Entre com o número de pontos:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirmar", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = NumericalMethodsCalculator()
    app.mainloop()
