import tkinter as tk
from tkinter import messagebox
import numpy as np
import math

class NumericalMethodsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x600')
        self.resizable(0, 0)
        self.title('Calculadora de Metodos Numericos')
        self.create_main_menu()

    def create_main_menu(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(expand=True, padx=20, pady=20)

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
        frame.pack(fill='both', expand=True, padx=10, pady=10)

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

    def validate_x_entry(self, x_entry):
        if not x_entry.get():
            messagebox.showwarning("Aviso", "Por favor, entre com o valor de x.")
            return False
        return True

    def open_newton_window(self):
        window = tk.Toplevel(self)
        window.geometry('470x600')
        window.resizable(False, False)
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
                input_frame = tk.Frame(window)
                input_frame.pack(padx=10, pady=10)

                tk.Label(input_frame, text="Entre com o valor de x:", font=('Calibri', 12)).pack(side='left', padx=5, pady=5)
                x_entry = tk.Entry(input_frame, font=('Calibri', 12))
                x_entry.pack(side='left', padx=5, pady=5)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)

                def calculate_newton():
                    if not self.validate_x_entry(x_entry):
                        return
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

                tk.Button(input_frame, text="Calcular", command=calculate_newton, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(side='left', padx=5, pady=5)

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
        window.geometry('470x600')
        window.resizable(False, False)
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
                input_frame = tk.Frame(window)
                input_frame.pack(padx=10, pady=10)

                tk.Label(input_frame, text="Entre com o valor de x:", font=('Calibri', 12)).pack(side='left', padx=5, pady=5)
                x_entry = tk.Entry(input_frame, font=('Calibri', 12))
                x_entry.pack(side='left', padx=5, pady=5)

                result_label = tk.Label(window, font=('Calibri', 12), bg='LightBlue', fg='Red')
                result_label.pack(padx=5, pady=5)

                def calculate_newton_gregory():
                    if not self.validate_x_entry(x_entry):
                        return
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

                tk.Button(input_frame, text="Calcular", command=calculate_newton_gregory, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(side='left', padx=5, pady=5)

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
        window.geometry('470x600')
        window.resizable(False, False)
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
                input_frame = tk.Frame(window)
                input_frame.pack(padx=10, pady=10)

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

                        n = len(x)
                        sum_x = np.sum(x)
                        sum_y = np.sum(y)
                        sum_x_squared = np.sum(x**2)
                        sum_xy = np.sum(x * y)

                        # minimos quadrados
                        a1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
                        a0 = (sum_y - a1 * sum_x) / n

                        
                        y_pred = a0 + a1 * x

       
                        mean_y = np.mean(y)
                        ss_total = np.sum((y - mean_y)**2)
                        ss_residual = np.sum((y - y_pred)**2)
                        r_squared = 1 - (ss_residual / ss_total)

                        result_label.config(text=f'y = {a0:.4f} + {a1:.4f}x')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))


                tk.Button(input_frame, text="Calcular", command=calculate_linear_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(side='left', padx=5, pady=5)

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
        window.geometry('470x600')
        window.resizable(False, False)
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
                input_frame = tk.Frame(window)
                input_frame.pack(padx=10, pady=10)

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

                def cholesky_decomposition(A):
                    n = len(A)
                    L = np.zeros((n, n))
                    for i in range(n):
                        for j in range(i + 1):
                            sum = 0
                            if j == i:
                                for k in range(j):
                                    sum += L[j, k] ** 2
                                L[j, j] = np.sqrt(A[j, j] - sum)
                            else:
                                for k in range(j):
                                    sum += L[i, k] * L[j, k]
                                L[i, j] = (A[i, j] - sum) / L[j, j]
                    return L

                
                def lu_decomposition(A):
                    n = len(A)
                    L = np.zeros((n, n))
                    U = np.zeros((n, n))
                    
                    for i in range(n):
                        for j in range(i, n):
                            sum_u = sum(L[i][k] * U[k][j] for k in range(i))
                            U[i][j] = A[i][j] - sum_u

                        for j in range(i, n):
                            if i == j:
                                L[i][i] = 1
                            else:
                                sum_l = sum(L[j][k] * U[k][i] for k in range(i))
                                L[j][i] = (A[j][i] - sum_l) / U[i][i]

                    return L, U
                
                def calculate_polynomial_fit(method):
                    try:
                        points = self.get_points(points_entries)
                        if points is None:
                            return

                        x = np.array([p[0] for p in points])
                        y = np.array([p[1] for p in points])
                        n = degree + 1

                        # matriz de Vandermonde
                        A = np.zeros((len(x), n))
                        for i in range(len(x)):
                            for j in range(n):
                                A[i, j] = x[i] ** (n - j - 1)
                        B = y

                        if method == "LU":
                            A_T_A = np.dot(A.T, A)
                            A_T_B = np.dot(A.T, B)
                            L, U = lu_decomposition(A_T_A)
                            y_lu = np.linalg.solve(L, A_T_B)
                            coefficients = np.linalg.solve(U, y_lu)
                        elif method == "Cholesky":
                            A_T_A = np.dot(A.T, A)
                            A_T_B = np.dot(A.T, B)
                            L = cholesky_decomposition(A_T_A)
                            y_cholesky = np.linalg.solve(L, A_T_B)
                            coefficients = np.linalg.solve(L.T, y_cholesky)
                        else:
                            raise ValueError("Método de decomposição não selecionado.")

                        polynomial = format_polynomial(coefficients)
                        y_pred = np.polyval(coefficients, x)
                        r_squared = self.calculate_r_squared(y, y_pred)

                        result_label.config(text=f'polinomio: {polynomial}')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')
                        
                        

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                
                lu_button = tk.Button(window, text="LU", command=lambda: calculate_polynomial_fit("LU"), font=('Calibri', 12), bg='LightBlue', fg='Red')
                lu_button.pack(padx=5, pady=5)
                cholesky_button = tk.Button(window, text="Cholesky", command=lambda: calculate_polynomial_fit("Cholesky"), font=('Calibri', 12), bg='LightBlue', fg='Red')
                cholesky_button.pack(padx=5, pady=5)

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
        window.geometry('470x600')
        window.resizable(False, False)
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
                input_frame = tk.Frame(window)
                input_frame.pack(padx=10, pady=10)

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

                        # coeficientes m e c
                        ATA_inv = np.linalg.inv(A.T @ A)
                        ATA_inv_AT = ATA_inv @ A.T
                        mc = ATA_inv_AT @ log_y


                        m, c = mc[0], mc[1]

                        a = np.exp(c)
                        b = np.exp(m)

                        y_pred = a * np.power(b, x)

                        mean_y = np.mean(y)
                        ss_total = np.sum((y - mean_y)**2)
                        ss_residual = np.sum((y - y_pred)**2)
                        r_squared = 1 - (ss_residual / ss_total)

                        result_label.config(text=f'y = {a:.4f} * {b:.4f}^x')
                        r_squared_label.config(text=f'R² = {r_squared:.4f}')

                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                tk.Button(input_frame, text="Calcular", command=calculate_exponential_fit, font=('Calibri', 12), bg='LightBlue', fg='Red').pack(side='left', padx=5, pady=5)

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
