import psycopg2


class DBManager:
    '''
    Класс который будет подключаться к БД PostgreSQL.
    '''
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        '''
        Метод, который получает список всех компаний и количество вакансий у каждой компании.
        '''
        self.cursor.execute("""
                    SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_counter 
                    FROM companies c
                    LEFT JOIN vacancies v USING(company_id)
                    GROUP BY c.company_name;
                """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        '''
        Метод, который получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        '''
        self.cursor.execute("""
                    SELECT c.company_name, v.vacancy_name, v.salary_min, v.salary_max, v.vacancy_url
                    FROM companies c
                    JOIN vacancies v USING(company_id);
                """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        '''
        Метод, который получает среднюю зарплату по вакансиям.
        '''
        self.cursor.execute("""
                    SELECT ROUND(AVG((salary_min + salary_max) / 2)) AS avg_salary
                    FROM vacancies;
                """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        '''
        Метод, который получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        '''
        self.cursor.execute("""
                    SELECT * FROM vacancies
                    WHERE (salary_min + salary_max) > 
                    (SELECT AVG(salary_min + salary_max) FROM vacancies);
                """)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        '''
        Метод, который получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python.
        '''
        self.cursor.execute("""
                    SELECT * FROM vacancies 
                    WHERE vacancy_name ILIKE '%%' || %s || '%%';
                """, (keyword,))  # '%%' означает любую последовательность символов перед и после ключевого слова (%s)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
