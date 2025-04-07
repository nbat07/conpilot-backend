public class NumberReverser {
    public static int[] reverseAndSum(int number) {
        int n = number;
        String rev;
        if (n > 10) {
            rev = new StringBuilder(String.valueOf(number)).reverse().toString();
        } else {
            rev = String.valueOf(number);
        }
        int r = Integer.parseInt(rev);int sum = number + r;
        return new int[]{r, sum};
    }
}