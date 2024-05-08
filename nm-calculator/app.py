import numpy as np
import tkinter as tk
from tkinter import messagebox

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora MNC")
        self.master.resizable(False, False)  # Impede redimensionamento
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.menu_label = tk.Label(self.frame, text="Por favor, escolha uma das opções abaixo:", bg="white")
        self.menu_label.pack()

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

        for option in self.options:
            tk.Radiobutton(
                self.frame,
                text=option,
                variable=self.selection,
                value=option,
                bg="white"
            ).pack(anchor=tk.W)

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
                determinant = self.calcular_determinante(self.M)
                messagebox.showinfo("Resultado", f"O determinante é: {determinant:.3f}")
        elif selected_option == "Calcular o sistema triangular inferior":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calcular_triangular_inferior(len(self.M), self.M, self.V)
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")
        elif selected_option == "Calcular o sistema triangular superior":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.calcular_triangular_superior(len(self.M), self.M, self.V)
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")
        elif selected_option == "Calcular pelo método de Decomposicao LU":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                determinant = self.calcular_determinante(self.M)
                if determinant == 0:
                    messagebox.showerror("Erro", "A matriz inserida não converge. O determinante é igual a zero.")
                else:
                    L, U, B = self.decomposicao_lu(len(self.M), self.M, self.V)
                    X = self.sistema_lu(len(self.M), L, U, B)
                    for i in range(len(X)):
                        if abs(X[i]) < 1e-10:  # Limiar de tolerância para valores muito proximos de zero para printar zero
                            X[i] = 0
                    messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")
        elif selected_option == "Calcular pelo método de Gauss Compacto":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.gauss_compacto(len(self.M), self.M, self.V)
                for i in range(len(X)):
                        if abs(X[i]) < 1e-10:  # Limiar de tolerância para valores muito proximos de zero para printar zero
                            X[i] = 0
                messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")
        elif selected_option == "Calcular pelo método de Gauss Jordan":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                X = self.gauss_jordan(len(self.M), self.M, self.V)
                if X is None:
                    messagebox.showerror("Erro", "O sistema gerado é indeterminado.")
                else:
                    for i in range(len(X)):
                        if abs(X[i]) < 1e-10:  # Limiar de tolerância para valores muito proximos de zero para printar zero
                            X[i] = 0
                    messagebox.showinfo("Resultado", f"Os valores de X são: {', '.join(map(str, X))}")
        elif selected_option == "Calcular pelo método de Jacobi":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                B = self.V.tolist()
                aproximacao = [0] * len(self.M)
                X = [0] * len(self.M)
                max_iter = 1000  # Defina o número máximo de iterações
                e = 0.0001  # Defina a precisão desejada
                iteracoes = [0]
                if not self.criterio_colunas(self.M) or not self.criterio_linhas(self.M):
                    messagebox.showerror("Erro", "Matriz não converge. Criterio de Linhas ou Colunas não satisfeito.")
                else:
                    self.jacobi(len(self.M), self.M.tolist(), B, aproximacao, e, max_iter, X, iteracoes)
                    result_str = f"Os valores de X são: {', '.join(map(str, X))}\nNúmero de iterações: {iteracoes[0]}"
                    messagebox.showinfo("Resultado", result_str)

        elif selected_option == "Calcular pelo método de Gauss-Seidel":
            if not hasattr(self, 'M') or not hasattr(self, 'V'):
                messagebox.showerror("Erro", "Matriz ou vetor V não foram inseridos.")
            else:
                B = self.V.tolist()
                aproximacao = [0] * len(self.M)
                X = [0] * len(self.M)
                max_iter = 1000  # Defina o número máximo de iterações
                e = 0.0001  # Defina a precisão desejada
                iteracoes = [0]
                if not self.criterio_linhas(self.M) or not self.criterio_sassenfeld(self.M):
                    messagebox.showerror("Erro", "Matriz não converge. Criterio de Linhas ou Sassenfeld não satisfeito.")
                else:
                    self.gauss_seidel(len(self.M), self.M.tolist(), B, aproximacao, e, max_iter, X, iteracoes)
                    result_str = f"Os valores de X são: {', '.join(map(str, X))}\nNúmero de iterações: {iteracoes[0]}"
                    messagebox.showinfo("Resultado", result_str)

        elif selected_option == "Calcular matriz inversa":
            if not hasattr(self, "M"):
                messagebox.showerror("Erro", "Matriz não foi inserida")
            else:
                self.inverse_matrix_calculator()
                





    def enter_matrix(self):
        self.matrix_window = tk.Toplevel(self.master)
        self.matrix_window.title("Entrar com matriz")
        self.matrix_window.resizable(False, False)

        self.matrix_frame = tk.Frame(self.matrix_window, bg="white")
        self.matrix_frame.pack(fill=tk.BOTH, expand=True)

        self.order_label = tk.Label(self.matrix_frame, text="Ordem da matriz:", bg="white")
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

        self.vector_frame = tk.Frame(self.vector_window, bg="white")
        self.vector_frame.pack(fill=tk.BOTH, expand=True)

        self.order_label = tk.Label(self.vector_frame, text=f"Tamanho do vetor (ordem da matriz: {self.order}):", bg="white")
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

    def inverse_matrix_calculator(self):
        if not hasattr(self, "inverse_matrix_window"):
            self.inverse_matrix_window = tk.Toplevel(self.master)
            self.inverse_matrix_window.title("Matriz Inversa")
            self.inverse_matrix_window.resizable(False, False)

            self.inverse_matrix_options = [
                "Calcular Matriz Inversa por Gauss Compacto",
                "Calcular por Decomposição LU",
            ]

            self.inverse_matrix_selection = tk.StringVar(value=self.inverse_matrix_options[0])

            for inverse_matrix_options in self.inverse_matrix_options:
                tk.Radiobutton(
                    self.inverse_matrix_window,
                    text=inverse_matrix_options,
                    variable=self.inverse_matrix_selection,
                    value=inverse_matrix_options,
                    bg="white"
                ).pack(anchor=tk.W)

            self.confirm_button_inverse_matrix = tk.Button(self.inverse_matrix_window, text="Confirmar", command=self.confirm_inverse_matrix)
            self.confirm_button_inverse_matrix.pack()

    def confirm_inverse_matrix(self):
        selected_inverse_matrix_option = self.inverse_matrix_selection.get()
        if selected_inverse_matrix_option == "Calcular Matriz Inversa por Gauss Compacto":
            ordem = len(self.M)
            inversa = self.inversa_gauss(ordem, self.M)
            if inversa is not None:
                self.show_inverse_matrix(inversa)
        elif selected_inverse_matrix_option == "Calcular por Decomposição LU":
            ordem = len(self.M)
            inversa = self.inversa_lu(ordem, self.M)
            if inversa is not None:
                self.show_inverse_matrix(inversa)

    def show_inverse_matrix(self, inversa):
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Resultado da Matriz Inversa")
        
        result_window.resizable(False, False)

        #  label para o resultado
        result_label = tk.Label(result_window, text="Matriz Inversa:")
        result_label.grid(row=0, column=0, columnspan=len(inversa[0]))

        # elementos da matriz como labels
        for i, row in enumerate(inversa):
            for j, cell in enumerate(row):
                cell_label = tk.Label(result_window, text=str(cell), relief=tk.RIDGE, width=5, height=2)
                cell_label.grid(row=i+1, column=j, padx=5, pady=5)

        close_button = tk.Button(result_window, text="Fechar", command=result_window.destroy)
        close_button.grid(row=len(inversa)+1, column=0, columnspan=len(inversa[0]), pady=10)

    def sist_inversa_lu(self, ordem, matriz, L, U):
        for i in range(ordem):
            for j in range(ordem):
                U[i][j] = matriz[i][j]

        for k in range(ordem):
            L[k][k] = 1.0

            for i in range(k + 1, ordem):
                L[i][k] = U[i][k] / U[k][k]
                for j in range(k, ordem):
                    U[i][j] -= L[i][k] * U[k][j]



    def inversa_lu(self, ordem, matriz):
        L = [[0] * ordem for _ in range(ordem)]
        U = [[0] * ordem for _ in range(ordem)]
        identidade = [[1 if i == j else 0 for j in range(ordem)] for i in range(ordem)]

        self.sist_inversa_lu(ordem, matriz, L, U)

        y = [[0] * ordem for _ in range(ordem)]

        # Sistema Ly = I
        for k in range(ordem):
            for i in range(ordem):
                soma = sum(L[i][j] * y[j][k] for j in range(i))
                y[i][k] = (identidade[i][k] - soma) / L[i][i]

        inversa = [[0] * ordem for _ in range(ordem)]

        # Sistema Ux = y
        for k in range(ordem):
            for i in range(ordem - 1, -1, -1):
                soma = sum(U[i][j] * inversa[j][k] for j in range(i + 1, ordem))
                inversa[i][k] = (y[i][k] - soma) / U[i][i]

        return inversa

    def inversa_gauss(self, ordem, matriz):
        matriz_aumentada = [[0] * (2 * ordem) for _ in range(ordem)]

        for i in range(ordem):
            for j in range(ordem):
                matriz_aumentada[i][j] = matriz[i][j]
                matriz_aumentada[i][j + ordem] = 1.0 if i == j else 0.0

        # Gauss compacto
        for i in range(ordem):
            pivo = matriz_aumentada[i][i]

            if pivo == 0:
                troca = False

                for j in range(i + 1, ordem):
                    if matriz_aumentada[j][i] != 0:
                        troca = True
                        matriz_aumentada[i], matriz_aumentada[j] = matriz_aumentada[j], matriz_aumentada[i]
                        break

                if not troca:
                    messagebox.showerror("Erro", "A matriz não é invertível")
                    return None

                pivo = matriz_aumentada[i][i]

            for j in range(2 * ordem):
                matriz_aumentada[i][j] /= pivo

            for k in range(ordem):
                if k != i:
                    fator = matriz_aumentada[k][i]
                    for j in range(2 * ordem):
                        matriz_aumentada[k][j] -= fator * matriz_aumentada[i][j]

        inversa = [[matriz_aumentada[i][j + ordem] for j in range(ordem)] for i in range(ordem)]
        return inversa

    

    def calcular_determinante(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        else:
            resp = 0
            for i in range(n):
                if matrix[0][i] != 0:
                    matrix_aux = np.delete(matrix, 0, axis=0)
                    matrix_aux = np.delete(matrix_aux, i, axis=1)
                    pivo = matrix[0][i] if i % 2 == 0 else -matrix[0][i]
                    resp += pivo * self.calcular_determinante(matrix_aux)
            return resp
        
    def calcular_triangular_inferior(self, n, matrix, vector):
        X = np.zeros(n)
        for i in range(n):
            if i == 0:
                X[0] = vector[0] / matrix[0][0]
            else:
                soma = 0
                for j in range(i):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X

    def calcular_triangular_superior(self, n, matrix, vector):
        X = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                X[i] = vector[i] / matrix[i][i]
            else:
                soma = 0
                for j in range(i + 1, n):
                    soma += matrix[i][j] * X[j]
                X[i] = (vector[i] - soma) / matrix[i][i]
        return X
    
    # decomposiçãoLU
    def matriz_u(self, i, n, matrix, L, U):
        for j in range(n):
            if i == 0:
                U[i][j] = matrix[i][j]
            else:
                soma = 0
                for k in range(i):
                    soma += L[i][k] * U[k][j]
                U[i][j] = matrix[i][j] - soma

    def matriz_l(self, j, n, matrix, L, U):
        for i in range(n):
            if j == 0:
                L[i][j] = matrix[i][j] / U[j][j]
            else:
                soma = 0
                for k in range(j):
                    soma += L[i][k] * U[k][j]
                L[i][j] = (matrix[i][j] - soma) / U[j][j]

    def sistema_lu(self, n, L, U, B):
        Y = np.zeros(n)

        # Ly = B
        Y[0] = B[0] / L[0][0]
        for i in range(1, n):
            soma = 0
            for j in range(i):
                soma += L[i][j] * Y[j]
            Y[i] = (B[i] - soma) / L[i][i]

        # Ux = y
        X = np.zeros(n)
        X[n - 1] = Y[n - 1] / U[n - 1][n - 1]
        for i in range(n - 2, -1, -1):
            soma = 0
            for j in range(i + 1, n):
                soma += U[i][j] * X[j]
            X[i] = (Y[i] - soma) / U[i][i]

        return X

    def decomposicao_lu(self, n, M, B):
        U = np.zeros((n, n))
        L = np.zeros((n, n))

        for i in range(n):
            self.matriz_u(i, n, M, L, U)
            self.matriz_l(i, n, M, L, U)

        return L, U, B
    
    #cholesky
    def simetrica(self, matrix, order):
        for i in range(order):
            for j in range(order):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True

    def definida_positiva(self, matrix, order):
        for cont in range(1, order + 1):
            aux = matrix[:cont, :cont]
            if np.linalg.det(aux) <= 10e-7:
                return False
        return True
    




    # gauss compacto

    def gauss_compacto(self, n, M, B):
        X = np.zeros(n)

        for k in range(n - 1):
            for i in range(k + 1, n):
                aux = M[i][k] / M[k][k]
                B[i] -= aux * B[k]
                for j in range(k, n):
                    M[i][j] -= aux * M[k][j]

        X[n - 1] = B[n - 1] / M[n - 1][n - 1]

        for i in range(n - 2, -1, -1):
            aux = B[i]
            for j in range(i + 1, n):
                aux -= M[i][j] * X[j]
            X[i] = aux / M[i][i]

        return X
    

    # gauss jordan
    def gauss_jordan(self, n, M, B):
        matrizAumentada = np.zeros((n, n + 1))

        for i in range(n):
            for j in range(n + 1):
                if j == n:
                    matrizAumentada[i][j] = B[i]
                else:
                    matrizAumentada[i][j] = M[i][j]

        for i in range(n):
            pivo = matrizAumentada[i][i]
            if pivo == 0:
                return None  # Sistema indeterminado
            else:
                for j in range(i, n + 1):
                    matrizAumentada[i][j] /= pivo

                for k in range(n):
                    if k != i:
                        fator = matrizAumentada[k][i]
                        for j in range(i, n + 1):
                            matrizAumentada[k][j] -= fator * matrizAumentada[i][j]

        X = np.zeros(n)
        for i in range(n):
            X[i] = matrizAumentada[i][n]

        return X
    

##############################################################################
    #aqui começa os métodos iterativos

    #metodos auxiliares para os metodos iterativos

    def criterio_colunas(self, B):
        valor_max = -1
        for i in range(len(B)):
            aux = 0
            for j in range(len(B)):
                if i != j:
                    aux += abs(B[j][i])
            if aux > valor_max:
                valor_max = aux
        return valor_max < 1

    def criterio_linhas(self, B):
        valor_max = -1
        for i in range(len(B)):
            aux = 0
            for j in range(len(B)):
                if i != j:
                    aux += abs(B[j][i])
            if aux > valor_max:
                valor_max = aux
        return valor_max < 1

    def criterio_sassenfeld(self, B):
        auxB = [0] * len(B)
        for i in range(len(B)):
            for j in range(len(B)):
                if j < i:
                    auxB[i] += B[i][j] * auxB[j]
                else:
                    auxB[i] += B[i][j]
        
        maior = auxB[0]
        for i in range(1, len(B)):
            if auxB[i] > maior:
                maior = auxB[i]
        return maior < 1

    def calcula_erro(self, initialX, solution):
        erro = abs(solution[0] - initialX[0])
        valor_max = abs(solution[0])

        for i in range(1, len(initialX)):
            if abs(solution[i] - initialX[i]) > erro:
                erro = abs(solution[i] - initialX[i])
            if abs(solution[i]) > valor_max:
                valor_max = abs(solution[i])

        return erro / valor_max
    
    #jacobi


    def jacobi(n, M, vetorB, aproximacao, e, maxIter, X, iteracoes):
        temp = [0] * n

        for iter in range(1, maxIter + 1):
            erro = 0.0

            for i in range(n):
                temp[i] = vetorB[i]
                for j in range(n):
                    if i != j:
                        temp[i] -= M[i][j] * aproximacao[j]
                temp[i] /= M[i][i]

            for i in range(n):
                erro += (temp[i] - aproximacao[i]) * (temp[i] - aproximacao[i])

            for i in range(n):
                aproximacao[i] = temp[i]

            if erro < e:
                break

        for i in range(n):
            X[i] = aproximacao[i]

        iteracoes[0] = iter
        return X
    

    #gauss seidel

    def gauss_seidel(ordem, matriz, B, aproximacao, e, maxIter, X, iteracoes):
        aprox_atual = aproximacao.copy()
        aprox_anterior = aproximacao.copy()

        for iteracao in range(maxIter):
            aprox_anterior = aprox_atual.copy()

            for i in range(ordem):
                soma = 0
                for j in range(ordem):
                    if j != i:
                        soma += matriz[i][j] * aprox_atual[j]
                aprox_atual[i] = (B[i] - soma) / matriz[i][i]

            diferenca = sum(abs(aprox_atual[i] - aprox_anterior[i]) for i in range(ordem))

            if diferenca < e:
                break

        for i in range(ordem):
            X[i] = aprox_atual[i]

        iteracoes[0] = iteracao
        return X


    

    


#main
def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
