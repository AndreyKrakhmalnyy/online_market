def my_decorator(func):
  def wrapper(*args, **kwargs):
    print(f"Вызов функции {func.__name__}")
    result = func(*args, **kwargs)
    print(f"Функция {func.__name__} завершена")
    return result
  return wrapper

@my_decorator
def say_hello(name):
  print(f"Привет, {name}!")

say_hello("Мир")
