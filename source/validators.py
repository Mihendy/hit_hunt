from datetime import datetime


def str_datetime_validator(lined_dt) -> bool:
    """Проверка даты, написанной строкой слитно в
    формате ДД-ММ-ГГГГ:чч:мм:cc (exp: 16-05-2022:01:50:30)"""
    if lined_dt is None:
        return True
    try:
        datetime.strptime(lined_dt, '%d-%m-%Y:%H:%M:%S')
    except (ValueError, TypeError):
        try:
            datetime.strptime(lined_dt, '%d-%m-%Y')
        except (ValueError, TypeError):
            return False
    return True


def limit_validator(limit) -> bool:
    """Проверка лимита - числа, которое показывает, сколько
    строк таблицы удовлетворяющих другим условиям нужно вывести.(1 <= limit <= 100)"""
    return limit in range(1, 101)


def utc_validator(utc) -> bool:
    """Проверка валидности UTC"""
    return utc in map(lambda x: x / 10, range(-120, 121, 5))
