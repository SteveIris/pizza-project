import click
import random


class Recipe:
    def __init__(self, name: str, ingredients: list, size='L'):
        """Инициализирует объект класса"""
        self.ingredients = ingredients
        self.name = name
        self.size = size

    def __eq__(self, other):
        """Сравнивает два рецепта"""
        return self.name == other.name and self.ingredients == other.ingredients

    def __hash__(self):
        return hash(self.name)

    def dict(self):
        """Выводит рецепт в консоль"""
        print('-'+self.name+': '+', '.join(self.ingredients))


pizza_menu = {Recipe('Pepperoni', ['pepperoni', 'sweet peppers', 'mozarella']),
              Recipe('Margherita', ['tomato sauce', 'mozarella', 'tomatoes']),
              Recipe('Hawaiian', ['cheese', 'chicken', 'pineapple'])}


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    """Готовит и доставляет пиццу"""
    order_recipe = Recipe('', [])
    recipe_found = False
    for pizza_recipe in pizza_menu:
        if pizza.lower() == pizza_recipe.name.lower():
            order_recipe = pizza_recipe
            recipe_found = True
    if recipe_found:
        bake(order_recipe)
        if delivery:
            deliver(order_recipe)
        else:
            pickup(order_recipe)
    else:
        print('Такой пиццы в меню нет :(')
    return


@cli.command()
def menu():
    """Выводит меню"""
    for pizza in pizza_menu:
        pizza.dict()


def log(time_spent: str) -> callable:
    """Фиксирует время работы функций"""
    def outer_wrapper(func: callable) -> callable:
        def inner_wrapper(pizza: Recipe):
            func(pizza)
            print(time_spent.format(random.randint(1, 10)))

        return inner_wrapper

    return outer_wrapper


@log('Приготовили за {}c!')
def bake(pizza: Recipe):
    """Готовит пиццу"""
    pass


@log('Доставили за {}с!')
def deliver(pizza: Recipe):
    """Доставляет пиццу"""
    pass


@log('Забрали за {}c!')
def pickup(pizza: Recipe):
    """Самовывоз"""
    pass


if __name__ == "__main__":
    cli.add_command(menu)
    cli.add_command(order)
    cli()
