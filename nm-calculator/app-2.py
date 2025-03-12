import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import math
from abc import ABC, abstractmethod

# ---------------------- Strategy Pattern ----------------------
class NumericalMethod(ABC):
    @abstractmethod
    def calculate(self, points, x_value=None, degree=None):
        pass
    
    @abstractmethod
    def get_result_text(self):
        pass

class NewtonInterpolation(NumericalMethod):
    def calculate(self, points, x_value=None, degree=None):
        n = len(points)
        Y = self.divided_diff_table(points, n)
        result = self.newton_interpolation(Y, x_value, points, n)
        self.result = result
        self.x_value = x_value
        return result
    
    def divided_diff_table(self, points, n):
        Y = np.zeros((n, n))
        for i in range(n):
            Y[i][0] = points[i][1]
        for i in range(1, n):
            for j in range(n - i):
                Y[j][i] = (Y[j + 1][i - 1] - Y[j][i - 1]) / (points[j + i][0] - points[j][0])
        return Y
    
    def newton_interpolation(self, Y, x, points, n):
        result = Y[0][0]
        product_term = 1.0
        for i in range(1, n):
            product_term *= (x - points[i - 1][0])
            result += product_term * Y[0][i]
        return result
    
    def get_result_text(self):
        return f'f({self.x_value}) = {self.result:.4f}'

class NewtonGregoryInterpolation(NumericalMethod):
    def calculate(self, points, x_value=None, degree=None):
        n = len(points)
        h = round(points[1][0] - points[0][0], 5)
        for i in range(1, n):
            if round(points[i][0] - points[i - 1][0], 5) != h:
                raise ValueError("Os pontos não estão igualmente espaçados para a Interpolação de Newton-Gregory.")
        
        Y = self.gregory_diff_table(points, n)
        result = self.newton_gregory_interpolation(Y, x_value, points, n, h)
        self.result = result
        self.x_value = x_value
        return result
    
    def gregory_diff_table(self, points, n):
        Y = np.zeros((n, n))
        for i in range(n):
            Y[i][0] = points[i][1]
        for i in range(1, n):
            for j in range(n - i):
                Y[j][i] = Y[j + 1][i - 1] - Y[j][i - 1]
        return Y
    
    def newton_gregory_interpolation(self, Y, x, points, n, h):
        s = (x - points[0][0]) / h
        result = Y[0][0]
        product_term = 1.0
        for i in range(1, n):
            product_term *= (s - (i - 1))
            result += (product_term * Y[0][i]) / math.factorial(i)
        return result
    
    def get_result_text(self):
        return f'f({self.x_value}) = {self.result:.4f}'

class LinearFit(NumericalMethod):
    def calculate(self, points, x_value=None, degree=None):
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        y_pred = m * x + c
        r_squared = self.calculate_r_squared(y, y_pred)
        
        self.m = m
        self.c = c
        self.r_squared = r_squared
        return m, c, r_squared
    
    def calculate_r_squared(self, y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared
    
    def get_result_text(self):
        return f'y = {self.c:.4f} + {self.m:.4f}x', f'R² = {self.r_squared:.4f}'

class PolynomialFit(NumericalMethod):
    def calculate(self, points, x_value=None, degree=None):
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        
        coefficients = np.polyfit(x, y, degree)
        polynomial = self.format_polynomial(coefficients)
        y_pred = np.polyval(coefficients, x)
        r_squared = self.calculate_r_squared(y, y_pred)
        
        self.polynomial = polynomial
        self.r_squared = r_squared
        return polynomial, r_squared
    
    def format_polynomial(self, coefficients):
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
    
    def calculate_r_squared(self, y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared
    
    def get_result_text(self):
        return f'polinomio: {self.polynomial}', f'R² = {self.r_squared:.4f}'

class ExponentialFit(NumericalMethod):
    def calculate(self, points, x_value=None, degree=None):
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        
        log_y = np.log(y)
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, log_y, rcond=None)[0]
        a = math.exp(c)
        b = math.exp(m)
        
        y_pred = a * np.power(b, x)
        r_squared = self.calculate_r_squared(y, y_pred)
        
        self.a = a
        self.b = b
        self.r_squared = r_squared
        return a, b, r_squared
    
    def calculate_r_squared(self, y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared
    
    def get_result_text(self):
        return f'y = {self.a:.4f} * {self.b:.4f}^x', f'R² = {self.r_squared:.4f}'

# ----------------------  Factory Pattern para os métodos ----------------------
class MethodFactory:
    @staticmethod
    def get_method(method_name):
        methods = {
            'newton': NewtonInterpolation(),
            'newton_gregory': NewtonGregoryInterpolation(),
            'linear': LinearFit(),
            'polynomial': PolynomialFit(),
            'exponential': ExponentialFit()
        }
        return methods.get(method_name)

# ---------------------- Composite Pattern para as views ----------------------
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
        # Estilo da tela principal
        self.frame.configure(padding="20 20 20 20")
        
        # Título da aplicação
        ttk.Label(
            self.frame, 
            text="Calculadora de Métodos Numéricos", 
            font=('Segoe UI', 14, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 20))
        
        # Definição dos métodos disponíveis
        methods = [
            ("Polinômio Interpolador de Newton", 'newton'),
            ("Polinômio Interpolador de Newton-Gregory", 'newton_gregory'),
            ("Ajuste Linear (y=a₀+a₁x)", 'linear'),
            ("Ajuste Polinomial", 'polynomial'),
            ("Ajuste Exponencial (y=ab^x)", 'exponential')
        ]
        
        # Criação dos botões para cada método
        for text, method_name in methods:
            btn = ttk.Button(
                self.frame, 
                text=text,
                command=lambda m=method_name: self.controller.show_method_config(m)
            )
            btn.pack(fill='x', pady=5)

class MethodConfigView(View):
    def __init__(self, parent, controller, method_name):
        super().__init__(parent, controller)
        self.method_name = method_name
        self.titles = {
            'newton': 'Polinômio Interpolador de Newton',
            'newton_gregory': 'Polinômio Interpolador de Newton-Gregory',
            'linear': 'Ajuste Linear (y=a₀+a₁x)',
            'polynomial': 'Ajuste Polinomial',
            'exponential': 'Ajuste Exponencial (y=ab^x)'
        }
    
    def setup(self):
        self.frame.configure(padding="20 20 20 20")
        
        # Título do método
        ttk.Label(
            self.frame, 
            text=self.titles[self.method_name],
            font=('Segoe UI', 12, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 20))
        
        # Botão de voltar
        back_btn = ttk.Button(
            self.frame,
            text="◄ Voltar",
            command=self.controller.show_main_menu,
            style='Link.TButton'
        )
        back_btn.pack(anchor='w', pady=(0, 15))
        
        # Configs específicas do método
        config_frame = ttk.Frame(self.frame)
        config_frame.pack(fill='x')
        
        ttk.Label(config_frame, text="Número de pontos:", background='#f5f5f5').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.num_points_entry = ttk.Entry(config_frame, width=10)
        self.num_points_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Campo para o grau do polinômio (exibe apenas para o ajuste polinomial)
        self.degree_label = ttk.Label(config_frame, text="Grau do polinômio:", background='#f5f5f5')
        self.degree_entry = ttk.Entry(config_frame, width=10)
        
        if self.method_name == 'polynomial':
            self.degree_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
            self.degree_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Botão de avançar para entrada de pontos
        ttk.Button(
            config_frame, 
            text="Continuar",
            command=self.validate_and_continue
        ).grid(row=2, column=0, columnspan=2, pady=15)
    
    def validate_and_continue(self):
        try:
            num_points = int(self.num_points_entry.get())
            if num_points < 1 or num_points > 100:
                raise ValueError("Número de pontos deve estar entre 1 e 100")
            
            degree = None
            if self.method_name == 'polynomial':
                degree = int(self.degree_entry.get())
                if degree < 1:
                    raise ValueError("O grau do polinômio deve ser maior que zero")
            
            self.controller.show_points_input(self.method_name, num_points, degree)
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

class PointsInputView(View):
    def __init__(self, parent, controller, method_name, num_points, degree=None):
        super().__init__(parent, controller)
        self.method_name = method_name
        self.num_points = num_points
        self.degree = degree
        self.point_entries = []
        self.titles = {
            'newton': 'Polinômio Interpolador de Newton',
            'newton_gregory': 'Polinômio Interpolador de Newton-Gregory',
            'linear': 'Ajuste Linear (y=a₀+a₁x)',
            'polynomial': 'Ajuste Polinomial',
            'exponential': 'Ajuste Exponencial (y=ab^x)'
        }
    
    def setup(self):
        self.frame.configure(padding="20 20 20 20")
        
        # Título do método
        ttk.Label(
            self.frame, 
            text=self.titles[self.method_name],
            font=('Segoe UI', 12, 'bold'),
            background='#f5f5f5'
        ).pack(pady=(0, 10))
        
        # Botão de voltar
        back_btn = ttk.Button(
            self.frame,
            text="◄ Voltar",
            command=lambda: self.controller.show_method_config(self.method_name),
            style='Link.TButton'
        )
        back_btn.pack(anchor='w', pady=(0, 10))
        
        # Frame para os pontos com scrollbar se for necessário
        points_container = ttk.Frame(self.frame)
        points_container.pack(fill='both', expand=True, pady=5)
        
        if self.num_points > 8:  # Usa scrollbar para o caso de muitos pontos
            canvas = tk.Canvas(points_container, bg='#f5f5f5', highlightthickness=0)
            scrollbar = ttk.Scrollbar(points_container, orient="vertical", command=canvas.yview)
            self.points_frame = ttk.Frame(canvas)
            
            self.points_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=self.points_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Bind para o scroll do mouse
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        else:
            self.points_frame = points_container
        
        # Cabeçalhos para x e y
        ttk.Label(self.points_frame, text="x", width=10, background='#f5f5f5', font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(self.points_frame, text="y", width=10, background='#f5f5f5', font=('Segoe UI', 10, 'bold')).grid(row=0, column=3, padx=5, pady=2)
        
        # Cria campos para entrada dos pontos
        for i in range(self.num_points):
            ttk.Label(self.points_frame, text=f"Ponto {i+1}:", background='#f5f5f5').grid(row=i+1, column=0, padx=5, pady=2, sticky='e')
            x_entry = ttk.Entry(self.points_frame, width=10)
            x_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            ttk.Label(self.points_frame, text="→", background='#f5f5f5').grid(row=i+1, column=2, padx=2, pady=2)
            
            y_entry = ttk.Entry(self.points_frame, width=10)
            y_entry.grid(row=i+1, column=3, padx=5, pady=2)
            
            self.point_entries.append((x_entry, y_entry))
        
        # Frame para o cálculo
        calc_frame = ttk.Frame(self.frame)
        calc_frame.pack(fill='x', pady=10)
        
        # Campo para x (somente para métodos de interpolação)
        self.x_entry = None
        if self.method_name in ['newton', 'newton_gregory']:
            ttk.Label(calc_frame, text="Valor de x:", background='#f5f5f5').pack(side='left', padx=5)
            self.x_entry = ttk.Entry(calc_frame, width=10)
            self.x_entry.pack(side='left', padx=5)
        
        # Botão do cálculo
        ttk.Button(
            calc_frame, 
            text="Calcular",
            command=self.calculate
        ).pack(side='left', padx=5)
        
        # Frame para exibir resultados
        result_frame = ttk.Frame(self.frame, padding=10)
        result_frame.pack(fill='x', pady=5)
        
        self.result_label = ttk.Label(
            result_frame, 
            font=('Segoe UI', 10, 'bold'),
            background='#f0f0f0',
            padding=10
        )
        self.result_label.pack(fill='x', pady=2, ipady=5)
        
        self.r_squared_label = ttk.Label(
            result_frame, 
            font=('Segoe UI', 10),
            background='#f0f0f0',
            padding=5
        )
        if self.method_name in ['linear', 'polynomial', 'exponential']:
            self.r_squared_label.pack(fill='x', pady=2, ipady=3)
    
    def calculate(self):
        try:
            # Obtem pontos
            points = []
            for entry_pair in self.point_entries:
                try:
                    x = float(entry_pair[0].get())
                    y = float(entry_pair[1].get())
                    points.append((x, y))
                except ValueError:
                    raise ValueError("Por favor, insira apenas valores numéricos válidos.")
            
            # Verifica valor de x se for necessário
            x_value = None
            if self.x_entry and self.method_name in ['newton', 'newton_gregory']:
                if not self.x_entry.get():
                    raise ValueError("Por favor, insira o valor de x.")
                x_value = float(self.x_entry.get())
            
            # Calcula usando o método correspondente
            method = MethodFactory.get_method(self.method_name)
            method.calculate(points, x_value, self.degree)
            
            # Mostra o resultados
            result_text = method.get_result_text()
            if isinstance(result_text, tuple):
                self.result_label.config(text=result_text[0])
                self.r_squared_label.config(text=result_text[1])
            else:
                self.result_label.config(text=result_text)
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# ---------------------- Controlador Principal ----------------------
class NumericalMethodsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x520')
        self.minsize(480, 520)
        self.resizable(0, 0)
        self.title('Calculadora de Métodos Numéricos')
        self.configure(bg='#f5f5f5')
        
        # Configuração de estilos
        self.setup_styles()
        
        # Container principal para as views
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)
        
        # Inicializa as views
        self.views = {}
        self.current_view = None
        
        # Inicializa com o menu principal
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
        
        # Mostra menu principal inicialmente
        self.show_view('main_menu')
    
    def show_view(self, view_name):
        # Esconde a view atual se ela existir
        if self.current_view:
            self.current_view.hide()
        
        # Exibe a nova view
        self.current_view = self.views[view_name]
        self.current_view.show()
    
    def show_main_menu(self):
        self.show_view('main_menu')
    
    def show_method_config(self, method_name):
        # Cria a view de config se não existir
        view_name = f'config_{method_name}'
        if view_name not in self.views:
            config_view = MethodConfigView(self.container, self, method_name)
            config_view.setup()
            self.views[view_name] = config_view
        
        self.show_view(view_name)
    
    def show_points_input(self, method_name, num_points, degree=None):
        # Cria uma nova view para entrada de pontos
        view_name = f'points_{method_name}_{num_points}'
        if degree:
            view_name += f'_{degree}'
        
        points_view = PointsInputView(self.container, self, method_name, num_points, degree)
        points_view.setup()
        self.views[view_name] = points_view
        
        self.show_view(view_name)

if __name__ == "__main__":
    app = NumericalMethodsCalculator()
    app.mainloop()