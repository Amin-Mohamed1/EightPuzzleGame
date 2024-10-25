def get_buttons_data(array: list[list[int]]):
    data = 0
    for i in range(3):
        for j in range(3):
            data = data * 10 + int(array[i][j])
    return data


arr = [[0, 2, 3], [4, 5, 6], [7, 8, 1]]
print(get_buttons_data(arr))  # 123456780
