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

    @pytest.mark.parametrize(
        "method, args, should_raise, needs_preparation",  # Параметры для тест-кейсов
        BurgerTestData.NONE_PARAMETERS_CASES  # Данные из тестового набора
    )
    def test_none_handling(
        self, 
        burger_fixture,            # Бургер (пустой)
        burger_with_ingredient,    # Бургер (с ингредиентом)
        method,                    # Тестируемый метод
        args,                      # Аргументы
        should_raise,              # Флаг: ожидается исключение? (True/False)
        needs_preparation          # Флаг: требуется бургер с ингредиентом? (True/False)
    ):
        """
        Проверка обработки None-параметров в методах бургера.
        Тестирует два сценария:
        1. Методы, которые должны принимать None (set_buns, add_ingredient)
        2. Методы, которые должны вызывать исключение (remove_ingredient, move_ingredient)
        """
        
        # Выбираем наиболее подходящую фикстуру бургера в зависимости от тест-кейса
        burger = burger_with_ingredient if needs_preparation else burger_fixture
        
        if should_raise:
            # Методы должны вызывать исключение при None-параметрах
            with pytest.raises((TypeError, IndexError)):  
                getattr(burger, method)(*args) 
        else:
            # Методы должны принимать None без ошибок
            getattr(burger, method)(*args)
            
            # Проверка состояния после вызова
            if method == "set_buns":
                # Булочка должна быть None
                assert burger.bun is None, "Булочка должна быть None после set_buns(None)"
                
            elif method == "add_ingredient":
                # Последний ингредиент должен быть None
                assert burger.ingredients[-1] is None, "Последний ингредиент должен быть None"
