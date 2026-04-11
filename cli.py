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
                if len(parts) < 4:
                    raise ValueError("Not enough arguments")

                action_type = ActionType(command)
                name = parts[1]
                order_type = OrderType(parts[2].upper())

                if order_type == OrderType.LMT:
                    if len(parts) < 5:
                        raise ValueError("LMT requires price and quantity")

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

            elif command == "QUOTE":
                if len(parts) != 2:
                    raise ValueError("Usage: QUOTE <SYMBOL>")
                exchange.quote(parts[1])

            else:
                print("Unknown command")

        except ValueError as e:
            print("Error:", e)

        except Exception as e:
            print("Unexpected error:", e)