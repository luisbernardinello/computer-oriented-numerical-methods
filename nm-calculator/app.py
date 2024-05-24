import numpy as np
import tkinter as tk
from tkinter import messagebox


# caso não esteja funcionando o módulo tkinter verificar se a opção Install Tcl/Tk and IDLE foi marcada durante a instalação do Python 3

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora MNC")
        self.master.resizable(False, False) 
        
        ##### centralizar janela  
        window_width = 400  
        window_height = 550 

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ##### options
        self.options = [
            "Entrar com matriz",
            "Entrar com vetor de termos independentes",
            "Calcular o determinante",
            "Calcular o sistema triangular inferior",
            "Calcular o sistema triangular superior",
            "Calcular pelo método de Decomposicao LU",
            "Calcular pelo método de Cholesky",
            "Calcular pelo método de Gauss Compacto",
            "Calcular pelo método de Gauss Jordan",
            "Calcular pelo método de Jacobi",
            "Calcular pelo método de Gauss-Seidel",
            "Calcular matriz inversa",
            "Sair"
        ]
        
        self.selection = tk.StringVar(value=self.options[0])
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, bg="gray89")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.menu_label = tk.Label(self.frame, text="Por favor, escolha uma das opções abaixo:", bg="LightBlue", font=("Trebuchet MS", 9, "bold"))
        self.menu_label.pack()

        
        option_groups = {
            "Entrada de Dados": [
                "Entrar com matriz",
                "Entrar com vetor de termos independentes"
            ],
            "Determinante": [
                "Calcular o determinante",
            ],
            "Sistemas Triangulares": [
                "Calcular o sistema triangular inferior",
                "Calcular o sistema triangular superior"
            ],
            "Métodos Diretos": [
                "Calcular pelo método de Decomposicao LU",
                "Calcular pelo método de Cholesky",
                "Calcular pelo método de Gauss Compacto",
                "Calcular pelo método de Gauss Jordan"
            ],
            "Métodos Iterativos": [
                "Calcular pelo método de Jacobi",
                "Calcular pelo método de Gauss-Seidel"
            ],
            "Matriz Inversa": [
                "Calcular matriz inversa"
            ]
            
        }

        # rotulos e radiobuttons para cada label
        for group_label, options in option_groups.items():
            group_label_widget = tk.Label(self.frame, text=group_label, bg="LightBlue", font=("Trebuchet MS", 9, "bold"))
            group_label_widget.pack(anchor=tk.W)

            for option in options:
                tk.Radiobutton(
                    self.frame,
                    text=option,
                    variable=self.selection,
                    value=option,
                    bg="gray89"
                ).pack(anchor=tk.W, padx=20, pady=2)

        self.confirm_button = tk.Button(self.frame, text="Confirmar", command=self.handle_selection)
        self.confirm_button.pack()


    def handle_selection(self):
        selected_option = self.selection.get()
        
        if selected_option == "Sair":
            self.master.destroy()

        elif selected_option == "Entrar com matriz":
            self.enter_matrix()

        elif selected_option == "Entrar com vetor de termos independentes":
            self.enter_vector()   

        elif selected_option == "Calcular o determinante":
            if not hasattr(self, 'M'):
                messagebox.showerror("Erro", "Nenhuma matriz foi inserida.")
            else:
                determinant = self.calc_determinant(self.M)
                messagebox.showinfo("Resultado", f"O determinante é: {round(determinant, 4)}")

        elif selected_option == "Calcular o sistema triangular inferior":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calc_lower_triangular(len(self.M), self.M, self.V)
                X = [round(x, 4) for x in X]
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular o sistema triangular superior":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calc_upper_triangular(len(self.M), self.M, self.V)
                X = [round(x, 4) for x in X]
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular pelo método de Decomposicao LU":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                determinant = self.calc_determinant(self.M)
                if determinant == 0:
                    messagebox.showerror("Erro", "A matriz inserida não converge. O determinante é igual a zero.")
                else:
                    triangular_matrix_L, triangular_matrix_U, vector = self.calc_LU_decomposition(len(self.M), self.M, self.V)
                    X = self.aux_LU(len(self.M), triangular_matrix_L, triangular_matrix_U, vector)
                    X = [0 if abs(x) < 1e-10 else round(x, 4) for x in X]
                    messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular pelo método de Cholesky":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                determinant = self.calc_determinant(self.M)
                calc_simetric = self.calc_simetric(self.M)
                if determinant < 0:
                    messagebox.showerror("Erro", "A matriz inserida não é definida positiva.")
                elif calc_simetric == False:
                    messagebox.showerror("Erro", "A matriz inserida não é simétrica.")
                else:
                    X = self.calc_cholesky(len(self.M), self.M, self.V)
                    X = [0 if abs(x) < 1e-10 else round(x, 4) for x in X]
                    messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular pelo método de Gauss Compacto":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calc_compact_gauss(len(self.M), self.M, self.V)
                X = [0 if abs(x) < 1e-10 else round(x, 4) for x in X]
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular pelo método de Gauss Jordan":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calc_gauss_jordan(len(self.M), self.M, self.V)
                if X is None:
                    messagebox.showerror("Erro", "O sistema gerado é indeterminado.")
                else:
                    X = [0 if abs(x) < 1e-10 else round(x, 4) for x in X]
                    messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")

        elif selected_option == "Calcular pelo método de Jacobi":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                vector = self.V.tolist()
                aprox = [0] * len(self.M)
                X = [0] * len(self.M)
                max_iter = 1000  
                e = 0.0001  # precisao
                iterations = [0]
                if not self.column_convergence(self.M) or not self.line_convergence(self.M):
                    messagebox.showerror("Erro", "Matriz não converge. Criterio de Linhas ou Colunas não satisfeito.")
                else:
                    self.calc_jacobi(len(self.M), self.M.tolist(), vector, aprox, e, max_iter, X, iterations)
                    X = [round(x, 4) for x in X]
                    result_str = f"Os valores de X são: {', '.join(map(str, X))}\nNúmero de iterações: {iterations[0]}"
                    messagebox.showinfo("Resultado", result_str)

        elif selected_option == "Calcular pelo método de Gauss-Seidel":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                vector = self.V.tolist()
                aprox = [0] * len(self.M)
                X = [0] * len(self.M)
                max_iter = 1000  # iteracoes
                e = 0.0001  # precisao
                iterations = [0]
                if not self.line_convergence(self.M) or not self.sassenfeld_convergence_criterion(self.M):
                    messagebox.showerror("Erro", "Matriz não converge. Criterio de Linhas ou Sassenfeld não satisfeito.")
                else:
                    self.calc_gauss_seidel(len(self.M), self.M.tolist(), vector, aprox, e, max_iter, X, iterations)
                    X = [round(x, 4) for x in X]
                    result_str = f"Os valores de X são: {', '.join(map(str, X))}\nNúmero de iterações: {iterations[0]}"
                    messagebox.showinfo("Resultado", result_str)

        elif selected_option == "Calcular matriz inversa":
            if not hasattr(self, "M"):
                messagebox.showerror("Erro", "Matriz não foi inserida")
            else:
                self.inverse_matrix_calculator()



################################################################ INSERE MATRIZ E VETOR DE TERMOS INDEPENDENTES

    def enter_matrix(self):
        self.matrix_window = tk.Toplevel(self.master)
        self.matrix_window.title("Entrar com matriz")
        self.matrix_window.resizable(False, False)

        

        self.matrix_frame = tk.Frame(self.matrix_window, bg="gray89")
        self.matrix_frame.pack(fill=tk.BOTH, expand=True)

        self.order_label = tk.Label(self.matrix_frame, text="Ordem da matriz:", bg="gray89")
        self.order_label.grid(row=0, column=0, padx=5, pady=5)

        self.order_entry = tk.Entry(self.matrix_frame, width=5)
        self.order_entry.grid(row=0, column=1, padx=5, pady=5)

        self.confirm_order_button = tk.Button(self.matrix_frame, text="Confirmar", command=self.create_matrix_entries)
        self.confirm_order_button.grid(row=0, column=2, padx=5, pady=5)

    def create_matrix_entries(self):
        order = self.order_entry.get()
        try:
            order = int(order)
        except ValueError:
            messagebox.showerror("Erro", "Insira um numero inteiro válido.")
            return
        self.order = order #armazena ordem

        self.matrix_entries = []
        for i in range(order):
            row_entries = []
            for j in range(order):
                entry = tk.Entry(self.matrix_frame, width=8)
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        self.confirm_matrix_button = tk.Button(self.matrix_frame, text="Confirmar", command=self.confirm_matrix)
        self.confirm_matrix_button.grid(row=order+1, column=0, columnspan=order, padx=5, pady=5)

    def confirm_matrix(self):
        order = len(self.matrix_entries)
        M = np.zeros((order, order))
        for i in range(order):
            for j in range(order):
                entry_value = self.matrix_entries[i][j].get()
                try:
                    M[i][j] = float(entry_value)
                except ValueError:
                    messagebox.showerror("Erro", "Insira somente numeros válidos.")
                    return
        self.M = M
        self.matrix_window.destroy()
        messagebox.showinfo("Sucesso", "Matriz inserida com sucesso.")

    def enter_vector(self):
        if not hasattr(self, 'order'):
            messagebox.showerror("Erro", "Entre com o valor da matriz antes do vetor.")
            return

        self.vector_window = tk.Toplevel(self.master)
        self.vector_window.title("Entrar com o vetor de termos independentes")
        self.vector_window.resizable(False, False)

        self.vector_frame = tk.Frame(self.vector_window, bg="gray89")
        self.vector_frame.pack(fill=tk.BOTH, expand=True)

        self.order_label = tk.Label(self.vector_frame, text=f"Tamanho do vetor (ordem da matriz: {self.order}):", bg="gray89")
        self.order_label.grid(row=0, column=0, padx=5, pady=5)

        self.vector_entries = []
        for i in range(self.order):
            entry = tk.Entry(self.vector_frame, width=8)
            entry.grid(row=i + 1, column=0, padx=5, pady=5)
            self.vector_entries.append(entry)

        self.confirm_vector_button = tk.Button(self.vector_frame, text="Confirmar", command=self.confirm_vector)
        self.confirm_vector_button.grid(row=self.order + 1, column=0, padx=5, pady=5)

    def confirm_vector(self):
        V = []
        for entry in self.vector_entries:
            value = entry.get()
            try:
                V.append(float(value))
            except ValueError:
                messagebox.showerror("Erro", "Insira apenas números válidos para o vetor.")
                return

        self.V = np.array(V)
        self.vector_window.destroy()
        messagebox.showinfo("Sucesso", "Vetor inserido com sucesso.")




############################################################################  DETERMINANTE

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

############################################################################ MATRIZ INVERSA

    ##### metodos auxiliares para exibir e calcular matriz inversa
    def inverse_matrix_calculator(self):
        inverse_matrix_window = tk.Toplevel()
        inverse_matrix_window.title("Matriz Inversa")
        inverse_matrix_window.resizable(False, False)

        

        inverse_matrix_options = [
            "Calcular Matriz Inversa por Gauss Compacto",
            "Calcular por Decomposição LU",
        ]

        inverse_matrix_selection = tk.StringVar(value=inverse_matrix_options[0])

        for option in inverse_matrix_options:
            tk.Radiobutton(
                inverse_matrix_window,
                text=option,
                variable=inverse_matrix_selection,
                value=option,
                bg="gray89"
            ).pack(anchor=tk.W)

        confirm_button_inverse_matrix = tk.Button(inverse_matrix_window, text="Confirmar", command=lambda: self.confirm_inverse_matrix(inverse_matrix_selection))
        confirm_button_inverse_matrix.pack()

    def confirm_inverse_matrix(self, inverse_matrix_selection):
        selected_inverse_matrix_option = inverse_matrix_selection.get()
        if selected_inverse_matrix_option == "Calcular Matriz Inversa por Gauss Compacto":
            order = len(self.M)
            inversa = self.inverse_matrix_gauss(order, self.M)
            if inversa is not None:
                self.show_inverse_matrix(inversa)
        elif selected_inverse_matrix_option == "Calcular por Decomposição LU":
            order = len(self.M)
            inversa = self.inverse_matrix_lu(order, self.M)
            if inversa is not None:
                self.show_inverse_matrix(inversa)


    def show_inverse_matrix(self, inversa):
        result_window = tk.Toplevel(self.master)
        result_window.title("Resultado da Matriz Inversa")
        result_window.resizable(False, False)

        # Label para o resultado
        result_label = tk.Label(result_window, text="Matriz Inversa:")
        result_label.grid(row=0, column=0, columnspan=len(inversa[0]))

        # Elementos da matriz como labels
        for i, row in enumerate(inversa):
            for j, cell in enumerate(row):
                cell_label = tk.Label(result_window, text=f"{round(cell, 4)}", relief=tk.RIDGE, width=10, height=2)
                cell_label.grid(row=i+1, column=j, padx=5, pady=5)

        close_button = tk.Button(result_window, text="Fechar", command=result_window.destroy)
        close_button.grid(row=len(inversa)+1, column=0, columnspan=len(inversa[0]), pady=10)




    ##### matriz inversa por decomposição LU
    def aux_inverse_matrix_lu(self, order, matrix, triangular_matrix_L, triangular_matrix_U):
        for i in range(order):
            for j in range(order):
                triangular_matrix_U[i][j] = matrix[i][j]

        for k in range(order):
            triangular_matrix_L[k][k] = 1.0

            for i in range(k + 1, order):
                triangular_matrix_L[i][k] = triangular_matrix_U[i][k] / triangular_matrix_U[k][k]
                for j in range(k, order):
                    triangular_matrix_U[i][j] -= triangular_matrix_L[i][k] * triangular_matrix_U[k][j]



    def inverse_matrix_lu(self, order, matrix):
        triangular_matrix_L = [[0] * order for _ in range(order)]
        triangular_matrix_U = [[0] * order for _ in range(order)]
        ident = [[1 if i == j else 0 for j in range(order)] for i in range(order)]

        self.aux_inverse_matrix_lu(order, matrix, triangular_matrix_L, triangular_matrix_U)

        y = [[0] * order for _ in range(order)]

        # Ly = i
        for k in range(order):
            for i in range(order):
                soma = sum(triangular_matrix_L[i][j] * y[j][k] for j in range(i))
                y[i][k] = (ident[i][k] - soma) / triangular_matrix_L[i][i]

        inversa = [[0] * order for _ in range(order)]

        # Ux = y
        for k in range(order):
            for i in range(order - 1, -1, -1):
                soma = sum(triangular_matrix_U[i][j] * inversa[j][k] for j in range(i + 1, order))
                inversa[i][k] = (y[i][k] - soma) / triangular_matrix_U[i][i]

        return inversa


    ##### calcular matriz inversa por Gauss Compacto

    def inverse_matrix_gauss(self, order, matrix):
        augmented_matrix = [[0] * (2 * order) for _ in range(order)]

        for i in range(order):
            for j in range(order):
                augmented_matrix[i][j] = matrix[i][j]
                augmented_matrix[i][j + order] = 1.0 if i == j else 0.0

        # Gauss compacto
        for i in range(order):
            pivot = augmented_matrix[i][i]

            if pivot == 0:
                swap = False

                for j in range(i + 1, order):
                    if augmented_matrix[j][i] != 0:
                        swap = True
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break

                if not swap:
                    messagebox.showerror("Erro", "A matriz não é invertível")
                    return None

                pivot = augmented_matrix[i][i]

            for j in range(2 * order):
                augmented_matrix[i][j] /= pivot

            for k in range(order):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(2 * order):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

        inversa = [[augmented_matrix[i][j + order] for j in range(order)] for i in range(order)]
        return inversa

    

        

################################################################ SISTEMAS TRIANGULARES       
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
    
  ################################################################ METODOS DIRETOS
  
  
   ###### decomposiçãoLU
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

    def calc_LU_decomposition(self, ordem, matrix, vector):
        triangular_matrix_U = np.zeros((ordem, ordem))
        triangular_matrix_L = np.zeros((ordem, ordem))

        for i in range(ordem):
            self.calc_triangular_matrix_U(i, ordem, matrix, triangular_matrix_L, triangular_matrix_U)
            self.calc_triangular_matrix_L(i, ordem, matrix, triangular_matrix_L, triangular_matrix_U)

        return triangular_matrix_L, triangular_matrix_U, vector
    
    ###### cholesky
    def calc_simetric(self, matrix):
        order = len(matrix)
        for i in range(order):
            for j in range(order):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True
    

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



    ###### gauss compacto

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
    

    ###### gauss jordan
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
    

############################################################################## METODOS ITERATIVOS


    ###### metodos auxiliares para os metodos iterativos

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


    ###### Método de Jacobi

    def calc_jacobi(self,order, matrix, vector, aprox, e, max_iterations, solution, iterations):
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
    

    ###### Método de Gauss Seidel

    def calc_gauss_seidel(self,order, matrix, vector, aprox, e, max_iterations, solution, iterations):
        current = aprox.copy()
        previous  = aprox.copy()

        for iteration in range(max_iterations):
            previous  = current.copy()

            for i in range(order):
                soma = 0
                for j in range(order):
                    if j != i:
                        soma += matrix[i][j] * current[j]
                current[i] = (vector[i] - soma) / matrix[i][i]

            difference = sum(abs(current[i] - previous [i]) for i in range(order))

            if difference < e:
                break

        for i in range(order):
            solution[i] = current[i]

        iterations[0] = iteration
        return solution


###################################################################### MAIN
def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
    
    

if __name__ == "__main__":
    main()
