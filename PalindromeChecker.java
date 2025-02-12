public class PalindromeChecker {
    public static boolean isPalindrome(String a){
        if (a == null) {
            return false;
        }
        int left = 0;
        int right = a.length() - 1;
        while (left < right) {
            if (a.charAt(left) != a.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}