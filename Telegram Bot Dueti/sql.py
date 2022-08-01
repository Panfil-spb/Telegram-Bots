import sqlite3


def execute_read_quary(text: str) -> list:
    """Функция выполнения запроса на получение данных"""
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()
    cursor.execute(text)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_quary(text: str) -> sqlite3.Cursor:
    """функция выполнения запроса для изменения бд"""
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()
    cursor.execute(text)
    conn.commit()
    conn.close()


def check_user(user_name: str) -> bool:
    """функция для проверки наличия пользователя в базе"""
    text = """select Name from Users"""
    result = execute_read_quary(text)
    for users in result:
        if user_name in users:
            return True
    return False


def add_user(user_name: str, flag_qr: bool = False, flag_txt: bool = False) -> None:
    """функция добавления пользователя"""
    if not check_user(user_name):
        text = f"""
        insert into Users (Name, Flag_to_save_qr, Flag_to_update_text)
        values 
        ('{user_name}', {flag_qr}, {flag_txt})  
        """
        execute_quary(text)


def update_user(user_name: str, flag_qr: bool = False, flag_txt: bool = False) -> None:
    """функция изменения индекаторов пользователя"""
    text = f"""update Users 
    set Flag_to_save_qr={flag_qr}, Flag_to_update_text={flag_txt}
    where Name='{user_name}'
    """
    execute_quary(text)


def get_qr_flag(user_name: str) -> bool:
    """функция получения флага редактирования файла"""
    if check_user(user_name):
        text = f"""select Flag_to_save_qr from Users where Name='{user_name}'"""
        result = execute_read_quary(text)
        return result[0][0]
    else:
        return False


def get_txt_flag(user_name: str) -> bool:
    """функция получения флага редактирования файла"""
    if check_user(user_name):
        text = f"""select Flag_to_update_text from Users where Name='{user_name}'"""
        result = execute_read_quary(text)
        return result[0][0]
    else:
        return False


def get_file_path(user_name: str) -> str:
    """функция получения пути к файлу который будет редактироваться"""
    if check_user(user_name):
        text = f"""select file_path from Users where Name='{user_name}'"""
        result = execute_read_quary(text)
        return result[0][0]


def update_user_file_path(user_name: str, file_path: str) -> None:
    """функция изменения пути к файлу который будет редактироваться"""
    text = f"""update Users
    set file_path='{file_path}'
    where Name='{user_name}'"""
    execute_quary(text)
