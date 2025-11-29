import pytest
from praktikum.burger import Burger
from test_data.burger_data import move_ingredient_params

class TestBurger:
    """Тесты для класса Burger"""

    def test_init_creates_burger_with_none_bun(self):
        """Инициализация создает бургер с bun=None"""
        burger = Burger()
        assert burger.bun == None

    def test_init_creates_burger_with_empty_ingredients(self):
        """Инициализация создает бургер с пустым списком ингредиентов"""
        burger = Burger()
        assert len(burger.ingredients) == 0

    def test_set_buns_sets_bun_correctly(self, mock_bun):
        """Установка булочки сохраняет объект"""
        burger = Burger()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_adds_to_list(self, parametrized_ingredient):
        """Ингредиент добавляется в список бургера"""
        burger = Burger()
        burger.add_ingredient(parametrized_ingredient)
        assert burger.ingredients[0] == parametrized_ingredient

    def test_remove_ingredient_by_valid_index_removes_item(self, parametrized_ingredient):
        """Удаление по индексу удаляет конкретный ингредиент из списка"""
        burger = Burger()
        burger.add_ingredient(parametrized_ingredient)

        assert parametrized_ingredient in burger.ingredients

        burger.remove_ingredient(0)

        assert parametrized_ingredient not in burger.ingredients
        assert len(burger.ingredients) == 0

    @pytest.mark.parametrize("index,new_index", move_ingredient_params)
    def test_move_ingredient_changes_position(self, three_different_ingredients, index, new_index):
        """Ингредиент перемещается с index на new_index"""
        burger = Burger()
        for ing in three_different_ingredients:
            burger.add_ingredient(ing)

        ingredient_to_move = burger.ingredients[index]
        burger.move_ingredient(index, new_index)
        assert burger.ingredients[new_index] == ingredient_to_move

    def test_get_price_returns_zero_without_bun(self, parametrized_ingredient):
        """Цена без булочки = сумма ингредиентов"""
        burger = Burger()
        burger.add_ingredient(parametrized_ingredient)
        result = burger.get_price()
        assert result == parametrized_ingredient.get_price()

    def test_get_price_calculates_correctly(self, mock_bun, parametrized_ingredient):
        """Цена = булочка*2 + ингредиенты"""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(parametrized_ingredient)
        expected = mock_bun.get_price() * 2 + parametrized_ingredient.get_price()
        assert burger.get_price() == expected


    def test_get_receipt_without_ingredients(self, mock_bun):
        """Чек без ингредиентов: 2 булочки + цена"""
        burger = Burger()
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        bun_name = mock_bun.get_name()
        assert f'(==== {bun_name} ====' in receipt
        assert receipt.count(f'(==== {bun_name} ====)') == 2
        assert "Price:" in receipt


    def test_get_receipt_with_ingredients(self, mock_bun, parametrized_ingredient):
        """Чек с ингредиентами: булочки + ингредиент + цена"""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(parametrized_ingredient)
        receipt = burger.get_receipt()

        assert mock_bun.get_name() in receipt
        assert parametrized_ingredient.get_name() in receipt
        assert "Price:" in receipt
