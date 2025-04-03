import operator
import sqlalchemy as sa

class QueryUtils:

    @staticmethod
    def parse_filters(model, filters: dict):
        operators = {
            "gt": operator.gt,
            "lt": operator.lt,
            "eq": operator.eq,
            "ne": operator.ne,
            "ge": operator.ge,
            "le": operator.le,
            "in": lambda field, value: field.in_(value),
            "cn": lambda field, value: field.ilike(f"%{value}%"),
        }

        m_filters = []

        for key, value in filters.items():
            field, sep, op = key.partition("__")
            field = getattr(model, field, None)
            if field is None:
                continue
            op = operators.get(op) or operator.eq
            m_filters.append(op(field, value))

        return m_filters

    @staticmethod
    def parse_sort(model, order: list[str]):

        m_order = []
        operators = {
            "asc": sa.asc,
            "desc": sa.desc,
        }

        for order_item in order:
            field, sep, op = order_item.partition("__")
            field = getattr(model, field, None)
            if field is None:
                continue
            op = operators.get(op) or sa.asc
            m_order.append(op(field))

        return m_order
