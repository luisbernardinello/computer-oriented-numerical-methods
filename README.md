# Computational Numerical Methods

![Unesp](https://img.shields.io/badge/BCC-UNESP-Bauru.svg)
![License](https://img.shields.io/badge/Code%20License-MIT-blue.svg)

## 📑 Overview

This project implements a numerical methods calculator with a graphical interface using Python and Tkinter. Developed as part of the Computational Numerical Methods course at UNESP Bauru, this implementation demonstrates fundamental concepts of numerical analysis and algorithms applied to solving mathematical problems.

## 🏗️ Project Components

### 1. Linear Systems Solvers

The following methods for solving linear systems have been implemented:

- **Gauss-Jordan Method**

  - Implements Gaussian elimination with complete pivoting
  - Transforms the augmented matrix into reduced row echelon form
  - Obtains direct solution of the system

- **LU Decomposition**

  - Decomposes the coefficient matrix into triangular matrices L and U
  - Solves systems Ly = b and Ux = y sequentially
  - Allows efficient solving of multiple systems with the same coefficient matrix

- **Compact Gauss Method**

  - Optimized version of Gaussian elimination
  - Saves memory by using a single matrix during the process
  - Implements partial pivoting strategy

- **Cholesky Method**

  - Applicable to symmetric positive definite matrices
  - Decomposes matrix A in the form A = LL^T
  - Offers computational advantages for certain types of problems

- **Matrix Inversion**

  - Calculates the inverse matrix using Gaussian elimination
  - Solves n linear systems for each column of the identity matrix

- **Iterative Methods**

  - **Jacobi-Richardson**

    - Uses values from the previous iteration for all unknowns
    - Implements stopping criterion based on tolerance

  - **Gauss-Seidel**
    - Uses updated values for unknowns already calculated in the iteration
    - Generally converges faster than Jacobi-Richardson

### 2. Curve Fitting

- **Least Squares Fitting**
  - Implements linear and polynomial regression
  - Minimizes the sum of squared residuals
  - Calculates optimal coefficients and fit quality statistics

## 📚 References

- Arenales, S., & Darezzo, A. (2008). _Cálculo Numérico: aprendizagem com Apoio de Software_.
- Chapra, S. C., & Canale, R. P. (2008). _Métodos Numéricos para Engenharia_.
- Burden, R. L., & Faires, J. D. (2010). _Numerical Analysis_ (9th ed.). Brooks/Cole.
- Heath, M. T. (2018). _Scientific Computing: An Introductory Survey_ (3rd ed.). SIAM.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<h4 align="center">
<img src="https://socialify.git.ci/luisbernardinello/computer-oriented-numerical-methods/image?font=Raleway&language=1&name=1&owner=1&pattern=Overlapping%20Hexagons&theme=Auto" alt="Computational Numerical Methods" width="498" height="270" />
</h4>
