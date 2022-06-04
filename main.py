import numpy as np
import skfuzzy as fuzzy
import skfuzzy.control as control
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPress ENTER to continue...")


if __name__ == "__main__":
    clear_console()

    # Definindo Universo de Discurso e Nome da Variável
    universo_m = np.arange(0, 2.41, 0.01)
    massa = control.Antecedent(universe=universo_m, label="massa")

    # Criando Função de Pertinência (Triangular -> trimf; Trapezoidal -> trapmf)
    massa["mp"] = fuzzy.trimf(massa.universe, [0, 0, 0.6])
    massa["pe"] = fuzzy.trimf(massa.universe, [0, 0.6, 1.2])
    massa["me"] = fuzzy.trimf(massa.universe, [0.6, 1.2, 1.8])
    massa["gr"] = fuzzy.trimf(massa.universe, [1.2, 1.8, 2.4])
    massa["mg"] = fuzzy.trimf(massa.universe, [1.8, 2.4, 2.4])
    massa.view()

    # Definindo Universo de Discurso e Nome da Variável
    universo_v = np.arange(0, 181, 1)
    velocidade = control.Antecedent(universe=universo_v, label="velocidade")

    # Criando Função de Pertinência (Triangular -> trimf; Trapezoidal -> trapmf)
    velocidade["mb"] = fuzzy.trimf(velocidade.universe, [0, 0, 45])
    velocidade["ba"] = fuzzy.trimf(velocidade.universe, [0, 45, 90])
    velocidade["me"] = fuzzy.trimf(velocidade.universe, [45, 90, 135])
    velocidade["al"] = fuzzy.trimf(velocidade.universe, [90, 135, 180])
    velocidade["ma"] = fuzzy.trimf(velocidade.universe, [135, 180, 180])
    velocidade.view()

    # Universo da Pressão
    universo_p = np.arange(0, 1.1, 0.1)
    pressao = control.Consequent(universe=universo_p, label="pressao")

    # Criando Função de Pertinência (Triangular -> trimf; Trapezoidal -> trapmf)
    pressao["mi"] = fuzzy.trimf(pressao.universe, [0, 0, 0.5])
    pressao["me"] = fuzzy.trimf(pressao.universe, [0, 0.5, 1.0])
    pressao["el"] = fuzzy.trimf(pressao.universe, [0.5, 1.0, 1.0])
    pressao.view()

    # REGRA -> Expressão X, Resultado Y
    # Coluna 1
    regra1 = control.Rule((velocidade["mb"] & massa["mp"]) |
                          (velocidade["mb"] & massa["pe"]) |
                          (velocidade["mb"] & massa["me"]),
                          pressao["mi"])
    regra2 = control.Rule((velocidade["mb"] & massa["gr"]) |
                          (velocidade["mb"] & massa["mg"]),
                          pressao["me"])
    # Coluna 2
    regra3 = control.Rule((velocidade["ba"] & massa["mp"]) |
                          (velocidade["ba"] & massa["pe"]) |
                          (velocidade["ba"] & massa["me"]),
                          pressao["mi"])
    regra4 = control.Rule((velocidade["ba"] & massa["gr"]) |
                          (velocidade["ba"] & massa["mg"]),
                          pressao["me"])
    # Coluna 3
    regra5 = control.Rule((velocidade["me"] & massa["mp"]) |
                          (velocidade["me"] & massa["pe"]),
                          pressao["mi"])
    regra6 = control.Rule((velocidade["me"] & massa["me"]),
                          pressao["me"])
    regra7 = control.Rule((velocidade["me"] & massa["gr"]) |
                          (velocidade["me"] & massa["mg"]),
                          pressao["el"])
    # Coluna 4
    regra8 = control.Rule((velocidade["al"] & massa["mp"]) |
                          (velocidade["al"] & massa["pe"]) |
                          (velocidade["al"] & massa["me"]),
                          pressao["me"])
    regra9 = control.Rule((velocidade["al"] & massa["gr"]) |
                          (velocidade["al"] & massa["mg"]),
                          pressao["el"])
    # Coluna 5
    regra10 = control.Rule((velocidade["ma"] & massa["mp"]) |
                           (velocidade["ma"] & massa["pe"]) |
                           (velocidade["ma"] & massa["me"]),
                           pressao["me"])
    regra11 = control.Rule((velocidade["ma"] & massa["gr"]) |
                           (velocidade["ma"] & massa["mg"]),
                           pressao["el"])

    # Adicionando Regras ao Controle
    pressao_controle = control.ControlSystem([regra1, regra2,
                                              regra3, regra4,
                                              regra5, regra6, regra7,
                                              regra8, regra9,
                                              regra10, regra11])

    # Criando Sistema c/ o Controle de PressÃo
    sistema = control.ControlSystemSimulation(pressao_controle)

    # Valores de Entrada
    sistema.input["massa"] = 1.5
    sistema.input["velocidade"] = 155

    # Executando o Sistema
    sistema.compute()
    pressao.view(sim=sistema)
    print(f"Resultado 'desfuzzificado': {sistema.output['pressao']}")

    pause()
    print("Fim do Programa!\n")
