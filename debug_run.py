import unittest.mock as mock
import main
import sys

# Simulando as entradas do usuário:
# 1. senha_instalação (pedido no escopo global de fazerLogin.py)
# 2. pin_instalacao (pedido em main.main())
# 3. dia_inicio (pedido em main.obter_intervalo_dias())
# 4. dia_fim (pedido em main.obter_intervalo_dias())
mock_inputs = iter(["SENHA_TESTE", "PIN_TESTE", "1", "31"])

with mock.patch('builtins.input', lambda _: next(mock_inputs)):
    try:
        print("Iniciando a execução do main()...")
        main.main()
    except Exception as e:
        import traceback
        print("\n--- ERRO DETECTADO ---")
        traceback.print_exc()
        sys.exit(1)
