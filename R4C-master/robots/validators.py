import re


def validate_robot_data(robot_data: dict) -> bool:
    """Функция для валидации данных при создании робота"""
    keys = ('model', 'version', 'created')
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

    for key in keys:
        if not robot_data.get(key):
            return False
    if not pattern.match(str(robot_data.get('created'))):
        return False
    return True
