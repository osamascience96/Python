def health_calculator(age, apple_ate, cigs_smoked):
    answer = (100-age) + apple_ate - cigs_smoked
    print(answer)


osama_data = [22, 2, 4]

health_calculator(*osama_data)
