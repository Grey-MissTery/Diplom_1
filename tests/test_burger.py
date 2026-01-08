import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from data import BurgerTestData, IngredientTestData, ReceiptData


class TestBurger:

    def test_bun_should_be_none_by_default(self):
        """Проверка отсутствия булочки по умолчанию"""
        burger = Burger()
        assert burger.bun is None

    def test_ingredients_should_be_empty_list_by_default(self):
        """Проверка пустого списка ингредиентов по умолчанию"""
        burger = Burger()
        assert burger.ingredients == []

    def test_set_buns_updates_bun_correctly(self, mock_bun, burger_fixture):
        """Проверка корректной установки булочки"""
        name = mock_bun.name
        burger_fixture.set_buns(mock_bun)
        assert burger_fixture.bun.name == name

    def test_add_ingredient_appends_to_ingredients_list(self, mock_ingredient_filling, burger_fixture):
        """Проверка добавления одного ингредиента в список"""
        burger_fixture.add_ingredient(mock_ingredient_filling)
        assert burger_fixture.ingredients[0].name == mock_ingredient_filling.name

    def test_add_ingredient_multiple_same_correctly(self, mock_ingredient_filling, burger_fixture):
        """Проверка корректного добавления нескольких одинаковых ингредиентов в список"""
        for _ in range(5):
            burger_fixture.add_ingredient(mock_ingredient_filling)
        assert len(burger_fixture.ingredients) == 5 and \
            all(ingredient == mock_ingredient_filling for ingredient in burger_fixture.ingredients), \
            (f"Количество ингредиентов: {len(burger_fixture.ingredients)}/5, "
                f"Совпадение с mock-объектом: {all(ingredient == mock_ingredient_filling for ingredient in burger_fixture.ingredients)}") 
    
    def test_remove_ingredient_decreases_ingredients_count(self, burger_fixture):
        """Проверка удаления ингредиента по индексу"""
        ingredient = IngredientTestData.COMMON_CASES
        burger_fixture.add_ingredient(ingredient[0])
        burger_fixture.add_ingredient(ingredient[1])
        burger_fixture.remove_ingredient(0)
        assert len(burger_fixture.ingredients) == 1 and burger_fixture.ingredients[0] == ingredient[1]

    def test_move_ingredient_changes_positions_correctly(self, burger_fixture):
        """Проверка перемещения ингредиента"""
        ingredient = IngredientTestData.COMMON_CASES
        burger_fixture.add_ingredient(ingredient[0])
        burger_fixture.add_ingredient(ingredient[1])
        burger_fixture.move_ingredient(0, 1)
        assert burger_fixture.ingredients[0] == ingredient[1] and burger_fixture.ingredients[1] == ingredient[0]

    @pytest.mark.parametrize('bun_price, ingredients_prices, expected_price', BurgerTestData.BURGERS_PRICE_DATA)
    def test_get_price_with_multiple_ingredients_correctly(
        self, mock_bun, burger_fixture, bun_price, ingredients_prices, expected_price):
        """Проверка расчета цены с разным количеством ингредиентов"""
        mock_bun.get_price.return_value = bun_price
        burger_fixture.set_buns(mock_bun)
        for price in ingredients_prices:
            mock = Mock() 
            mock.get_price.return_value = price
            burger_fixture.add_ingredient(mock)
        assert burger_fixture.get_price() == expected_price

    def test_get_receipt_structure_with_only_bun(self, burger_fixture, mock_bun):
        """Проверка формата чека для бургера только с булочкой без ингредиентов"""
        burger_fixture.set_buns(mock_bun)
        assert burger_fixture.get_receipt() == ReceiptData.EXP_ONLY_BUN

    def test_get_receipt_with_ingredients_of_different_type(
            self, burger_fixture, mock_bun, mock_ingredient_filling, mock_ingredient_sauce):
        """Проверка формата чека с разными типами ингредиентов"""
        burger_fixture.set_buns(mock_bun)
        burger_fixture.add_ingredient(mock_ingredient_filling)
        burger_fixture.add_ingredient(mock_ingredient_sauce)
        assert burger_fixture.get_receipt() == ReceiptData.EXP_DIFF_INGREDS

    def test_get_receipt_with_multiple_ingredients_of_same_type(
        self, burger_fixture, mock_bun, mock_ingredient_filling, mock_ingredient_sauce):
        """Проверка формата чека с повторяющимися ингредиентами"""
        burger_fixture.set_buns(mock_bun)
        burger_fixture.add_ingredient(mock_ingredient_filling)
        burger_fixture.add_ingredient(mock_ingredient_filling)
        burger_fixture.add_ingredient(mock_ingredient_sauce)
        assert burger_fixture.get_receipt() == ReceiptData.EXP_SAME_INGREDS
        
    def test_get_receipt_with_empty_ingredient_name(self, burger_fixture, mock_bun, mock_ingredient_filling):
        """Проверка формата чека с пустыми названиями"""
        mock_ingredient_filling.get_type.return_value = ""
        mock_ingredient_filling.get_name.return_value = ""
        mock_bun.get_name.return_value = ""
        burger_fixture.set_buns(mock_bun)
        burger_fixture.add_ingredient(mock_ingredient_filling)
        assert burger_fixture.get_receipt() == ReceiptData.EXP_EMPTY_NAME

    def test_get_price_with_none_bun_raises_error(self, mock_ingredient_filling, burger_fixture):
        """Проверка, что при расчете цены без установленной булочки вызывает AttributeError"""
        burger_fixture.add_ingredient(mock_ingredient_filling)
        with pytest.raises(AttributeError):
            burger_fixture.get_price()

    def test_get_receipt_with_no_bun_raises_error(self, burger_fixture, mock_ingredient_filling):
        """Проверка, что генерация чека без булочки вызывает AttributeError"""
        burger_fixture.add_ingredient(mock_ingredient_filling)
        with pytest.raises(AttributeError):
            burger_fixture.get_receipt()

    def test_get_receipt_with_none_ingredient_raises_error(self, burger_fixture, mock_bun):
        """Проверка, что генерация чека с None-ингредиентом вызывает AttributeError"""
        burger_fixture.set_buns(mock_bun)
        burger_fixture.ingredients.append(None)  # добавляем None напрямую
        with pytest.raises(AttributeError):
            burger_fixture.get_receipt()

    def test_get_receipt_with_invalid_ingredient_type(self, burger_fixture, mock_bun):
        """Проверка, что генерация чека с невалидным типом ингредиента вызывает AttributeError"""
        class InvalidIngredient:
            pass
        invalid_ingredient = InvalidIngredient()
        burger_fixture.set_buns(mock_bun)
        burger_fixture.add_ingredient(invalid_ingredient)  # Добавляем невалидного ингредиента
        with pytest.raises(AttributeError):
            burger_fixture.get_receipt()

    def test_get_receipt_with_long_ingredient_name(self, burger_fixture, mock_bun, mock_ingredient_filling):
        """Проверка обработки длинных названий в чеке"""
        mock_bun.get_name.return_value = "б" * 100
        mock_ingredient_filling.get_type.return_value = "т" * 100
        mock_ingredient_filling.get_name.return_value = "и" * 100
        burger_fixture.set_buns(mock_bun)
        burger_fixture.add_ingredient(mock_ingredient_filling)
        receipt = burger_fixture.get_receipt()
        assert all(x in receipt for x in ("б" * 100, "т" * 100, "и" * 100))

    
    # Новые тесты для обработки None вместо одного параметризованного
    def test_set_buns_with_none_should_not_raise(self, burger_fixture):
        """Проверка, что set_buns принимает None без ошибок"""
        burger_fixture.set_buns(None)
        assert burger_fixture.bun is None

    def test_add_ingredient_with_none_should_not_raise(self, burger_fixture):
        """Проверка, что add_ingredient принимает None без ошибок"""
        burger_fixture.add_ingredient(None)
        assert burger_fixture.ingredients[-1] is None

    def test_remove_ingredient_with_none_should_raise(self, burger_fixture):
        """Проверка, что remove_ingredient вызывает TypeError при None-индексе"""
        with pytest.raises(TypeError):
            burger_fixture.remove_ingredient(None)

    def test_move_ingredient_with_none_source_should_raise(self, burger_with_ingredient):
        """Проверка, что move_ingredient вызывает TypeError при None как исходном индексе"""
        with pytest.raises(TypeError):
            burger_with_ingredient.move_ingredient(None, 0)

    def test_move_ingredient_with_none_target_should_raise(self, burger_with_ingredient):
        """Проверка, что move_ingredient вызывает TypeError при None как целевом индексе"""
        with pytest.raises(TypeError):
            burger_with_ingredient.move_ingredient(0, None)