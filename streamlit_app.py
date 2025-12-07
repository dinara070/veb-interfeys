import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, time

# --- 1. ІНІЦІАЛІЗАЦІЯ СКЛАДНИХ ДАНИХ (ІМІТАЦІЯ БАЗИ ДАНИХ) ---

# Використовуємо реальні ПІБ для ключових ролей
USERS_INFO = {
    'panasenko@fmfkn.edu': {'name': 'ПАНАСЕНКО ОЛЕКСІЙ БОРИСОВИЧ', 'role': 'admin', 'password': 'admin'},
    'voevoda@fmfkn.edu': {'name': 'ВОЄВОДА АЛІНА ЛЕОНІДІВНА', 'role': 'dean', 'password': 'dean'},
    'konoshevskyi@fmfkn.edu': {'name': 'КОНОШЕВСЬКИЙ ОЛЕГ ЛЕОНІДОВИЧ', 'role': 'dean', 'password': 'dean'}, 
    'kovtonyukm@fmfkn.edu': {'name': "КОВТОНЮК МАР'ЯНА МИХАЙЛІВНА", 'role': 'teacher', 'password': 'teacher'}, 
    'teacher@fmfkn.edu': {'name': 'МАТЯШ ОЛЬГА ІВАНІВНА', 'role': 'teacher', 'password': 'teacher'},
    'student@fmfkn.edu': {'name': 'ІВАНОВ О.О.', 'role': 'student', 'password': 'student'},
}
ROLES = {email: info['role'] for email, info in USERS_INFO.items()}


# --- 2. Ініціалізація Груп, Викладачів та Розкладу (Mock Data) ---
@st.cache_data(show_spinner="Завантаження структури факультету...")
def setup_fmfkn_structure():
    
    # --- A. Реальні Викладачі та Кафедри ---
    TEACHER_DATA = []
    
    # Кафедра Алгебри і методики навчання математики (10 осіб)
    KAFEDRA_AMNM = "Алгебри і методики навчання математики"
    TEACHER_DATA.extend([
        {'ПІБ': 'КОНОШЕВСЬКИЙ ОЛЕГ ЛЕОНІДОВИЧ', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'dean', 'Посада': 'Завідувач кафедри, доцент'},
        {'ПІБ': 'МАТЯШ ОЛЬГА ІВАНІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Професор'},
        {'ПІБ': 'МИХАЙЛЕНКО ЛЮБОВ ФЕДОРІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Професор'},
        {'ПІБ': 'ВОЄВОДА АЛІНА ЛЕОНІДІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'dean', 'Посада': 'Декан, доцент'},
        {'ПІБ': 'ВОТЯКОВА ЛЕСЯ АНДРІЇВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'КАЛАШНІКОВ ІГОР В’ЯЧЕСЛАВОВИЧ', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'НАКОНЕЧНА ЛЮДМИЛА ЙОСИПІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'ПАНАСЕНКО ОЛЕКСІЙ БОРИСОВИЧ', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'admin', 'Посада': 'Заступник декана, доцент'}, 
        {'ПІБ': 'ТЮТЮННИК ДІАНА ОЛЕГІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Асистент'},
        {'ПІБ': 'КОМАРОВА КАРИНА ВАДИМІВНА', 'Кафедра': KAFEDRA_AMNM, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
    ])

    # Кафедра Математики та інформатики (12 осіб)
    KAFEDRA_MI = "Математики та інформатики"
    TEACHER_DATA.extend([
        {'ПІБ': "КОВТОНЮК МАР'ЯНА МИХАЙЛІВНА", 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Завідувач кафедри, професор'},
        {'ПІБ': 'БАК СЕРГІЙ МИКОЛАЙОВИЧ', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Професор, заступник декана з наукової роботи'},
        {'ПІБ': 'КЛОЧКО ОКСАНА ВІТАЛІЇВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Професор'},
        {'ПІБ': 'ГРАНЯК ВАЛЕРІЙ ФЕДОРОВИЧ', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'КОВТОНЮК ГАЛИНА МИКОЛАЇВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'КОСОВЕЦЬ ОЛЕНА ПАВЛІВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'КРУПСЬКИЙ ЯРОСЛАВ ВОЛОДИМИРОВИЧ', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'СОЯ ОЛЕНА МИКОЛАЇВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'ТЮТЮН ЛЮБОВ АНДРІЇВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'ЛЕОНОВА ІВАННА МИКОЛАЇВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Асистент'},
        {'ПІБ': 'ПОЛІЩУК ВІТАЛІЙ ОЛЕГОВИЧ', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Завідувач обчислювальними лабораторіями'},
        {'ПІБ': 'ЯРОШ ОКСАНА ІВАНІВНА', 'Кафедра': KAFEDRA_MI, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
    ])

    # Кафедра Фізики і методики навчання фізики та астрономії (10 осіб)
    KAFEDRA_FMFA = "Фізики і методики навчання фізики, астрономії"
    TEACHER_DATA.extend([
        {'ПІБ': 'СІЛЬВЕЙСТР АНАТОЛІЙ МИКОЛАЙОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Завідувач кафедри, професор'},
        {'ПІБ': 'ЗАБОЛОТНИЙ ВОЛОДИМИР ФЕДОРОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Професор'},
        {'ПІБ': 'БІЛЮК АНАТОЛІЙ ІВАНОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'ДУМЕНКО ВІКТОРІЯ ПЕТРІВНА', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'МОКЛЮК МИКОЛА ОЛЕКСІЙОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Доцент'},
        {'ПІБ': 'КСЕНДЗОВА ОКСАНА СЕРГІЇВНА', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
        {'ПІБ': 'МАМІЧЕВА ІННА ОЛЕКСІЇВНА', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
        {'ПІБ': 'МОРОЗ ЯРОСЛАВ ОЛЕКСІЙОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
        {'ПІБ': 'СІВАЄВА НАТАЛІЯ ВІТАЛІЇВНА', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
        {'ПІБ': 'ЖУРЖА АРТЕМ АРСЕНОВИЧ', 'Кафедра': KAFEDRA_FMFA, 'Роль': 'teacher', 'Посада': 'Старший лаборант'},
    ])

    df_teachers = pd.DataFrame(TEACHER_DATA)
    
    # --- B. Групи (24 групи) ---
    BACHELOR_GROUPS = [f'{i}{group}' for i in range(1, 5) for group in ['М', 'СОМ', 'СОІ', 'СОФА']]
    MASTER_GROUPS = [f'{i}М{group}' for i in range(1, 3) for group in ['М', 'СОМ', 'СОІ', 'СОФА']]
    ALL_GROUPS = BACHELOR_GROUPS + MASTER_GROUPS
    
    # --- C. Студенти (Імітація 10 студентів на групу) ---
    STUDENTS = []
    # Додаємо одного "чистого" студента для тестування реєстрації
    STUDENTS.append({
        'ПІБ': 'ІВАНОВ О.О.', 
        'Група': '1СОІ', 
        'Курс': 1,
        'Статус': 'Активний',
        'Оцінка_Алгоритми': 85,
        'Оцінка_Фізика': 70,
    })
    
    for group in ALL_GROUPS:
        try:
            course = int(group[0])
        except ValueError:
            course = 1 
            
        for i in range(1, 10): 
            STUDENTS.append({
                'ПІБ': f'Студент {group}-{i}', 
                'Група': group, 
                'Курс': course,
                'Статус': 'Активний',
                'Оцінка_Алгоритми': random.randint(70, 100) if 'СОІ' in group or 'КН' in group else np.nan,
                'Оцінка_Фізика': random.randint(70, 100) if 'СОФА' in group else np.nan,
            })
    df_students = pd.DataFrame(STUDENTS)
    
    # --- D. Розклад (Спрощена генерація) ---
    DAYS = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця']
    TIMES = ['9:00', '10:40', '12:40', '14:20']
    DISCIPLINES = ['Алгебра', 'Матаналіз', 'Програмування', 'Фізика', 'Методика']
    schedule_data = []
    
    for group in ALL_GROUPS:
        used_time_slots = set()
        for _ in range(3): # 3 пари на тиждень
            day = random.choice(DAYS)
            time_slot = random.choice(TIMES)
            teacher = random.choice(df_teachers['ПІБ'].tolist())
            discipline = random.choice(DISCIPLINES)
            
            if (day, time_slot) not in used_time_slots:
                used_time_slots.add((day, time_slot))
                schedule_data.append({
                    'Група': group,
                    'Дисципліна': discipline,
                    'Викладач': teacher,
                    'День': day,
                    'Час': time_slot,
                    'Аудиторія': f'Ауд-{random.randint(100, 500)}'
                })
    df_schedule = pd.DataFrame(schedule_data)
    
    # --- E. Обчислення DF_GRADES для повернення ---
    DF_GRADES_CALCULATED = df_students.melt(
        id_vars=['ПІБ', 'Група', 'Курс'], 
        value_vars=[col for col in df_students.columns if col.startswith('Оцінка_')],
        var_name='Дисципліна', 
        value_name='Оцінка'
    ).dropna()
    DF_GRADES_CALCULATED['Дисципліна'] = DF_GRADES_CALCULATED['Дисципліна'].str.replace('Оцінка_', '')
    
    # ПОВЕРТАЄМО ВСІ СТРУКТУРИ
    return df_students, df_teachers, df_schedule, DF_GRADES_CALCULATED 


# Ініціалізація даних у st.session_state, якщо вони ще не завантажені
if 'df_students' not in st.session_state or 'df_teachers' not in st.session_state or 'df_schedule' not in st.session_state or 'DF_GRADES' not in st.session_state or 'DOCS' not in st.session_state:
    # Отримуємо всі чотири об'єкти
    df_students_initial, df_teachers_initial, df_schedule_initial, DF_GRADES_initial = setup_fmfkn_structure()
    st.session_state['df_students'] = df_students_initial
    st.session_state['df_teachers'] = df_teachers_initial
    st.session_state['df_schedule'] = df_schedule_initial
    st.session_state['DF_GRADES'] = DF_GRADES_initial
    st.session_state['USERS_INFO'] = USERS_INFO
    # Імітація документації
    st.session_state['DOCS'] = "Тут міститься текст наказу №123 про відрахування Іванова."
    
# Отримання даних з session_state
df_students = st.session_state['df_students']
df_teachers = st.session_state['df_teachers']
df_schedule = st.session_state['df_schedule']
USERS_INFO = st.session_state['USERS_INFO']
DF_GRADES = st.session_state['DF_GRADES'] 

# --- 3. АВТЕНТИФІКАЦІЯ ТА РЕЄСТРАЦІЯ (п. 1) ---

def login_form():
    st.sidebar.title("🔑 Вхід до SIS")
    email = st.sidebar.text_input("Університетський Email", key="login_email")
    password = st.sidebar.text_input("Пароль", type="password", key="login_password")
    
    if st.sidebar.button("Увійти", key="login_btn"):
        if email in USERS_INFO and USERS_INFO[email]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['role'] = USERS_INFO[email]['role']
            st.session_state['user_name'] = USERS_INFO[email]['name']
            st.rerun()
        else:
            st.sidebar.error("Невірний email або пароль.")

def registration_form():
    st.sidebar.header("📝 Реєстрація (Імітація)")
    with st.sidebar.form("registration_form"):
        new_email = st.text_input("Новий Email (університетський)", key="reg_email")
        new_password = st.text_input("Пароль", type="password", key="reg_password")
        full_name = st.text_input("ПІБ (Наприклад: Студент Прізвище)", key="reg_name")
        
        new_role = st.selectbox("Роль", ['student', 'teacher', 'admin', 'dean'], key="reg_role_key")
        
        # --- ДИНАМІЧНА ГРАФА "ГРУПА" ---
        new_group = None
        if new_role == 'student':
             new_group = st.selectbox("Група (Обов'язково для студента)", df_students['Група'].unique())
        # -------------------------------
        
        submitted = st.form_submit_button("Зареєструватися")
        
        if submitted:
            if new_role in ['admin', 'dean']:
                st.warning(f"⚠️ Увага: Реєстрація нового {new_role.capitalize()} дозволена лише для імітації тестування.")
                
            if new_email in USERS_INFO:
                st.sidebar.error("Користувач з таким Email вже існує.")
            elif not full_name or not new_password:
                st.sidebar.error("Заповніть усі поля.")
            elif new_role == 'student' and not new_group:
                st.sidebar.error("Оберіть групу для студента.")
            else:
                # 1. Додаємо нового користувача
                USERS_INFO[new_email] = {'name': full_name, 'role': new_role, 'password': new_password}
                
                # 2. Якщо це студент, додаємо його до mock-бази df_students
                if new_role == 'student' and new_group:
                    new_student_row = pd.DataFrame([{
                        'ПІБ': full_name, 
                        'Група': new_group, 
                        'Курс': int(new_group[0]) if new_group[0].isdigit() else 1,
                        'Статус': 'Активний',
                        'Оцінка_Алгоритми': np.nan, 
                        'Оцінка_Фізика': np.nan,
                    }])
                    # Оновлюємо DF_STUDENTS
                    st.session_state['df_students'] = pd.concat([st.session_state['df_students'], new_student_row], ignore_index=True)
                    
                    # Оновлюємо DF_GRADES (щоб функція calculate_gpa бачила нового студента)
                    new_grades = st.session_state['df_students'].melt(
                        id_vars=['ПІБ', 'Група', 'Курс'], 
                        value_vars=[col for col in st.session_state['df_students'].columns if col.startswith('Оцінка_')],
                        var_name='Дисципліна', 
                        value_name='Оцінка'
                    ).dropna()
                    new_grades['Дисципліна'] = new_grades['Дисципліна'].str.replace('Оцінка_', '')
                    st.session_state['DF_GRADES'] = new_grades


                st.session_state['USERS_INFO'] = USERS_INFO
                st.session_state['logged_in'] = True
                st.session_state['role'] = new_role
                st.session_state['user_name'] = full_name
                st.sidebar.success("Реєстрація успішна! Ви увійшли.")
                st.rerun()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_form()
    registration_form()
    st.title("Ласкаво просимо до SIS ФМФКН")
    st.info("Будь ласка, увійдіть або зареєструйтеся через бічну панель. Для адміна/декана використовуйте email panasenko@fmfkn.edu або voevoda@fmfkn.edu (пароль: admin/dean).")
    st.stop()
    
# --- Логіка Виходу ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['page'] = "Головна панель"
    st.rerun()

# --- ВІДНОВЛЕНА ФУНКЦІЯ ---
def calculate_gpa(student_name):
    """Імітація розрахунку середнього балу"""
    grades = DF_GRADES[DF_GRADES['ПІБ'] == student_name]['Оцінка']
    return grades.mean() if not grades.empty else np.nan

# --- 4. Рендеринг Компонентів ---

role = st.session_state['role']
user_name = st.session_state['user_name']

st.sidebar.button("Вийти", on_click=logout)
st.sidebar.markdown(f"**Ваша роль:** {role.capitalize()}")
st.sidebar.markdown("---")

# --- 4.1. Головна Панель (Dashboard) (п. 2, 12) ---
def render_dashboard():
    st.header("Головна панель")
    
    if role in ['admin', 'dean']:
        st.subheader("📊 Статистика факультету (Адміністратор/Деканат)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Студентів (активних)", df_students[df_students['Статус'] == 'Активний'].shape[0])
        col2.metric("Груп (загалом)", df_students['Група'].nunique())
        col3.metric("Викладачів", df_teachers.shape[0])
        col4.metric("Кафедр", df_teachers['Кафедра'].nunique())

        st.markdown("---")
        st.subheader("Повідомлення та оголошення (п. 2, 10)")
        st.info(f"**Для Деканату:** Звітність викладачів за I семестр має бути подана до {datetime(2025, 12, 15).strftime('%d.%m.%Y')}.")
        st.warning("Увага! В аудиторії 404 15.12.2025 буде проведено комплексний екзамен.")
        
    elif role == 'teacher':
        st.subheader("📚 Мої групи та успішність (п. 2, 5, 8)")
        teacher_groups = df_schedule[df_schedule['Викладач'] == user_name]['Група'].unique()
        
        st.markdown(f"**Мої групи:** {', '.join(teacher_groups) if teacher_groups.size > 0 else 'Не призначено'}")
        
        st.subheader("Електронний журнал (Імітація)")
        st.caption("Оцінки можна редагувати безпосередньо в таблиці (зміни тимчасові).")
        # Імітація електронного журналу (п. 8)
        editable_grades = st.data_editor(
            DF_GRADES.sort_values(by=['Група', 'ПІБ']), 
            use_container_width=True, 
            key="teacher_grades_edit"
        )
        
    elif role == 'student':
        student_info_df = df_students[df_students['ПІБ'] == user_name]
        
        if student_info_df.empty:
            st.error("Помилка: Ваші дані не знайдені в базі студентів. Зверніться до адміністратора.")
            return

        student_info = student_info_df.iloc[0]
        student_group = student_info['Група']
        
        st.subheader("🎓 Моя успішність (п. 2, 8)")
        avg_grade = calculate_gpa(user_name)
        
        col1, col2 = st.columns(2)
        col1.metric("Середній бал (іміт.)", f"{avg_grade:.2f}" if not pd.isna(avg_grade) else "N/A")
        col2.metric("Моя група", student_group)
        
        st.markdown("**Поточні оцінки:**")
        st.dataframe(DF_GRADES[DF_GRADES['ПІБ'] == user_name], use_container_width=True)

# --- 4.2. Модуль "Студенти" (п. 3, 11) ---
def render_students_module():
    st.header("Модуль 'Студенти'")
    if role not in ['admin', 'dean']:
        st.error("У вас немає прав доступу до цього модуля.")
        return
        
    st.subheader("База даних студентів")
    
    # Фільтри (п. 11)
    col1, col2 = st.columns(2)
    selected_course = col1.selectbox("Фільтр за курсом", ['Всі'] + df_students['Курс'].unique().tolist())
    selected_status = col2.selectbox("Фільтр за статусом", ['Всі'] + df_students['Статус'].unique().tolist())

    filtered_df = df_students.copy()
    if selected_course != 'Всі':
        filtered_df = filtered_df[filtered_df['Курс'] == selected_course]
    if selected_status != 'Всі':
        filtered_df = filtered_df[filtered_df['Статус'] == selected_status]

    st.dataframe(filtered_df, use_container_width=True)

# --- 4.3. Модуль "Розклад" (п. 7) ---
def render_schedule_module():
    st.header("Модуль 'Розклад'")
    
    current_schedule = st.session_state['df_schedule'] 
    
    st.subheader("Перегляд розкладу")
    
    view_type = st.selectbox("Переглянути розклад для:", ['Групи', 'Викладача', 'Увесь розклад'])
    
    if view_type == 'Групи':
        selected_group = st.selectbox("Оберіть групу:", current_schedule['Група'].unique())
        st.dataframe(current_schedule[current_schedule['Група'] == selected_group].sort_values(by='Час'), use_container_width=True)
    elif view_type == 'Викладача':
        selected_teacher = st.selectbox("Оберіть викладача:", current_schedule['Викладач'].unique())
        st.dataframe(current_schedule[current_schedule['Викладач'] == selected_teacher].sort_values(by='Час'), use_container_width=True)
    else:
        st.dataframe(current_schedule.sort_values(by=['Група', 'День', 'Час']), use_container_width=True)

    if role in ['admin', 'dean']:
        st.subheader("🛠️ Редагування розкладу")
        with st.expander("Додати нову пару"):
            render_schedule_edit_form() 

# --- 4.4. Форма Редагування Розкладу (Імітація Backend/CRUD) ---
def render_schedule_edit_form():
    
    with st.form("add_schedule_item_full"):
        st.markdown("**Новий запис:**")
        
        col_g, col_d = st.columns(2)
        group = col_g.selectbox("Група", st.session_state['df_students']['Група'].unique())
        discipline = col_d.selectbox("Дисципліна", st.session_state['df_schedule']['Дисципліна'].unique())
        
        col_t, col_a = st.columns(2)
        teacher = col_t.selectbox("Викладач", df_teachers['ПІБ'].unique())
        classroom = col_a.text_input("Аудиторія", value=f"Ауд-{random.randint(100, 500)}")
        
        col_day, col_time = st.columns(2)
        DAYS_OF_WEEK = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця']
        day = col_day.selectbox("День тижня", DAYS_OF_WEEK)
        time_str = col_time.text_input("Час початку (наприклад, 10:40)", value="10:40")

        submitted = st.form_submit_button("Додати пару")
        
        if submitted:
            current_schedule_df = st.session_state['df_schedule']
            
            # Перевірка конфлікту (п. 7)
            conflict_group = current_schedule_df[(current_schedule_df['Група'] == group) & (current_schedule_df['День'] == day) & (current_schedule_df['Час'] == time_str)]
            conflict_teacher = current_schedule_df[(current_schedule_df['Викладач'] == teacher) & (current_schedule_df['День'] == day) & (current_schedule_df['Час'] == time_str)]
            
            if not conflict_group.empty or not conflict_teacher.empty:
                st.warning("⚠️ Конфлікт розкладу! Група або викладач вже зайняті в цей час.")
            else:
                new_row = pd.DataFrame([{
                    'Група': group, 
                    'Дисципліна': discipline, 
                    'Викладач': teacher, 
                    'День': day, 
                    'Час': time_str,
                    'Аудиторія': classroom
                }])
                
                st.session_state['df_schedule'] = pd.concat([current_schedule_df, new_row], ignore_index=True)
                st.success("✅ Нову пару успішно додано до розкладу!")
                st.toast("Розклад оновлено!")

# --- 4.5. Модуль "Керування даними (Адмін)" (п. 3, 5, 9) ---
def render_admin_data_management():
    st.header("Адмін-Керування даними (Студенти, Викладачі, Документи)")
    
    if role not in ['admin', 'dean']:
        st.error("🚫 У вас немає прав адміністратора для редагування цієї секції.")
        return
        
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Студенти (редагування)", "Викладачі (редагування)", "Документація"])

    # --- 1. Редагування Студентів (п. 3) ---
    with tab1:
        st.subheader("Редагування Бази Студентів")
        st.warning("Редагування відбувається безпосередньо в таблиці. Зміни зберігаються лише на час поточної сесії.")
        
        # Використовуємо st.data_editor для можливості редагування Pandas DataFrame
        edited_students_df = st.data_editor(st.session_state['df_students'], use_container_width=True, key="admin_edit_students")
        
        if st.button("Зберегти зміни у студентах (тимчасово)"):
            st.session_state['df_students'] = edited_students_df
            st.success("База студентів оновлена!")

    # --- 2. Редагування Викладачів (п. 5) ---
    with tab2:
        st.subheader("Редагування Списку Викладачів")
        st.warning("Ви можете змінювати ПІБ, Кафедру та Посаду викладачів.")

        # Редагування DataFrame Викладачів
        edited_teachers_df = st.data_editor(st.session_state['df_teachers'], use_container_width=True, key="admin_edit_teachers")

        if st.button("Зберегти зміни у викладачах (тимчасово)"):
            st.session_state['df_teachers'] = edited_teachers_df
            st.success("База викладачів оновлена!")
            
    # --- 3. Редагування Документації (п. 9) ---
    with tab3:
        st.subheader("Редагування Основної Документації")
        st.info("Імітація: Редагування тексту важливого документа (наприклад, Наказу)")

        edited_doc_text = st.text_area(
            "Текст документа:", 
            st.session_state['DOCS'], 
            height=300, 
            key="admin_edit_docs"
        )

        if st.button("Зберегти зміни у документації (тимчасово)"):
            st.session_state['DOCS'] = edited_doc_text
            st.success("Документація оновлена!")
            
# --- 4.6. Модуль "Документообіг" (для перегляду) ---
def render_doc_module():
    st.header("Модуль 'Документообіг' (Перегляд)")
    st.markdown("---")
    st.subheader("Накази та Довідки")
    
    st.markdown("**Приклад поточного документа:**")
    st.text(st.session_state['DOCS'])
    
    if role == 'student':
        st.markdown("---")
        st.subheader("Сервіс для Студента")
        st.button("Отримати довідку про навчання (PDF)")
        st.caption("Імітація генерації PDF.")
        
# --- 5. Навігація в Бічній Панелі ---

PAGES = {
    "Головна панель": render_dashboard,
    "Керування даними (Адмін)": render_admin_data_management, 
    "Студенти та Групи": render_students_module,
    "Викладачі та Кафедри": render_teachers_module,
    "Розклад занять (Редагування)": render_schedule_module,
    "Документообіг (Перегляд)": render_doc_module,
}

if 'page' not in st.session_state:
    st.session_state['page'] = "Головна панель"

# Видаляємо адміністративні сторінки з навігації, якщо користувач не є адміністратором/деканом
visible_pages = list(PAGES.keys())
if role not in ['admin', 'dean']:
    # Ховаємо "Керування даними (Адмін)"
    if "Керування даними (Адмін)" in visible_pages:
        visible_pages.remove("Керування даними (Адмін)")
    # Ховаємо "Студенти та Групи" (бо доступ обмежено всередині)
    if "Студенти та Групи" in visible_pages:
        visible_pages.remove("Студенти та Групи")
    # Ховаємо "Розклад занять (Редагування)" (якщо роль не дозволяє, краще не відображати)
    if "Розклад занять (Редагування)" in visible_pages:
        visible_pages.remove("Розклад занять (Редагування)")
    # Для викладачів і студентів показуємо тільки релевантне
    
    
selection = st.sidebar.radio("Навігація", visible_pages, index=visible_pages.index(st.session_state['page']) if st.session_state['page'] in visible_pages else 0)


if selection != st.session_state['page']:
    st.session_state['page'] = selection
    st.rerun() 
    
# Рендеринг обраної сторінки
PAGES[st.session_state['page']]()
