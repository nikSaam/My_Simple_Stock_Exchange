def run_cli(exchange):
    while True:
        cmd = input("Action: ")

        if cmd == "QUIT":
            break

        parts = cmd.split()

        try:
            if parts[0] in ["BUY", "SELL"]:
                side = parts[0]
                symbol = parts[1]
                order_type = parts[2]

                if order_type == "LMT":
                    price = float(parts[3].replace("$", ""))
                    qty = int(parts[4])
                else:
                    price = None
                    qty = int(parts[3])

                order = exchange.place_order(symbol, side, order_type, price, qty)

                print(f"You placed: {order}")

            elif parts[0] == "VIEW":
                exchange.view_orders()

            elif parts[0] == "QUOTE":
                exchange.quote(parts[1])

        except Exception as e:
            print("Error:", e)
