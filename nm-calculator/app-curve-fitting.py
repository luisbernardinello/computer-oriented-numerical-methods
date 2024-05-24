import tkinter as tk
from tkinter import messagebox
import numpy as np
import math

class NumericalMethodsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.resizable(0, 0)
        self.title('Numerical Methods Calculator')
        self.create_main_menu()

    def create_main_menu(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(expand=True)

        options = [
            "Calcular polinomio interpolado por Newton",
            "Calcular polinomio interpolado por Newton-Gregory",
            "Ajustar os pontos tabelados a uma reta da forma y=a0+a1x",
            "Ajustar os pontos tabelados a um polinomio de grau desejado",
            "Ajustar os pontos tabelados a uma curva exponencial da forma y=ab^x"
        ]

        commands = [
            self.open_newton_window,
            self.open_newton_gregory_window,
            self.open_linear_fit_window,
            self.open_polynomial_fit_window,
            self.open_exponential_fit_window
        ]

        for option, command in zip(options, commands):
            button = tk.Button(self.menu_frame, text=option, command=command, font=('Calibri', 12), bg='LightBlue', fg='Red', width=50)
            button.pack(pady=10)

    def create_points_entries(self, window, num_points):
        entries_frame = tk.Frame(window)
        entries_frame.pack()

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
            messagebox.showerror("Error", "Invalid input in points. Please enter valid numbers.")
            return None

    def open_newton_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Polinomio Interpolado por Newton')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)
                tk.Label(window, text="Enter x value:", font=('Calibri', 12)).pack(padx=5, pady=5)
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
                            y = np.zeros((n, n))
                            for i in range(n):
                                y[i][0] = points[i][1]
                            for i in range(1, n):
                                for j in range(n - i):
                                    y[j][i] = (y[j + 1][i - 1] - y[j][i - 1]) / (points[j + i][0] - points[j][0])
                            return y

                        def newton_interpolation(y, x, points, n):
                            result = y[0][0]
                            for i in range(1, n):
                                term = y[0][i]
                                for j in range(i):
                                    term *= (x - points[j][0])
                                result += term
                            return result

                        y = divided_diff_table(points, num_points)
                        result = newton_interpolation(y, x, points, num_points)
                        result_label.config(text=f'P({x}) = {result:.4f}')

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(window, text="Calculate", command=calculate_newton, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Error", "Invalid number of points. Please enter a number between 1 and 100.")

        num_points_label = tk.Label(window, text="Enter number of points:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirm", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

    def open_newton_gregory_window(self):
        window = tk.Toplevel(self)
        window.geometry('600x400')
        window.title('Polinomio Interpolado por Newton-Gregory')

        def show_points_entries():
            try:
                num_points = int(num_points_entry.get())
                if num_points < 1 or num_points > 100:
                    raise ValueError()
                num_points_label.pack_forget()
                num_points_entry.pack_forget()
                confirm_button.pack_forget()

                points_entries = self.create_points_entries(window, num_points)
                tk.Label(window, text="Enter x value:", font=('Calibri', 12)).pack(padx=5, pady=5)
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
                            y = np.zeros((n, n))
                            for i in range(n):
                                y[i][0] = points[i][1]
                            for i in range(1, n):
                                for j in range(n - i):
                                    y[j][i] = y[j + 1][i - 1] - y[j][i - 1]
                            return y

                        def newton_gregory_interpolation(y, x, points, n, h):
                            s = (x - points[0][0]) / h
                            result = y[0][0]
                            for i in range(1, n):
                                term = y[0][i]
                                for j in range(i):
                                    term *= (s - j)
                                term /= math.factorial(i)
                                result += term
                            return result

                        h = points[1][0] - points[0][0]
                        for i in range(1, num_points):
                            if points[i][0] - points[i - 1][0] != h:
                                raise ValueError("Points are not equally spaced for Newton-Gregory interpolation.")

                        y = gregory_diff_table(points, num_points)
                        result = newton_gregory_interpolation(y, x, points, num_points, h)
                        result_label.config(text=f'P({x}) = {result:.4f}')

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(window, text="Calculate", command=calculate_newton_gregory, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Error", "Invalid number of points. Please enter a number between 1 and 100.")

        num_points_label = tk.Label(window, text="Enter number of points:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirm", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
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

                def calculate_linear_fit():
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])

                        A = np.vstack([x, np.ones(len(x))]).T
                        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

                        result_label.config(text=f'y = {c:.4f} + {m:.4f}x')

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(window, text="Calculate", command=calculate_linear_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Error", "Invalid number of points. Please enter a number between 1 and 100.")

        num_points_label = tk.Label(window, text="Enter number of points:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirm", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
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

                def calculate_polynomial_fit():
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])

                        coefficients = np.polyfit(x, y, degree)
                        polynomial = np.poly1d(coefficients)

                        result_label.config(text=f'Polynomial: {polynomial}')

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(window, text="Calculate", command=calculate_polynomial_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

        num_points_label = tk.Label(window, text="Enter number of points:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        degree_label = tk.Label(window, text="Enter degree of polynomial:", font=('Calibri', 12))
        degree_label.pack(padx=5, pady=5)
        degree_entry = tk.Entry(window, font=('Calibri', 12))
        degree_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirm", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
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

                        result_label.config(text=f'y = {a:.4f} * {b:.4f}^x')

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(window, text="Calculate", command=calculate_exponential_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(padx=5, pady=5)

            except ValueError:
                messagebox.showerror("Error", "Invalid number of points. Please enter a number between 1 and 100.")

        num_points_label = tk.Label(window, text="Enter number of points:", font=('Calibri', 12))
        num_points_label.pack(padx=5, pady=5)
        num_points_entry = tk.Entry(window, font=('Calibri', 12))
        num_points_entry.pack(padx=5, pady=5)
        confirm_button = tk.Button(window, text="Confirm", command=show_points_entries, font=('Calibri', 12), bg='LightBlue', fg='Red')
        confirm_button.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = NumericalMethodsCalculator()
    app.mainloop()
