import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time

# --- 1. Імітація Бази Даних (На рівні Pandas та Session State) ---
# Використовуємо st.session_state для збереження даних розкладу, щоб вони могли бути змінені.
@st.cache_data
def load_mock_data():
    # Моделювання даних для факультету МФКН
    data = {
        'ПІБ': [
            'Іванов О.О.', 'Петренко І.В.', 'Сидорова К.М.', 
            'Ковальчук В.С.', 'Мороз А.П.', 'Дмитрук Г.Р.'
        ],
        'Група': ['КН-301', 'Ф-201', 'КН-301', 'М-101', 'Ф-201', 'КН-301'],
        'Курс': [3, 2, 3, 1, 2, 3],
        'Оцінка_Алгоритми': [92, 78, 85, 95, np.nan, 88],
        'Оцінка_Фізика': [80, 95, 75, np.nan, 90, 82],
        'Статус': ['Активний', 'Активний', 'Відрахований', 'Активний', 'Активний', 'Активний'],
    }
    df = pd.DataFrame(data)
    
    teachers = {
        'ПІБ': ['Проф. Сміт', 'Доц. Джонс', 'Проф. Петров'],
        'Дисципліна': ['Алгоритми', 'Фізика', 'Матанализ'],
        'Роль': ['teacher', 'teacher', 'teacher']
    }
    df_teachers = pd.DataFrame(teachers)

    # Імітація розкладу
    schedule = {
        'Група': ['КН-301', 'КН-301', 'Ф-201', 'М-101'],
        'Дисципліна': ['Алгоритми', 'Матанализ', 'Фізика', 'Лінійна алгебра'],
        'Викладач': ['Проф. Сміт', 'Проф. Петров', 'Доц. Джонс', 'Проф. Петров'],
        'День': ['Понеділок', 'Вівторок', 'Середа', 'Четвер'],
        'Час': ['9:00', '11:00', '13:00', '15:00']
    }
    df_schedule_initial = pd.DataFrame(schedule)
    
    return df, df_teachers, df_schedule_initial

df_students, df_teachers, df_schedule_initial = load_mock_data()

# Ініціалізація або оновлення df_schedule у session_state
if 'df_schedule' not in st.session_state:
    st.session_state['df_schedule'] = df_schedule_initial.copy()

df_schedule = st.session_state['df_schedule'] # Використовуємо змінну з сесії для читання
    
DF_GRADES = df_students.melt(
    id_vars=['ПІБ', 'Група', 'Курс'], 
    value_vars=['Оцінка_Алгоритми', 'Оцінка_Фізика'],
    var_name='Дисципліна', 
    value_name='Оцінка'
).dropna()
DF_GRADES['Дисципліна'] = DF_GRADES['Дисципліна'].str.replace('Оцінка_', '')

# --- 2. Імітація Авторизації та Ролей (п. 1) ---
ROLES = {
    'admin@fmfkn.edu': 'admin',
    'petrov@fmfkn.edu': 'teacher',
    'ivanov@fmfkn.edu': 'student',
    'sidorova@fmfkn.edu': 'student',
    'dean@fmfkn.edu': 'dean'
}

def login_form():
    st.sidebar.title("🔑 Авторизація")
    email = st.sidebar.text_input("Університетський Email", value="dean@fmfkn.edu")
    password = st.sidebar.text_input("Пароль (будь-який)", type="password", value="123")
    
    if st.sidebar.button("Увійти"):
        if email in ROLES:
            st.session_state['logged_in'] = True
            st.session_state['role'] = ROLES[email]
            st.session_state['user_id'] = email
            st.session_state['user_name'] = email.split('@')[0].capitalize()
            st.rerun()
        else:
            st.sidebar.error("Невірний email або користувач не знайдений.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_form()
    st.title("Ласкаво просимо до SIS ФМФКН")
    st.info("Будь ласка, увійдіть через бічну панель.")
    st.stop()
    
# --- Логіка Виходу ---
def logout():
    st.session_state['logged_in'] = False
    st.rerun()

st.sidebar.button("Вийти", on_click=logout)
role = st.session_state['role']
user_name = st.session_state['user_name']

# --- Головний Заголовок ---
st.title(f"⚛️ SIS ФМФКН | Роль: {role.capitalize()}")
st.markdown(f"Ласкаво просимо, **{user_name}**!")
st.sidebar.markdown(f"**Ваша роль:** {role.capitalize()}")
st.sidebar.markdown("---")

# --- 3. Головна Панель (Dashboard) (п. 2) ---
def render_dashboard():
    st.header("Головна панель")
    
    if role in ['admin', 'dean']:
        st.subheader("📊 Статистика факультету")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Студентів", df_students.shape[0])
        col2.metric("Груп", df_students['Група'].nunique())
        col3.metric("Викладачів", df_teachers.shape[0])
        col4.metric("Дисциплін", DF_GRADES['Дисципліна'].nunique())

        st.subheader("📢 Оголошення")
        st.info("Нагадування: термін подачі звітів викладачів спливає 15 грудня.")
        
    elif role == 'teacher':
        st.subheader("📚 Мої групи та успішність")
        teacher_disc = df_teachers[df_teachers['ПІБ'] == user_name.replace('Ivanov', 'Проф. Сміт')]['Дисципліна'].iloc[0] # Імітація
        
        st.markdown(f"**Ваша дисципліна:** **{teacher_disc}**")
        st.write("Студенти, які вивчають цю дисципліну:")
        
        # Імітація електронного журналу (п. 8)
        journal = DF_GRADES[DF_GRADES['Дисципліна'] == teacher_disc]
        st.dataframe(journal.sort_values(by='Оцінка', ascending=False))
        
        st.subheader("🗓️ Розклад на тиждень")
        st.dataframe(df_schedule[df_schedule['Викладач'] == user_name.replace('Ivanov', 'Проф. Сміт')])

    elif role == 'student':
        st.subheader("🎓 Моя успішність")
        student_grades = DF_GRADES[DF_GRADES['ПІБ'].str.contains(user_name)]
        avg_grade = student_grades['Оцінка'].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Середній бал", f"{avg_grade:.2f}" if not pd.isna(avg_grade) else "N/A")
        col2.metric("Поточний курс", student_grades['Курс'].iloc[0] if not student_grades.empty else 'N/A')
        
        st.dataframe(student_grades.sort_values(by='Оцінка', ascending=False), use_container_width=True)

        st.subheader("🗓️ Розклад занять")
        student_group = df_students[df_students['ПІБ'].str.contains(user_name)]['Група'].iloc[0]
        st.dataframe(df_schedule[df_schedule['Група'] == student_group], use_container_width=True)


# --- 4. Загальні Модулі ---
def render_students_module(): # (п. 3)
    st.header("Модуль 'Студенти'")
    if role in ['admin', 'dean', 'teacher']:
        st.dataframe(df_students, use_container_width=True)
        st.subheader("📊 Аналітика успішності (п. 12)")
        
        # Візуалізація середнього балу по курсах
        avg_by_course = df_students.groupby('Курс')['Оцінка_Алгоритми'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='Курс', y='Оцінка_Алгоритми', data=avg_by_course, ax=ax)
        ax.set_title("Середній бал (Алгоритми) по курсах")
        st.pyplot(fig)
    else:
        st.error("У вас немає прав доступу до цього модуля.")

def render_schedule_module(): # (п. 7)
    st.header("Модуль 'Розклад'")
    st.subheader("Перегляд розкладу")
    
    # Використовуємо df_schedule із session_state
    current_schedule = st.session_state['df_schedule'] 
    
    view_type = st.selectbox("Переглянути розклад для:", ['Групи', 'Викладача', 'Увесь розклад'])
    
    if view_type == 'Групи':
        selected_group = st.selectbox("Оберіть групу:", current_schedule['Група'].unique())
        st.dataframe(current_schedule[current_schedule['Група'] == selected_group], use_container_width=True)
    elif view_type == 'Викладача':
        selected_teacher = st.selectbox("Оберіть викладача:", current_schedule['Викладач'].unique())
        st.dataframe(current_schedule[current_schedule['Викладач'] == selected_teacher], use_container_width=True)
    else:
        st.dataframe(current_schedule, use_container_width=True)

    if role in ['admin', 'dean']:
        if st.button("Перейти до редагування розкладу"):
            st.session_state['page'] = "Редагування розкладу"
            st.rerun()

# --- Новий Модуль Редагування Розкладу (Імітація Backend) ---
def render_schedule_edit_module():
    st.header("🛠️ Редагування Розкладу")
    
    if role not in ['admin', 'dean']:
        st.error("У вас немає прав для редагування розкладу.")
        return
        
    st.subheader("Додати нову пару")
    
    with st.form("add_schedule_item"):
        col_g, col_d = st.columns(2)
        group = col_g.selectbox("Група", df_students['Група'].unique())
        discipline = col_d.selectbox("Дисципліна", DF_GRADES['Дисципліна'].unique())
        
        col_t, col_a = st.columns(2)
        teacher = col_t.selectbox("Викладач", df_teachers['ПІБ'].unique())
        classroom = col_a.text_input("Аудиторія", value="404")
        
        col_day, col_time = st.columns(2)
        day = col_day.selectbox("День тижня", ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця'])
        time_str = col_time.text_input("Час початку (наприклад, 10:40)", value="10:40")

        submitted = st.form_submit_button("Додати пару")
        
        if submitted:
            # Імітація перевірки конфлікту (Дуже спрощена!)
            conflict_group = st.session_state['df_schedule'][(st.session_state['df_schedule']['Група'] == group) & (st.session_state['df_schedule']['День'] == day) & (st.session_state['df_schedule']['Час'] == time_str)]
            conflict_teacher = st.session_state['df_schedule'][(st.session_state['df_schedule']['Викладач'] == teacher) & (st.session_state['df_schedule']['День'] == day) & (st.session_state['df_schedule']['Час'] == time_str)]
            
            if not conflict_group.empty or not conflict_teacher.empty:
                st.warning("⚠️ Конфлікт розкладу! Група або викладач вже зайняті в цей час.")
            else:
                new_row = pd.DataFrame([{
                    'Група': group, 
                    'Дисципліна': discipline, 
                    'Викладач': teacher, 
                    'День': day, 
                    'Час': time_str
                }])
                
                # Оновлення global df_schedule через session_state
                st.session_state['df_schedule'] = pd.concat([st.session_state['df_schedule'], new_row], ignore_index=True)
                st.success("✅ Нову пару успішно додано до розкладу!")

    st.subheader("Поточний розклад")
    st.dataframe(st.session_state['df_schedule'], use_container_width=True)

# --- 5. Навігація в Бічній Панелі ---
PAGES = {
    "Головна панель": render_dashboard,
    "Студенти та Групи": render_students_module,
    "Розклад занять": render_schedule_module,
    "Редагування розкладу": render_schedule_edit_module, # Новий модуль
    "Документообіг (Імітація)": lambda: st.header("Документообіг"),
}

# Використовуємо session_state для керування активною сторінкою
if 'page' not in st.session_state:
    st.session_state['page'] = "Головна панель"

# Створюємо навігацію, яка оновлює st.session_state['page']
selected_page = st.sidebar.radio("Навігація", list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state['page']))

# Оновлюємо активну сторінку для відображення
if selected_page != st.session_state['page']:
    st.session_state['page'] = selected_page
    
# Рендеринг обраної сторінки
PAGES[st.session_state['page']]()
