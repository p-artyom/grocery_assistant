from django.conf import settings

from recipes import models


def cut_string(
    field: str,
    cut_out: int = settings.STR_LENGTH_WHEN_PRINTING_MODEL,
) -> str:
    """Обрезает строку, если оно больше заданной длины.

    Args:
        field: Текст строки.
        cut_out: Длина строки.

    Returns:
        Текст строки с добавлением многоточия, если оно больше заданной длины.
    """
    return field[:cut_out] + '…' if len(field) > cut_out else field


def check_favorites(user, object):
    if user.is_anonymous:
        return False
    return models.Favorite.objects.filter(
        user=user,
        recipe=object.id,
    ).exists()


def check_is_in_shopping_cart(user, object):
    if user.is_anonymous:
        return False
    return models.ShoppingCart.objects.filter(
        user=user,
        recipe=object.id,
    ).exists()
