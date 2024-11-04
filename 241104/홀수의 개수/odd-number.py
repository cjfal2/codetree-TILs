def main(n):
    answer_min = float("inf")
    answer_max = 0

    answer_min, answer_max = back(n, count_odds(n), answer_min, answer_max)

    return f"{answer_min} {answer_max}"


def count_odds(number_str):
    return sum(1 for digit in number_str if int(digit) % 2 != 0)


def back(number_str, current_odd_count, answer_min, answer_max):
    # 한 자리
    if len(number_str) == 1:
        answer_min = min(answer_min, current_odd_count)
        answer_max = max(answer_max, current_odd_count)
        return answer_min, answer_max
    
    # 세 자리 이상
    for i in range(1, len(number_str)):
        for j in range(i+1, len(number_str)):
            left = number_str[:i]
            middle = number_str[i:j]
            right = number_str[j:]
            
            new_number = str(int(left) + int(middle) + int(right))
            
            answer_min, answer_max = back(new_number, current_odd_count + count_odds(new_number), answer_min, answer_max)

    # 두 자리
    if len(number_str) == 2:
        new_number = str(int(number_str[0]) + int(number_str[1]))
        answer_min, answer_max = back(new_number, current_odd_count + count_odds(new_number), answer_min, answer_max)

    return answer_min, answer_max


if __name__ == "__main__":
    input_number = input().strip()
    print(main(input_number))