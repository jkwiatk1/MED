


from fpgrowth.fpgrowth_hierarchical import prepare, fpgrowth


def generate_plot_min_conf(transactions):
    minConf_values = [0.1, 0.2, 0.3, 0.5, 0.6]

    num_rules = []

    for minConf in minConf_values:
        freq_items_more1, rules = fpgrowth(transactions, 10, minConf)
        num_rules.append(len(rules))

    # Generowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(minConf_values, num_rules, marker='o')
    plt.xlabel('minConf')
    plt.ylabel('Number of Association Rules')
    plt.title('Number of Association Rules for Different minConf')
    plt.show()

import matplotlib.pyplot as plt

def generate_plot_min_sup(transactions):
    minSup_values = [5, 10, 25, 30]

    num_rules = []

    for minSup in minSup_values:
        freq_items_more1, rules = fpgrowth(transactions, minSup, 0.2)
        num_rules.append(len(rules))

    # Generowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(minSup_values, num_rules, marker='o')
    plt.xlabel('minSup')
    plt.ylabel('Number of Association Rules')
    plt.title('Number of Association Rules for Different minSup')
    plt.show()



# Wywołanie funkcji generującej wykresy
# generate_plot_min_sup(transactions_list)
# generate_plot_min_conf(transactions_list)



#generate_plots(transactions_list)

import matplotlib.pyplot as plt
import time

# Funkcja generująca wykres czasu wykonania
def generate_time_plot():
    # Różne długości parametru transactions
    minConf = 0.5
    minSup = 10
    transaction_lengths = [200,300, 500]
    execution_times = []  # Lista czasów wykonania
    transactions = generate_transactions()
    for t in transactions:
         # Wygenerowanie transakcji o danej długości

        print("Trans len", len(t))
        start_time = time.time()
        freq_items_more1, rules = fpgrowth(t, minSup, minConf)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_times.append(execution_time)

    # Generowanie wykresu czasu wykonania
    plt.plot(transaction_lengths, execution_times, marker='o')
    plt.xlabel('Transaction Length')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Transaction Length')
    plt.show()

# Funkcja generująca transakcje o zadanej długości
def generate_transactions():

    t200, _ = prepare('../dataset/t_200.csv')
    t300, _ = prepare('../dataset/t_300.csv')
    t500, _ = prepare('../dataset/t_500.csv')
    t1000, _ = prepare('../dataset/t_1000.csv')


    transactions = [t200, t300,  t500]

    return transactions

# Wywołanie funkcji generującej wykres czasu wykonania
# generate_time_plot()