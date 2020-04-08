def Palindrome(s):
    if len(s) < 1:
        return True
    else:
        if s[0] == s[-1]:
            return Palindrome(s[1:-1])
        else:
            return False


string = "aaabaaa"
print(Palindrome(string))