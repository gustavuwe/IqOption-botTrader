from iqoptionapi.stable_api import IQ_Option
import sys, time

API = IQ_Option('email', 'senha')
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect() == False:
    print('Erro ao se conectar')
    API.reconnect()
else:
    print('Conectado com sucesso')

    time.sleep(1)

porcentagem_lucro = 10
entrada = 10.0
par = 'EURUSD-OTC'
timeframe = 1
valor_minimo = round(float(entrada) * (float(porcentagem_lucro / 100)), 2)


API.subscribe_strike_list(par, timeframe)

status,id = API.buy_digital_spot(par, entrada, 'put', timeframe)
time.sleep(2)

while API.get_async_order(id)['position-changed']['msg']['status'] == 'open':
	vpv = round(API.get_digital_spot_profit_after_sale(id), 2)
	
	print('Atual: $' + str(vpv) + ' - Minimo para venda: $' + str(valor_minimo))
	
	if vpv > valor_minimo:
		print('Fechando operação')
		API.close_digital_option(id)
		break
	
	time.sleep(0.3)
	
status,valor = API.check_win_digital_v2(id)
print('Resultado da operação: ' + ('WIN - ' if valor > 0 else 'LOSS - ') + str(round(valor, 2)))
