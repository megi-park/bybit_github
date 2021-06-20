import bybit
import mkdntjr12_bybit1
import balance as bl

def order(signal,size):
    client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key)
    #아래 구문이 실행만 되면 무조건 실행 됨. 현재 side 는 buy 에 있으며, symbol 은 BTCUSD 를 거래하겠다는 뜻, order type 은 시장가, 지정가 주문 유무 이며, market 이 시장가라는 뜻
    #qty 는 계약 단위이며, 현재 BTCUSD의 경우에는 달러가 계약 단위가 되기 때문에 1달러씩 계약 됨. 추후에는 내가 가진 자기자본 100% 로 설정이 필요할 듯
    # time in force 는 언제 청산 할 것이냐 라는 뜻 good till cancel 은 내가 청산하겠다고 할 때까지 계속 되는 것
    order = client.Order.Order_new(side=signal,symbol="BTCUSD",order_type="Market",qty=size,time_in_force="GoodTillCancel").result() #qty 를 나중에는 자기자본율을 받아야함
    side = order[0]["result"]["side"]
    order_type = order[0]["result"]["order_type"]
    qt = order[0]["result"]["qty"]
    status = order[0]["result"]["order_status"]
    time = order[0]["result"]["created_at"]
    print("공매수/공매도 : {0} , 시장가/지정가 : {1} , 수량 : {2} , 체결 유무 : {3} , 체결 시간 : {4}".format(side, order_type, qt, status, time))
    return side, order_type, qt, status, time

# print(client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="1").result()) #leverage 설정 함수 BTCUSD 에서 레버리지를 몇으로 설정할 것이냐

# print(client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=myposi_size,time_in_force="GoodTillCancel").result()) # qty 에 내 포지션 규모를 입력함으로써 자동 청산되도록 설정이 가능해졌음
# client.Order.Order_cancelAll(symbol="BTCUSD").result() #주문 취소 - 시장가 청산이 아님

# order("Buy",1)

