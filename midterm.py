import pack.modu as lib


def main():                                                                         #主程式
    # 檢查資料庫存不存在，若不存在則建立資料庫及資料表
    lib.check_database_existence()

    # 讀取使用者檔案，並將資料插入到資料庫的 users 表格中
    lib.read_users_file()

    # 讀取圖書檔案，並將資料插入到資料庫的 books 表格中
    lib.read_books_file()

    # 使用者登入
    user_authenticated = False
    while not user_authenticated:
        username = input('請輸入帳號：')
        password = input('請輸入密碼：')
        user_authenticated = lib.login(username, password)

    # 顯示主選單
    while True:
        print('-------------------')
        print('    資料表 CRUD')
        print('-------------------')
        print('    1. 增加記錄')
        print('    2. 刪除記錄')
        print('    3. 修改記錄')
        print('    4. 查詢記錄')
        print('    5. 資料清單')
        print('-------------------')
        choice = input('選擇要執行的功能(Enter離開)：')

        if choice == '':
            break
        elif choice == '1':
            lib.add_record()
        elif choice == '2':
            lib.delete_record()
        elif choice == '3':
            lib.modify_record()
        elif choice == '4':
            lib.query_record()
        elif choice == '5':
            lib.list_records()
        else:
            print('=>無效的選擇')

if __name__ == "__main__":
    main()





