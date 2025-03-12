import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod

# ---------------------- Strategy Pattern ----------------------
class LinearSystemMethod(ABC):
    @abstractmethod
    def calculate(self, matrix, vector, **kwargs):
        pass

    @abstractmethod
    def get_result_text(self):
        pass

class DeterminantMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        determinant = self.calc_determinant(matrix)
        self.result = determinant
        return determinant

    def calc_determinant(self, matrix):
        order = len(matrix)
        if order == 1:
            return matrix[0][0]
        else:
            resp = 0
            for i in range(order):
                if matrix[0][i] != 0:
                    matrix_aux = np.delete(matrix, 0, axis=0)
                    matrix_aux = np.delete(matrix_aux, i, axis=1)
                    pivo = matrix[0][i] if i % 2 == 0 else -matrix[0][i]
                    resp += pivo * self.calc_determinant(matrix_aux)
            return resp

    def get_result_text(self):
        return f"Determinante: {self.result:.4f}"

class LowerTriangularMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        X = self.calc_lower_triangular(len(matrix), matrix, vector)
        self.result = X
        return X

    def calc_lower_triangular(self, order, matrix, vector):
        X = np.zeros(order)
        for i in range(order):
            if i == 0:
                X[0] = vector[0] / matrix[0][0]
            else:
                soma = 0
                for j in range(i):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X

    def get_result_text(self):
        return f"Solução (Triangular Inferior): {', '.join(f'{x:.4f}' for x in self.result)}"

class UpperTriangularMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        X = self.calc_upper_triangular(len(matrix), matrix, vector)
        self.result = X
        return X

    def calc_upper_triangular(self, order, matrix, vector):
        X = np.zeros(order)
        for i in range(order - 1, -1, -1):
            if i == order - 1:
                X[i] = vector[i] / matrix[i][i]
            else:
                soma = 0
                for j in range(i + 1, order):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X

    def get_result_text(self):
        return f"Solução (Triangular Superior): {', '.join(f'{x:.4f}' for x in self.result)}"

class LUDecompositionMethod(LinearSystemMethod):
    def __init__(self):
        self.determinant_method = DeterminantMethod()

    def calculate(self, matrix, vector, **kwargs):
        determinant = self.determinant_method.calculate(matrix, vector)
        if determinant == 0:
            raise ValueError("A matriz inserida não converge. O determinante é igual a zero.")
        triangular_matrix_L, triangular_matrix_U, vector = self.calc_LU_decomposition(len(matrix), matrix, vector)
        X = self.aux_LU(len(matrix), triangular_matrix_L, triangular_matrix_U, vector)
        X = [0 if abs(x) < 1e-10 else x for x in X]
        self.result = X
        return X

    def calc_LU_decomposition(self, ordem, matrix, vector):
        triangular_matrix_U = np.zeros((ordem, ordem))
        triangular_matrix_L = np.zeros((ordem, ordem))

        for i in range(ordem):
            self.calc_triangular_matrix_U(i, ordem, matrix, triangular_matrix_L, triangular_matrix_U)
            self.calc_triangular_matrix_L(i, ordem, matrix, triangular_matrix_L, triangular_matrix_U)

        return triangular_matrix_L, triangular_matrix_U, vector

    def calc_triangular_matrix_U(self, i, order, matrix, triangular_matrix_L, triangular_matrix_U):
        for j in range(order):
            if i == 0:
                triangular_matrix_U[i][j] = matrix[i][j]
            else:
                soma = 0
                for k in range(i):
                    soma += triangular_matrix_L[i][k] * triangular_matrix_U[k][j]
                triangular_matrix_U[i][j] = matrix[i][j] - soma

    def calc_triangular_matrix_L(self, j, order, matrix, triangular_matrix_L, triangular_matrix_U):
        for i in range(order):
            if j == 0:
                triangular_matrix_L[i][j] = matrix[i][j] / triangular_matrix_U[j][j]
            else:
                soma = 0
                for k in range(j):
                    soma += triangular_matrix_L[i][k] * triangular_matrix_U[k][j]
                triangular_matrix_L[i][j] = (matrix[i][j] - soma) / triangular_matrix_U[j][j]

    def aux_LU(self, order, triangular_matrix_L, triangular_matrix_U, vector):
        Y = np.zeros(order)

        # Ly = b
        Y[0] = vector[0] / triangular_matrix_L[0][0]
        for i in range(1, order):
            soma = 0
            for j in range(i):
                soma += triangular_matrix_L[i][j] * Y[j]
            Y[i] = (vector[i] - soma) / triangular_matrix_L[i][i]

        # Ux = y
        X = np.zeros(order)
        X[order - 1] = Y[order - 1] / triangular_matrix_U[order - 1][order - 1]
        for i in range(order - 2, -1, -1):
            soma = 0
            for j in range(i + 1, order):
                soma += triangular_matrix_U[i][j] * X[j]
            X[i] = (Y[i] - soma) / triangular_matrix_U[i][i]

        return X

    def get_result_text(self):
        return f"Solução (Decomposição LU): {', '.join(f'{x:.4f}' for x in self.result)}"

class CholeskyMethod(LinearSystemMethod):
    def __init__(self):
        self.determinant_method = DeterminantMethod()

    def calculate(self, matrix, vector, **kwargs):
        determinant = self.determinant_method.calculate(matrix, vector)
        calc_simetric = self.calc_simetric(matrix)
        if determinant < 0:
            raise ValueError("A matriz inserida não é definida positiva.")
        elif not calc_simetric:
            raise ValueError("A matriz inserida não é simétrica.")
        X = self.calc_cholesky(len(matrix), matrix, vector)
        X = [0 if abs(x) < 1e-10 else x for x in X]
        self.result = X
        return X

    def calc_simetric(self, matrix):
        order = len(matrix)
        for i in range(order):
            for j in range(order):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True

    def calc_cholesky(self, order, matrix, vector):
        triangular_matrix_L = np.zeros((order, order))
        self.aux_cholesky(order, matrix, triangular_matrix_L)
        
        # Ly = b utilizando a função de matriz triangular inferior
        vector_y = np.zeros(order)
        vector_y = self.calc_lower_triangular(order, triangular_matrix_L, vector)  
        
        # matriz transposta de L pelo .T do numpy
        transposed_triangular_matrix_L = triangular_matrix_L.T
        
        # L^t x = y utilizando a função de matriz triangular superior
        solution_vector = np.zeros(order)
        solution_vector = self.calc_upper_triangular(order, transposed_triangular_matrix_L, vector_y)  
        
        return solution_vector

    def aux_cholesky(self, order, matrix, cholesky_matrix):
        for i in range(order):
            for j in range(order):
                if i == j:
                    if i == 0:
                        cholesky_matrix[i][j] = np.sqrt(matrix[i][j])
                    else:
                        soma = 0
                        for k in range(i):
                            soma += cholesky_matrix[i][k] ** 2
                        cholesky_matrix[i][j] = np.sqrt(matrix[i][j] - soma)
                else:
                    if j < i:
                        soma = 0
                        for k in range(j):
                            soma += cholesky_matrix[i][k] * cholesky_matrix[j][k]
                        cholesky_matrix[i][j] = (matrix[i][j] - soma) / cholesky_matrix[j][j]
                    else:
                        cholesky_matrix[i][j] = 0

    def calc_lower_triangular(self, order, matrix, vector):
        X = np.zeros(order)
        for i in range(order):
            if i == 0:
                X[0] = vector[0] / matrix[0][0]
            else:
                soma = 0
                for j in range(i):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X

    def calc_upper_triangular(self, order, matrix, vector):
        X = np.zeros(order)
        for i in range(order - 1, -1, -1):
            if i == order - 1:
                X[i] = vector[i] / matrix[i][i]
            else:
                soma = 0
                for j in range(i + 1, order):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X

    def get_result_text(self):
        return f"Solução (Cholesky): {', '.join(f'{x:.4f}' for x in self.result)}"

class GaussCompactMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        X = self.calc_compact_gauss(len(matrix), matrix, vector)
        X = [0 if abs(x) < 1e-10 else x for x in X]
        self.result = X
        return X

    def calc_compact_gauss(self, order, matrix, vector):
        X = np.zeros(order)

        for k in range(order - 1):
            for i in range(k + 1, order):
                temp = matrix[i][k] / matrix[k][k]
                vector[i] -= temp * vector[k]
                for j in range(k, order):
                    matrix[i][j] -= temp * matrix[k][j]

        X[order - 1] = vector[order - 1] / matrix[order - 1][order - 1]

        for i in range(order - 2, -1, -1):
            temp = vector[i]
            for j in range(i + 1, order):
                temp -= matrix[i][j] * X[j]
            X[i] = temp / matrix[i][i]

        return X

    def get_result_text(self):
        return f"Solução (Gauss Compacto): {', '.join(f'{x:.4f}' for x in self.result)}"

class GaussJordanMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        X = self.calc_gauss_jordan(len(matrix), matrix, vector)
        if X is None:
            raise ValueError("O sistema gerado é indeterminado.")
        X = [0 if abs(x) < 1e-10 else x for x in X]
        self.result = X
        return X

    def calc_gauss_jordan(self, order, matrix, vector):
        augmented_matrix = np.zeros((order, order + 1))

        for i in range(order):
            for j in range(order + 1):
                if j == order:
                    augmented_matrix[i][j] = vector[i]
                else:
                    augmented_matrix[i][j] = matrix[i][j]

        for i in range(order):
            pivo = augmented_matrix[i][i]
            if pivo == 0:
                return None  # Sistema indeterminado
            else:
                for j in range(i, order + 1):
                    augmented_matrix[i][j] /= pivo

                for k in range(order):
                    if k != i:
                        factor = augmented_matrix[k][i]
                        for j in range(i, order + 1):
                            augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

        X = np.zeros(order)
        for i in range(order):
            X[i] = augmented_matrix[i][order]

        return X

    def get_result_text(self):
        return f"Solução (Gauss-Jordan): {', '.join(f'{x:.4f}' for x in self.result)}"

class JacobiMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        if not self.column_convergence(matrix) or not self.line_convergence(matrix):
            raise ValueError("Matriz não converge. Critério de Linhas ou Colunas não satisfeito.")
        
        vector = vector.tolist()
        aprox = [0] * len(matrix)
        X = [0] * len(matrix)
        max_iter = 1000  
        e = 0.0001  # precisao
        iterations = [0]
        
        self.calc_jacobi(len(matrix), matrix.tolist(), vector, aprox, e, max_iter, X, iterations)
        X = [round(x, 4) for x in X]
        self.result = X
        self.iterations = iterations[0]
        return X

    def calc_jacobi(self, order, matrix, vector, aprox, e, max_iterations, solution, iterations):
        temp = [0] * order

        for iteration in range(1, max_iterations + 1):
            erro = 0.0

            for i in range(order):
                temp[i] = vector[i]
                for j in range(order):
                    if i != j:
                        temp[i] -= matrix[i][j] * aprox[j]
                temp[i] /= matrix[i][i]

            for i in range(order):
                erro += (temp[i] - aprox[i]) * (temp[i] - aprox[i])

            for i in range(order):
                aprox[i] = temp[i]

            if erro < e:
                break

        for i in range(order):
            solution[i] = aprox[i]

        iterations[0] = iteration
        return solution

    def column_convergence(self, matrix):
        n = len(matrix)
        for j in range(n):
            diagonal_sum = 0
            for i in range(n):
                if i != j:
                    diagonal_sum += abs(matrix[i][j])
            if abs(matrix[j][j]) <= diagonal_sum:
                return False
        return True

    def line_convergence(self, matrix):
        n = len(matrix)
        for i in range(n):
            diagonal_sum = 0
            for j in range(n):
                if i != j:
                    diagonal_sum += abs(matrix[i][j])
            if abs(matrix[i][i]) <= diagonal_sum:
                return False
        return True

    def get_result_text(self):
        return f"Solução (Jacobi): {', '.join(f'{x:.4f}' for x in self.result)}\nIterações: {self.iterations}"

class GaussSeidelMethod(LinearSystemMethod):
    def calculate(self, matrix, vector, **kwargs):
        if not self.line_convergence(matrix) or not self.sassenfeld_convergence_criterion(matrix):
            raise ValueError("Matriz não converge. Critério de Linhas ou Sassenfeld não satisfeito.")
        
        vector = vector.tolist()
        aprox = [0] * len(matrix)
        X = [0] * len(matrix)
        max_iter = 1000  
        e = 0.0001  # precisao
        iterations = [0]
        
        self.calc_gauss_seidel(len(matrix), matrix.tolist(), vector, aprox, e, max_iter, X, iterations)
        X = [round(x, 4) for x in X]
        self.result = X
        self.iterations = iterations[0]
        return X

    def calc_gauss_seidel(self, order, matrix, vector, aprox, e, max_iterations, solution, iterations):
        current = aprox.copy()
        previous = aprox.copy()

        for iteration in range(max_iterations):
            previous = current.copy()

            for i in range(order):
                soma = 0
                for j in range(order):
                    if j != i:
                        soma += matrix[i][j] * current[j]
                current[i] = (vector[i] - soma) / matrix[i][i]

            difference = sum(abs(current[i] - previous[i]) for i in range(order))

            if difference < e:
                break

        for i in range(order):
            solution[i] = current[i]

        iterations[0] = iteration
        return solution

    def line_convergence(self, matrix):
        n = len(matrix)
        for i in range(n):
            diagonal_sum = 0
            for j in range(n):
                if i != j:
                    diagonal_sum += abs(matrix[i][j])
            if abs(matrix[i][i]) <= diagonal_sum:
                return False
        return True

    def sassenfeld_convergence_criterion(self, matrix):
        n = len(matrix)
        temp_vec = [0] * n

        for i in range(n):
            temp_sum = 0
            for j in range(n):
                if j != i:
                    temp_sum += abs(matrix[i][j])
            temp_vec[i] = temp_sum / abs(matrix[i][i])

        largest_element = max(temp_vec)
        return largest_element < 1

    def get_result_text(self):
        return f"Solução (Gauss-Seidel): {', '.join(f'{x:.4f}' for x in self.result)}\nIterações: {self.iterations}"

# ---------------------- Factory Pattern ----------------------
class MethodFactory:
    @staticmethod
    def get_method(method_name):
        methods = {
            "determinant": DeterminantMethod(),
            "lower_triangular": LowerTriangularMethod(),
            "upper_triangular": UpperTriangularMethod(),
            "lu_decomposition": LUDecompositionMethod(),
            "cholesky": CholeskyMethod(),
            "gauss_compact": GaussCompactMethod(),
            "gauss_jordan": GaussJordanMethod(),
            "jacobi": JacobiMethod(),
            "gauss_seidel": GaussSeidelMethod(),
        }
        return methods.get(method_name)

# ---------------------- Composite Pattern para as Views ----------------------
class View(ABC):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    @abstractmethod
    def setup(self):
        pass

class MainMenuView(View):
    def setup(self):
        self.frame.configure(padding="20 20 20 20")

        ttk.Label(
            self.frame,
            text="Calculadora de Sistemas Lineares",
            font=('Segoe UI', 14, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 20))

        methods = [
            ("Calcular Determinante", "determinant"),
            ("Sistema Triangular Inferior", "lower_triangular"),
            ("Sistema Triangular Superior", "upper_triangular"),
            ("Decomposição LU", "lu_decomposition"),
            ("Método de Cholesky", "cholesky"),
            ("Gauss Compacto", "gauss_compact"),
            ("Gauss-Jordan", "gauss_jordan"),
            ("Método de Jacobi", "jacobi"),
            ("Método de Gauss-Seidel", "gauss_seidel"),
        ]

        for text, method_name in methods:
            btn = ttk.Button(
                self.frame,
                text=text,
                command=lambda m=method_name: self.controller.show_method(m)
            )
            btn.pack(fill='x', pady=5)

class MethodView(View):
    def __init__(self, parent, controller, method_name):
        super().__init__(parent, controller)
        self.method_name = method_name

    def setup(self):
        self.frame.configure(padding="20 20 20 20")

        ttk.Label(
            self.frame,
            text=f"Método: {self.method_name}",
            font=('Segoe UI', 12, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 20))

        back_btn = ttk.Button(
            self.frame,
            text="◄ Voltar",
            command=self.controller.show_main_menu,
            style='Link.TButton'
        )
        back_btn.pack(anchor='w', pady=(0, 15))

        self.data_button = ttk.Button(
            self.frame,
            text="Inserir Dados" if not hasattr(self.controller, 'M') else "Alterar Dados",
            command=self.controller.show_data_input
        )
        self.data_button.pack(pady=10)

        # Verifica se o método é o determinante
        if self.method_name == "determinant":
            # Para o determinante, só precisa da matriz
            self.calculate_button = ttk.Button(
                self.frame,
                text="Calcular",
                command=self.calculate,
                state=tk.NORMAL if hasattr(self.controller, 'M') else tk.DISABLED
            )
        else:
            # Para outros métodos, precisa da matriz e do vetor
            self.calculate_button = ttk.Button(
                self.frame,
                text="Calcular",
                command=self.calculate,
                state=tk.NORMAL if hasattr(self.controller, 'M') and hasattr(self.controller, 'V') else tk.DISABLED
            )
        self.calculate_button.pack(pady=10)

        self.result_label = ttk.Label(
            self.frame,
            font=('Segoe UI', 10, 'bold'),
            background='#f0f0f0',
            padding=10
        )
        self.result_label.pack(fill='x', pady=2, ipady=5)

    def calculate(self):
        try:
            method = MethodFactory.get_method(self.method_name)
            if self.method_name == "determinant":
                result = method.calculate(self.controller.M, None)  # Não precisa do vetor
            else:
                result = method.calculate(self.controller.M, self.controller.V)
            self.result_label.config(text=method.get_result_text())
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def update_view(self):
        """Atualiza a view para refletir o estado atual dos dados."""
        if hasattr(self.controller, 'M'):
            self.data_button.config(text="Alterar Dados")
        else:
            self.data_button.config(text="Inserir Dados")

        if self.method_name == "determinant":
            self.calculate_button.config(state=tk.NORMAL if hasattr(self.controller, 'M') else tk.DISABLED)
        else:
            self.calculate_button.config(state=tk.NORMAL if hasattr(self.controller, 'M') and hasattr(self.controller, 'V') else tk.DISABLED)

class DataInputView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.matrix_entries = []
        self.vector_entries = []

    def setup(self):
        self.frame.configure(padding="20 20 20 20")

        ttk.Label(
            self.frame,
            text="Inserir Matriz e Vetor",
            font=('Segoe UI', 12, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 20))

        back_btn = ttk.Button(
            self.frame,
            text="◄ Voltar",
            command=self.controller.show_main_menu,
            style='Link.TButton'
        )
        back_btn.pack(anchor='w', pady=(0, 15))

        ttk.Label(self.frame, text="Ordem da matriz:", background='#f5f5f5').pack()
        self.order_entry = ttk.Entry(self.frame, width=10)
        self.order_entry.pack()

        ttk.Button(
            self.frame,
            text="Confirmar Ordem",
            command=self.create_entries
        ).pack(pady=10)

        self.matrix_frame = ttk.Frame(self.frame)
        self.matrix_frame.pack()

        self.vector_frame = ttk.Frame(self.frame)
        self.vector_frame.pack()

        ttk.Button(
            self.frame,
            text="Confirmar Dados",
            command=self.confirm_data
        ).pack(pady=10)

    def create_entries(self):
        try:
            order = int(self.order_entry.get())
            if order < 1 or order > 10:
                raise ValueError("A ordem da matriz deve estar entre 1 e 10.")
            
            # Limpa entradas anteriores
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            for widget in self.vector_frame.winfo_children():
                widget.destroy()

            self.matrix_entries = []
            for i in range(order):
                row_entries = []
                for j in range(order):
                    entry = ttk.Entry(self.matrix_frame, width=8)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)

            ttk.Label(self.vector_frame, text="Vetor de termos independentes:", background='#f5f5f5').pack()
            self.vector_entries = []
            for i in range(order):
                entry = ttk.Entry(self.vector_frame, width=8)
                entry.pack(pady=2)
                self.vector_entries.append(entry)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def confirm_data(self):
        try:
            order = int(self.order_entry.get())
            matrix = np.zeros((order, order))
            vector = np.zeros(order)

            for i in range(order):
                for j in range(order):
                    matrix[i][j] = float(self.matrix_entries[i][j].get())

            for i in range(order):
                vector[i] = float(self.vector_entries[i].get())

            self.controller.M = matrix
            self.controller.V = vector
            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            self.controller.show_main_menu()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

# ---------------------- Controlador Principal ----------------------
class LinearSystemCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x520')
        self.minsize(480, 520)
        self.resizable(0, 0)
        self.title('Calculadora de Sistemas Lineares')
        self.configure(bg='#f5f5f5')

        self.setup_styles()

        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)

        self.views = {}
        self.current_view = None

        self.setup_main_menu()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Link.TButton', font=('Segoe UI', 9), background='#f5f5f5', foreground='blue')

    def setup_main_menu(self):
        self.main_menu = MainMenuView(self.container, self)
        self.main_menu.setup()
        self.views['main_menu'] = self.main_menu
        self.show_view('main_menu')

    def show_view(self, view_name):
        if self.current_view:
            self.current_view.hide()
        self.current_view = self.views[view_name]
        self.current_view.show()

        # Atualiza a view se for uma MethodView
        if isinstance(self.current_view, MethodView):
            self.current_view.update_view()

    def show_main_menu(self):
        self.show_view('main_menu')

    def show_method(self, method_name):
        view_name = f'method_{method_name}'
        if view_name not in self.views:
            method_view = MethodView(self.container, self, method_name)
            method_view.setup()
            self.views[view_name] = method_view
        self.show_view(view_name)

    def show_data_input(self):
        if 'data_input' not in self.views:
            data_input_view = DataInputView(self.container, self)
            data_input_view.setup()
            self.views['data_input'] = data_input_view
        self.show_view('data_input')

if __name__ == "__main__":
    app = LinearSystemCalculator()
    app.mainloop()