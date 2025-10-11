import numpy as np
import time
import concurrent.futures

rng = np.random.default_rng()
M = 10000
N = 4


def boolean_oracle(x):
    """
    call the Boolean oracle and return the value f(x)
    """
    res = []
    for row in x:
        x1 = bool(row[0])
        x2 = bool(row[1])
        x3 = bool(row[2])

        # --- CNF ---
        # clause 1: (x1 OR NOT x2)
        clause1 = x1 or not x2

        # clause 2: (x2 OR x3)
        clause2 = x2 or x3

        result = clause1 and clause2
        # --------------------

        res.append(int(result))
    return np.array(res).reshape(len(x), 1)

# def boolean_oracle(x):
#     """
#     test
#     """
#     t = x[:, 0].reshape(-1, 1)
#     return t
#     # return f(x)

def hardcode_samples_i(i):
    # return 32 (for len(Z) = 0,1,...,31): Y, f(Y), Y_Z, f(Y'_Z)
    print("data generated now ...")

    Z = np.random.randint(0, 2, size=(M, N - i))
    Y = np.random.randint(0, 2, size=(M, i))
    Ydot = np.random.randint(0, 2, size=(M, i))

    Y_Z = np.concatenate((Y, Z), axis=1)
    Ydot_Z = np.concatenate((Ydot, Z), axis=1)

    f_y_z = (-1) ** boolean_oracle(Y_Z)
    f_ydot_z = (-1) ** boolean_oracle(Ydot_Z)

    print(str(i) + "-th loop datageneration completed!")
    return Y, Ydot, f_y_z, f_ydot_z


def sample_inputs(n, m):
    """
    random sample generation
    """
    return np.random.randint(0, 2, size=(m, n))


def fyz_times_chi(y, z, S, X):
    res = 1
    for s in S:
        res *= X[s]
    return res


def sub_estimator(S, J, Y, Ydot, f_y_z, f_ydot_z):
    start_time = time.time()
    N = 32

    # calculate the chi_y, chi_y_dot
    chi_y = (-1) ** (np.sum(Y[:, S], axis=1, keepdims=True))
    chi_y_dot = (-1) ** (np.sum(Ydot[:, S], axis=1, keepdims=True))

    # calculate res
    res = f_y_z * f_ydot_z
    res *= chi_y
    res *= chi_y_dot

    # cal size of res == 1
    x = np.sum(res == 1)

    # get the final results
    e = (2 * x - M) / (M)

    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"exc-time: {execution_time} s")

    return e


def Goldreich_Levin(tau, N=4):
    backup_path = f"./backup.txt"
    current_B = [([], 0)]
    next_B = []

    def process_B(B):
        """Processes a single B and returns valid splits."""
        valid_Bs = []
        B1 = (B[0], B[1] + 1)
        B2 = (B[0] + [B[1]], B[1] + 1)

        weight_1 = sub_estimator(B[0], B[1] + 1, Y_ls, Ydot_ls, f_y_z_ls, f_ydot_z_ls)
        weight_2 = sub_estimator(B[0] + [B[1]], B[1] + 1, Y_ls, Ydot_ls, f_y_z_ls, f_ydot_z_ls)

        print("current B:" + str(B))
        if weight_1 > tau ** 2 / 2.0:
            valid_Bs.append(B1)
            print("B1 is appending..." + str(B1) + " estimator: " + str(weight_1))
        else:
            print("B1 is discard!" + str(B1) + " estimator: " + str(weight_1))
        if weight_2 > tau ** 2 / 2.0:
            valid_Bs.append(B2)
            print("B2 is appending..." + str(B2) + " estimator: " + str(weight_2))
        else:
            print("B2 is discard!" + str(B2) + " estimator: " + str(weight_2))
        return valid_Bs

    for i in range(N):
        # public data
        Y_ls, Ydot_ls, f_y_z_ls, f_ydot_z_ls = hardcode_samples_i(i + 1)

        # Parallel processing of current_B
        next_B = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_B, B): B for B in current_B}
            for future in concurrent.futures.as_completed(futures):
                next_B.extend(future.result())

        current_B = next_B[:]
        next_B = []

        with open(backup_path, "w") as file:
            file.write(",".join(map(str, current_B)))
        print("current B numbers: " + str(len(current_B)))
    return current_B


# precompute the data, used in recovery the coeff
_data_used_for_get_fourier_coeff = np.random.randint(0, 2, size=(1000000, 64))
_f_get_coeff = (-1) ** boolean_oracle(_data_used_for_get_fourier_coeff)


def get_Fourier_coeff(S_list):
    res = []
    for s in S_list:
        chi_x = (-1) ** (np.sum(_data_used_for_get_fourier_coeff[:, s[0]], axis=1, keepdims=True))
        t = _f_get_coeff * chi_x

        one = np.sum(t == 1)
        e = (2 * one - 1000000) / (1000000 * 1.0)
        res.append(e)

    return res


def reconstruct_bf(S_list, coeff_list, tau):
    print()
    print("-"*20 + "The reconstructed expression (^ stands for XOR)" + "-"*20)
    L = []
    C = []
    polynomial_terms = []

    for i in range(len(coeff_list)):
        if abs(coeff_list[i]) > tau/2.0:
            C.append(coeff_list[i])
            L.append(S_list[i][0])

    for i, term_indices in enumerate(L):
        coefficient = C[i]

        if not L[i]:
            term_variable_part = ""
        elif len(term_indices) == 1:
            term_variable_part = f"x{term_indices[0]}"
        else:
            term_variable_part = " ^ ".join([f"x{j}" for j in sorted(term_indices)])
            term_variable_part = f"({term_variable_part})"

        if term_variable_part:
            if coefficient == 1.0:
                term_str = term_variable_part
            elif coefficient == -1.0:
                term_str = f"-{term_variable_part}"
            else:
                term_str = f"{coefficient} * {term_variable_part}"
        else:
            term_str = str(coefficient)
        polynomial_terms.append(term_str)

    result = polynomial_terms[0]
    for term in polynomial_terms[1:]:
        if term.startswith('-'):
            result += f" - {term[1:]}"
        else:
            result += f" + {term}"
    print(result)


tau = 0.1
B = Goldreich_Levin(tau)
print("done")
print(B)
coefflist = get_Fourier_coeff(B)
print(coefflist)
reconstruct_bf(B, coefflist, tau)
