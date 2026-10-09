import re
from collections import OrderedDict
from dataclasses import dataclass
from typing import List, Optional

PHONE_PATTERN = re.compile(r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$')
PRIORITY_ORDER = {'MAX': 0, 'MIDDLE': 1, 'LOW': 2}


@dataclass
class Order:
    number: str
    products_raw: str
    customer: str
    address_raw: str
    phone_raw: str
    priority: str
    address_parts: Optional[List[str]] = None
    address_error: Optional[str] = None
    phone_error: Optional[str] = None
    aggregated_products: str = ""

    def aggregate_products(self):
        items = [p.strip() for p in self.products_raw.split(',') if p.strip()]
        counts = OrderedDict()
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        parts = []
        for item, cnt in counts.items():
            parts.append(f"{item} x{cnt}" if cnt > 1 else item)
        self.aggregated_products = ", ".join(parts)

    def validate(self):
        if not self.address_raw or not self.address_raw.strip():
            self.address_error = "no data"
            self.address_parts = None
        else:
            parts = [p.strip() for p in self.address_raw.split('.')]
            if len(parts) != 4:
                self.address_error = self.address_raw
                self.address_parts = None
            else:
                self.address_parts = parts
                self.address_error = None

        if not self.phone_raw or not self.phone_raw.strip():
            self.phone_error = "no data"
        else:
            phone = self.phone_raw.strip()
            if not PHONE_PATTERN.match(phone):
                self.phone_error = phone
            else:
                self.phone_error = None

        self.aggregate_products()

    def is_valid(self) -> bool:
        return self.address_error is None and self.phone_error is None


class OrderProcessor:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.orders: List[Order] = []

    def read_orders(self):
        with open(self.input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(';')
                if len(parts) != 6:
                    continue
                order = Order(
                    number=parts[0].strip(),
                    products_raw=parts[1].strip(),
                    customer=parts[2].strip(),
                    address_raw=parts[3].strip(),
                    phone_raw=parts[4].strip(),
                    priority=parts[5].strip()
                )
                order.validate()
                self.orders.append(order)

    def write_valid_orders(self, output_path: str):
        valid = [o for o in self.orders if o.is_valid()]

        def sort_key(o: Order):
            country = o.address_parts[0] if o.address_parts else ""
            is_russia = country in ("Россия", "Российская Федерация")
            country_key = (0, "") if is_russia else (1, country)
            priority_key = PRIORITY_ORDER.get(o.priority, 99)
            return (country_key, priority_key, o.number)

        valid.sort(key=sort_key)

        with open(output_path, 'w', encoding='utf-8') as f:
            for o in valid:
                addr_out = ". ".join(o.address_parts[1:]) if o.address_parts else ""
                f.write(
                    f"{o.number};{o.aggregated_products};{o.customer};"
                    f"{addr_out};{o.phone_raw.strip()};{o.priority}\n"
                )

    def write_invalid_orders(self, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            for o in self.orders:
                if o.phone_error is not None:
                    f.write(f"{o.number};2;{o.phone_error}\n")
                if o.address_error is not None:
                    f.write(f"{o.number};1;{o.address_error}\n")

    def process(self, valid_output: str, invalid_output: str):
        self.read_orders()
        self.write_valid_orders(valid_output)
        self.write_invalid_orders(invalid_output)


if __name__ == '__main__':
    processor = OrderProcessor('data/orders.txt')
    processor.process('out/order_country.txt', 'out/non_valid_orders.txt')
    print("Готово: order_country.txt и non_valid_orders.txt")