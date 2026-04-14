from models import ActionType, OrderType


def run_cli(exchange):
    while True:
        cmd = input("Action: ").strip()

        if cmd.upper() == "QUIT":
            break

        parts = cmd.split()

        if not parts:
            continue

        try:
            command = parts[0].upper()

            if command in ["BUY", "SELL"]:
                action_type = ActionType(command)
                name = parts[1]
                order_type = OrderType(parts[2].upper())

                if order_type == OrderType.LMT:
                    price = float(parts[3])
                    quantity = int(parts[4])
                else:
                    price = None
                    quantity = int(parts[3])

                order = exchange.place_order(
                    name=name,
                    action_type=action_type,
                    order_type=order_type,
                    price=price,
                    quantity=quantity,
                )

                print(order)

            elif command == "VIEW":
                exchange.view_orders()

            elif command == "TRADES":
                exchange.view_trades()

            elif command == "QUOTE":
                exchange.quote(parts[1])

            else:
                print("Unknown command")

        except Exception as e:
            print("Error:", e)