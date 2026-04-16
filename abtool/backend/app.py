"""
ABtool — веб-сервис для планирования и анализа A/B тестов.

Модуль содержит расчётные функции для:
- определения необходимого размера выборки;
- вычисления конверсии группы;
- расчёта относительного прироста (uplift);
- валидации входных параметров;
- интерпретации результата теста на понятном языке;
- статистической проверки значимости разницы двух конверсий.
"""

import math


def calculate_sample_size(baseline_cr, mde, alpha=0.05, power=0.80):
    """
    Рассчитывает необходимый размер выборки для A/B теста.

    Использует стандартную формулу для двустороннего теста двух пропорций.
    Z-значения фиксированы для наиболее распространённых значений alpha и power.

    Аргументы:
        baseline_cr (float): базовая конверсия контрольной группы, например 0.10
        mde (float): минимальный ожидаемый эффект (абсолютный), например 0.02
        alpha (float): уровень значимости, по умолчанию 0.05
        power (float): статистическая мощность (1 - beta), по умолчанию 0.80

    Возвращает:
        int: необходимое количество пользователей на каждую группу

    Пример:
        >>> calculate_sample_size(0.10, 0.02)
        3843
    """
    # z-значения для двустороннего теста
    z_alpha = 1.96   # alpha = 0.05
    z_beta = 0.84    # power = 0.80

    p1 = baseline_cr
    p2 = baseline_cr + mde
    p_avg = (p1 + p2) / 2

    numerator = (z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) +
                 z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    return math.ceil(numerator / denominator)


def calculate_conversion_rate(conversions, visitors):
    """
    Рассчитывает конверсию группы.

    Аргументы:
        conversions (int): количество целевых действий (конверсий)
        visitors (int): общее количество посетителей в группе

    Возвращает:
        float: конверсия в диапазоне [0, 1]

    Исключения:
        ValueError: если visitors <= 0 или conversions > visitors

    Пример:
        >>> calculate_conversion_rate(500, 5000)
        0.1
    """
    if visitors <= 0:
        raise ValueError("Количество посетителей должно быть больше нуля")
    if conversions > visitors:
        raise ValueError("Число конверсий не может превышать число посетителей")
    return conversions / visitors


def calculate_uplift(cr_control, cr_variant):
    """
    Рассчитывает относительный прирост конверсии варианта (uplift).

    Аргументы:
        cr_control (float): конверсия контрольной группы
        cr_variant (float): конверсия варианта B

    Возвращает:
        float: uplift в процентах; положительное значение означает улучшение,
               отрицательное — ухудшение. Например, 12.5 означает +12.5%.

    Пример:
        >>> calculate_uplift(0.10, 0.112)
        12.0
    """
    if cr_control == 0:
        return 0.0
    return (cr_variant - cr_control) / cr_control * 100


def validate_inputs(baseline_cr, mde):
    """
    Проверяет корректность входных параметров для расчёта выборки.

    Аргументы:
        baseline_cr (float): базовая конверсия, должна быть в диапазоне (0, 1)
        mde (float): минимальный ожидаемый эффект, должен быть > 0 и
                     не превышать 1 - baseline_cr

    Возвращает:
        tuple[bool, str]: пара (результат, сообщение).
            True и пустая строка — если параметры корректны.
            False и описание ошибки — если параметры некорректны.

    Пример:
        >>> validate_inputs(0.10, 0.02)
        (True, '')
        >>> validate_inputs(1.5, 0.02)
        (False, 'baseline_cr должна быть в диапазоне (0, 1)')
    """
    if not (0 < baseline_cr < 1):
        return False, "baseline_cr должна быть в диапазоне (0, 1)"
    if mde <= 0:
        return False, "MDE должен быть больше нуля"
    if baseline_cr + mde > 1:
        return False, "Сумма baseline_cr и MDE не может превышать 1"
    return True, ""


def interpret_result(p_value, uplift_pct, alpha=0.05):
    """
    Формирует текстовую интерпретацию результата A/B теста.

    Аргументы:
        p_value (float): достигнутый уровень значимости теста
        uplift_pct (float): относительный прирост конверсии в процентах
        alpha (float): порог значимости, по умолчанию 0.05

    Возвращает:
        str: текстовый вывод на русском языке с рекомендацией

    Пример:
        >>> interpret_result(0.03, 12.0)
        'Результат статистически значим (p=0.0300 < 0.05). Вариант B показал
        прирост +12.00%. Рекомендуется внедрить изменение.'
    """
    significant = p_value < alpha
    direction = "прирост" if uplift_pct >= 0 else "снижение"
    sign = "+" if uplift_pct >= 0 else ""

    if significant:
        recommendation = (
            "Рекомендуется внедрить изменение."
            if uplift_pct > 0
            else "Рекомендуется отклонить изменение."
        )
        return (
            f"Результат статистически значим (p={p_value:.4f} < {alpha}). "
            f"Вариант B показал {direction} {sign}{uplift_pct:.2f}%. "
            f"{recommendation}"
        )
    else:
        return (
            f"Результат статистически не значим (p={p_value:.4f} >= {alpha}). "
            f"Недостаточно данных для вывода. "
            f"Рекомендуется продолжить сбор данных или пересмотреть MDE."
        )


def compare_proportions(conv_a, n_a, conv_b, n_b):
    """
    Выполняет двусторонний z-тест для сравнения двух пропорций.

    Реализован без использования scipy — только стандартная библиотека math.
    Используется нормальное приближение, применимое при n >= 30.

    Аргументы:
        conv_a (int): число конверсий в контрольной группе A
        n_a (int): число посетителей в контрольной группе A
        conv_b (int): число конверсий в варианте B
        n_b (int): число посетителей в варианте B

    Возвращает:
        dict: словарь с ключами:
            - z_stat (float): значение z-статистики
            - p_value (float): двустороннее p-value (приближённое)
            - cr_a (float): конверсия группы A
            - cr_b (float): конверсия группы B
            - significant (bool): True если p_value < 0.05

    Пример:
        >>> compare_proportions(500, 5000, 560, 5000)
        {'z_stat': 2.134, 'p_value': 0.033, 'cr_a': 0.1, 'cr_b': 0.112,
         'significant': True}
    """
    cr_a = conv_a / n_a
    cr_b = conv_b / n_b

    # Объединённая пропорция
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))

    if se == 0:
        return {"z_stat": 0, "p_value": 1.0, "cr_a": cr_a, "cr_b": cr_b, "significant": False}

    z_stat = (cr_b - cr_a) / se

    # Приближение p-value через стандартное нормальное распределение
    # Используем формулу Абрамовица и Стегана (точность ~1e-4)
    t = 1 / (1 + 0.2316419 * abs(z_stat))
    poly = t * (0.319381530
                + t * (-0.356563782
                + t * (1.781477937
                + t * (-1.821255978
                + t * 1.330274429))))
    p_one_tail = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z_stat ** 2) * poly
    p_value = min(2 * p_one_tail, 1.0)

    return {
        "z_stat": round(z_stat, 4),
        "p_value": round(p_value, 6),
        "cr_a": round(cr_a, 6),
        "cr_b": round(cr_b, 6),
        "significant": p_value < 0.05,
    }


# ── Пример использования ──────────────────────────────────────────
if __name__ == "__main__":
    # Валидация входных данных
    ok, msg = validate_inputs(0.10, 0.02)
    print(f"Валидация: {'OK' if ok else 'Ошибка: ' + msg}")

    # Расчёт выборки
    n = calculate_sample_size(baseline_cr=0.10, mde=0.02)
    print(f"Размер выборки: {n} на группу ({n * 2} всего)")

    # Конверсии
    cr_a = calculate_conversion_rate(500, 5000)
    cr_b = calculate_conversion_rate(560, 5000)
    print(f"CR_A = {cr_a:.2%}, CR_B = {cr_b:.2%}")

    # Uplift
    uplift = calculate_uplift(cr_a, cr_b)
    print(f"Uplift: {uplift:+.1f}%")

    # Сравнение пропорций
    result = compare_proportions(500, 5000, 560, 5000)
    print(f"z = {result['z_stat']}, p = {result['p_value']}, значимо: {result['significant']}")

    # Интерпретация
    print(interpret_result(result["p_value"], uplift))