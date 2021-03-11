input_id = input("아이디를 입력해주세요.")

#real_egoing="11"
#real_k8805 = "ab"
members = ['egoing', 'k8805', 'leezhe']

for member in members:
    if member == input_id:
        print('Hello!, ' + member)
        import sys
        sys.exit()
print('Who are you?')

#if real_egoing==in_str:
#    print("Hello!, egoing")
#elif real_k8805 == in_str:
#     print("Hello!, k8805")
#else :
#     print("Who are you")