import sqlite3
import json
import csv


def login(username, password):
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 查詢使用者是否存在而且密碼要正確
        c.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            print('使用者驗證成功')
            return True
        else:
            return False

    except Exception as e:
        print('使用者驗證時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')
        return False




def check_database_existence():
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 檢查是否存在 users 資料表
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

        # 檢查是否存在 books 資料表
        c.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL)''')

        conn.commit()
        conn.close()

    except Exception as e:
        print('資料庫建立錯誤...')
        print(f'錯誤訊息：{str(e)}')

def read_users_file():                                                              #讀取user資料
    try:
        with open('users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = [(row['username'], row['password']) for row in reader]

        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 插入使用者資料到 users 資料表
        c.executemany('''INSERT INTO users (username, password) VALUES (?, ?)''', users)                    #SQL語法     INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)

        conn.commit()
        conn.close()

    except FileNotFoundError:
        print('找不到使用者檔...')
    except Exception as e:
        print('讀取使用者檔發生錯誤...')
        print(f'錯誤訊息：{str(e)}')

def read_books_file():
    try:
        with open('books.json', 'r', encoding='utf-8') as file:
            books = json.load(file)

        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 插入書籍資料到 books 資料表
        for book in books:
            c.execute('''INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)''',(book['title'], book['author'], book['publisher'], book['year']))

        conn.commit()
        conn.close()

    except FileNotFoundError:
        print('找不到圖書檔...')
    except Exception as e:
        print('讀取圖書檔發生錯誤...')
        print(f'錯誤訊息：{str(e)}')


def add_record():                                                                   #主程式選單1   增加紀錄
    try:
        # user輸入書籍資訊
        title = input('請輸入要新增的標題：')
        author = input('請輸入要新增的作者：')
        publisher = input('請輸入要新增的出版社：')
        year = int(input('請輸入要新增的年份：'))

        # 連接圖書資料庫
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 插入新的書籍紀錄到資料庫中
        c.execute('''INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)''',(title, author, publisher, year))

        conn.commit()
        conn.close()

        print('異動 1 記錄')

    except Exception as e:
        print('添加記錄時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')



def delete_record():                                                                 #主程式選單2   刪除紀錄
    try:
        # user輸入要刪除書籍的標題
        title_to_delete = input('請問要刪除哪一本書？：')

        # 連接資料庫
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 執行 SQL 查詢，刪除指定標題的記錄
        c.execute('''DELETE FROM books WHERE title=?''', (title_to_delete,))

        # 確認有沒有刪除記錄
        if c.rowcount == 0:
            print('=>給定的條件不足，無法進行刪除作業')
        else:
            print('異動 1 記錄')

        conn.commit()
        conn.close()

    except Exception as e:
        print('刪除記錄時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')


def modify_record():                                                                    #主程式選單3   修改紀錄
    try:
        # user輸入要修改的標題
        title_to_modify = input('請問要修改哪一本書的標題？：')

        # 連接資料庫
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 檢查書籍存不存在
        c.execute('''SELECT * FROM books WHERE title=?''', (title_to_modify,))
        book = c.fetchone()

        if not book:
            print('=> 無法找到指定的書籍')
        else:
            # user輸入新的書籍資訊
            new_title = input('請輸入要更改的標題：')
            author = input('請輸入要更改的作者：')
            publisher = input('請輸入要更改的出版社：')
            year = int(input('請輸入要更改的年份：'))

            # 更新資料庫中的記錄
            c.execute('''UPDATE books SET title=?, author=?, publisher=?, year=? WHERE title=?''',
                      (new_title, author, publisher, year, title_to_modify))

            print('異動 1 記錄')

        conn.commit()
        conn.close()

    except Exception as e:
        print('修改記錄時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')

def query_record():                                                                        #主程式選單4   查詢紀錄
    try:
        # user輸入要查詢書籍的關鍵字
        keyword = input('請輸入想查詢的關鍵字：')

        # 連接資料庫
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 執行 SQL 查詢，獲取符合條件的記錄
        c.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ?''',(f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))              #逐一查詢每個欄位是否有輸入的關鍵字
        records = c.fetchall()    #擷取查詢結果

        # 關閉資料庫連接
        conn.close()

        # 顯示記錄表格
        if not records:
            print('找不到符合條件的記錄')
        else:
            print('|  title  |   author   |  publisher  |   year  |')
            for record in records:
                print(f'|{record[1]:<10}|{record[2]:<12}|{record[3]:<13}|{record[4]:<8}|')

    except Exception as e:
        print('查詢記錄時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')


def list_records():                                                                          #主程式選單5  顯示紀錄
    try:
        # 連接資料庫
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # 執行 SQL 查詢，按照 title, author, publisher, year 分組
        c.execute('''SELECT * FROM books GROUP BY title, author, publisher, year''')
        records = c.fetchall()

        # 關閉資料庫連接
        conn.close()

        # 顯示記錄表格
        print('|  title  |   author   |  publisher  |   year  |')
        for record in records:
            print(f'|{record[1]:<10}|{record[2]:<12}|{record[3]:<13}|{record[4]:<8}|')

    except Exception as e:
        print('列出記錄時發生錯誤...')
        print(f'錯誤訊息：{str(e)}')



