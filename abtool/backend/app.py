"""
ABtool — веб-сервис для планирования и анализа A/B тестов.
Часть 1: начальная реализация расчётных функций.
"""

import math


def calculate_sample_size(baseline_cr, mde, alpha=0.05, power=0.80):
    """
    Рассчитывает необходимый размер выборки для A/B теста.

    Аргументы:
        baseline_cr (float): базовая конверсия контрольной группы, например 0.10
        mde (float): минимальный ожидаемый эффект (абсолютный), например 0.02
        alpha (float): уровень значимости, по умолчанию 0.05
        power (float): статистическая мощность, по умолчанию 0.80

    Возвращает:
        int: необходимое количество пользователей на каждую группу
    """
    # z-значения для заданных alpha и power
    z_alpha = 1.96   # соответствует alpha=0.05, двусторонний тест
    z_beta = 0.84    # соответствует power=0.80

    p1 = baseline_cr
    p2 = baseline_cr + mde

    # Стандартная формула для двух пропорций
    numerator = (z_alpha * math.sqrt(2 * (p1 + p2) / 2 * (1 - (p1 + p2) / 2)) +
                 z_beta  * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    return math.ceil(numerator / denominator)


def calculate_conversion_rate(conversions, visitors):
    """
    Рассчитывает конверсию группы.

    Аргументы:
        conversions (int): количество конверсий
        visitors (int): общее количество посетителей

    Возвращает:
        float: конверсия от 0 до 1

    Исключения:
        ValueError: если visitors <= 0
    """
    if visitors <= 0:
        raise ValueError("Количество посетителей должно быть больше нуля")
    return conversions / visitors


def calculate_uplift(cr_control, cr_variant):
    """
    Рассчитывает относительный прирост конверсии (uplift).

    Аргументы:
        cr_control (float): конверсия контрольной группы
        cr_variant (float): конверсия варианта

    Возвращает:
        float: uplift в процентах, например 12.5 означает +12.5%
    """
    if cr_control == 0:
        return 0.0
    return (cr_variant - cr_control) / cr_control * 100


# ── Пример использования ──────────────────────────────────────────
if __name__ == "__main__":
    # Пример 1: сколько нужно пользователей?
    n = calculate_sample_size(baseline_cr=0.10, mde=0.02)
    print(f"Необходимый размер выборки: {n} человек на группу ({n * 2} всего)")

    # Пример 2: считаем конверсии обеих групп
    cr_a = calculate_conversion_rate(conversions=500, visitors=5000)
    cr_b = calculate_conversion_rate(conversions=560, visitors=5000)
    print(f"CR группы A: {cr_a:.2%}")
    print(f"CR группы B: {cr_b:.2%}")

    # Пример 3: прирост
    uplift = calculate_uplift(cr_a, cr_b)
    print(f"Uplift: {uplift:+.1f}%")
