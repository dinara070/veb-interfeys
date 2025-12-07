import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time

# --- 1. Імітація Бази Даних (На рівні Pandas) ---
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
    df_schedule = pd.DataFrame(schedule)
    
    return df, df_teachers, df_schedule

df_students, df_teachers, df_schedule = load_mock_data()
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
    
    view_type = st.selectbox("Переглянути розклад для:", ['Групи', 'Викладача', 'Увесь розклад'])
    
    if view_type == 'Групи':
        selected_group = st.selectbox("Оберіть групу:", df_schedule['Група'].unique())
        st.dataframe(df_schedule[df_schedule['Група'] == selected_group], use_container_width=True)
    elif view_type == 'Викладача':
        selected_teacher = st.selectbox("Оберіть викладача:", df_schedule['Викладач'].unique())
        st.dataframe(df_schedule[df_schedule['Викладач'] == selected_teacher], use_container_width=True)
    else:
        st.dataframe(df_schedule, use_container_width=True)

    if role in ['admin', 'dean']:
        st.subheader("🛠️ Редагування розкладу")
        st.info("В режимі демонстрації цей функціонал імітується. У реальній системі потрібен Backend.")
        # Тут може бути форма для додавання нових пар

# --- 5. Навігація в Бічній Панелі ---
PAGES = {
    "Головна панель": render_dashboard,
    "Студенти та Групи": render_students_module,
    "Розклад занять": render_schedule_module,
    "Документообіг (Імітація)": lambda: st.header("Документообіг"),
}

selection = st.sidebar.radio("Навігація", list(PAGES.keys()))
PAGES[selection]()
