import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, time

# --- 1. ІНІЦІАЛІЗАЦІЯ СКЛАДНИХ ДАНИХ (ІМІТАЦІЯ БАЗИ ДАНИХ) ---

# --- Ролі та Паролі (Імітація) ---
ROLES = {
    'panasenko@fmfkn.edu': 'admin',
    'voevoda@fmfkn.edu': 'dean', # Додано декана для прикладу
    'prof.ivanov@fmfkn.edu': 'teacher',
    'student.ivanov@fmfkn.edu': 'student',
}
USERS_INFO = {
    'panasenko@fmfkn.edu': {'name': 'Панасенко Олексій Борисович', 'role': 'admin', 'password': 'admin'},
    'voevoda@fmfkn.edu': {'name': 'Воєвода Аліна Леонідівна', 'role': 'dean', 'password': 'dean'},
    'prof.ivanov@fmfkn.edu': {'name': 'Проф. Іванов', 'role': 'teacher', 'password': 'teacher'},
    'student.ivanov@fmfkn.edu': {'name': 'Іванов О.О.', 'role': 'student', 'password': 'student'},
    # Сюди будуть додаватися зареєстровані користувачі
}

# --- 2. Ініціалізація Груп, Викладачів та Розкладу (Mock Data) ---
@st.cache_data(show_spinner="Завантаження структури факультету...")
def setup_fmfkn_structure():
    # --- A. Викладачі (32 особи) ---
    KAFEDRY = {
        'Алгебри і методики навчання математики': 10,
        'Математики та інформатики': 12,
        'Фізики і методики навчання фізики, астрономії': 10,
    }
    TEACHER_NAMES = []
    
    # Створення іменованих викладачів
    TEACHER_NAMES.append('Панасенко Олексій Борисович') # Адміністратор
    TEACHER_NAMES.append('Воєвода Аліна Леонідівна') # Декан
    TEACHER_NAMES.extend([f'Викладач АМНМ_{i+1}' for i in range(KAFEDRY['Алгебри і методики навчання математики'] - 2)])
    TEACHER_NAMES.extend([f'Викладач МІ_{i+1}' for i in range(KAFEDRY['Математики та інформатики'])])
    TEACHER_NAMES.extend([f'Викладач ФМФА_{i+1}' for i in range(KAFEDRY['Фізики і методики навчання фізики, астрономії'])])
    
    # Викладачі у вигляді DataFrame
    df_teachers = pd.DataFrame({
        'ПІБ': TEACHER_NAMES,
        'Кафедра': 
            ['Алгебри і методики навчання математики'] * 10 + 
            ['Математики та інформатики'] * 12 + 
            ['Фізики і методики навчання фізики, астрономії'] * 10,
        'Роль': ['admin', 'dean'] + ['teacher'] * 30
    })
    
    # --- B. Групи (24 групи) ---
    # ВИПРАВЛЕННЯ СИНТАКСИЧНОЇ ПОМИЛКИ ТУТ:
    BACHELOR_GROUPS = [f'{i}{group}' for i in range(1, 5) for group in ['М', 'СОМ', 'СОІ', 'СОФА']]
    MASTER_GROUPS = [f'{i}{group}' for i in range(1, 3) for group in ['ММ', 'МСОМ', 'МСОІ', 'МСОФА']]
    
    ALL_GROUPS = BACHELOR_GROUPS + MASTER_GROUPS
    
    # --- C. Студенти (Імітація 10 студентів на групу) ---
    STUDENTS = []
    for group in ALL_GROUPS:
        # Безпечне отримання курсу з назви групи
        try:
            course = int(group[0])
        except ValueError:
            course = 1 # Значення за замовчуванням
            
        for i in range(1, 11):
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
    
    return df_students, df_teachers, df_schedule

# Ініціалізація даних у st.session_state, якщо вони ще не завантажені
if 'df_students' not in st.session_state or 'df_teachers' not in st.session_state or 'df_schedule' not in st.session_state:
    df_students_initial, df_teachers_initial, df_schedule_initial = setup_fmfkn_structure()
    st.session_state['df_students'] = df_students_initial
    st.session_state['df_teachers'] = df_teachers_initial
    st.session_state['df_schedule'] = df_schedule_initial
    st.session_state['USERS_INFO'] = USERS_INFO
    
# Отримання даних з session_state
df_students = st.session_state['df_students']
df_teachers = st.session_state['df_teachers']
df_schedule = st.session_state['df_schedule']
USERS_INFO = st.session_state['USERS_INFO']

# --- Допоміжні дані для оцінок ---
DF_GRADES = df_students.melt(
    id_vars=['ПІБ', 'Група', 'Курс'], 
    value_vars=[col for col in df_students.columns if col.startswith('Оцінка_')],
    var_name='Дисципліна', 
    value_name='Оцінка'
).dropna()
DF_GRADES['Дисципліна'] = DF_GRADES['Дисципліна'].str.replace('Оцінка_', '')


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
        full_name = st.text_input("ПІБ", key="reg_name")
        new_role = st.selectbox("Роль", ['student', 'teacher'], key="reg_role")
        submitted = st.form_submit_button("Зареєструватися")
        
        if submitted:
            if new_email in USERS_INFO:
                st.sidebar.error("Користувач з таким Email вже існує.")
            elif not full_name or not new_password:
                st.sidebar.error("Заповніть усі поля.")
            else:
                # Зберігаємо нового користувача в імітованій базі
                USERS_INFO[new_email] = {'name': full_name, 'role': new_role, 'password': new_password}
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
    st.info("Будь ласка, увійдіть або зареєструйтеся через бічну панель.")
    st.stop()
    
# --- Логіка Виходу ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['page'] = "Головна панель"
    st.rerun()

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
        student_info = df_students[df_students['ПІБ'].str.contains(user_name.split('@')[0].capitalize())].iloc[0]
        student_group = student_info['Група']
        
        st.subheader("🎓 Моя успішність (п. 2, 8)")
        avg_grade = calculate_gpa(student_info['ПІБ'])
        
        col1, col2 = st.columns(2)
        col1.metric("Середній бал (іміт.)", f"{avg_grade:.2f}" if not pd.isna(avg_grade) else "N/A")
        col2.metric("Моя група", student_group)
        
        st.markdown("**Поточні оцінки:**")
        st.dataframe(DF_GRADES[DF_GRADES['ПІБ'] == student_info['ПІБ']], use_container_width=True)

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

# --- 4.5. Інші Модулі (Імітація) ---
def render_doc_module():
    st.header("Модуль 'Документообіг' (п. 9)")
    st.markdown("---")
    st.subheader("Накази та Довідки")
    st.info("Імітація: Накази (зарахування, відрахування) та довідки (автоматичне формування PDF) керуються тут.")
    
    if role == 'student':
        st.button("Отримати довідку про навчання (PDF)")
        st.caption("Імітація генерації PDF.")

def render_teachers_module():
    st.header("Модуль 'Викладачі' (п. 5)")
    st.markdown("---")
    st.subheader("Персональний склад та Навантаження")
    st.dataframe(df_teachers, use_container_width=True)
    st.caption(f"Всього {df_teachers.shape[0]} викладачів. Панасенко О.Б. - заступник декана/адміністратор.")

# --- 5. Навігація в Бічній Панелі ---

PAGES = {
    "Головна панель": render_dashboard,
    "Студенти та Групи (Адмін/Декан)": render_students_module,
    "Викладачі та Кафедри": render_teachers_module,
    "Розклад занять (Редагування)": render_schedule_module,
    "Документообіг (Імітація)": render_doc_module,
}

if 'page' not in st.session_state:
    st.session_state['page'] = "Головна панель"

selection = st.sidebar.radio("Навігація", list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state['page']))

if selection != st.session_state['page']:
    st.session_state['page'] = selection
    st.rerun() 
    
# Рендеринг обраної сторінки
PAGES[st.session_state['page']]()
