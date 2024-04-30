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
            "Calcular matriz inversa (Decomposição LU)",
            "Calcular matriz inversa (Gauss Compacto)",
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

    def calcular_determinante(self, matriz):
        n = len(matriz)
        if n == 1:
            return matriz[0][0]
        else:
            resp = 0
            for i in range(n):
                if matriz[0][i] != 0:
                    matriz_aux = np.delete(matriz, 0, axis=0)
                    matriz_aux = np.delete(matriz_aux, i, axis=1)
                    pivo = matriz[0][i] if i % 2 == 0 else -matriz[0][i]
                    resp += pivo * self.calcular_determinante(matriz_aux)
            return resp
        
    def calcular_triangular_inferior(self, n, M, V):
        X = np.zeros(n)
        for i in range(n):
            if i == 0:
                X[0] = V[0] / M[0][0]
            else:
                soma = 0
                for j in range(i):
                    soma += M[i][j] * X[j]
                X[i] = (V[i] - soma) / M[i][i]
        return X

    def calcular_triangular_superior(self, n, M, V):
        X = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                X[i] = V[i] / M[i][i]
            else:
                soma = 0
                for j in range(i + 1, n):
                    soma += M[i][j] * X[j]
                X[i] = (V[i] - soma) / M[i][i]
        return X

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
