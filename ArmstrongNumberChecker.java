public class ArmstrongNumberChecker {
    public static boolean isArmstrongNumber(int num) {
        int sum = 0;
        int temp = num;

        // The power needs to be 3, not the number of digits
        while (temp > 0) {
            int digit = temp % 10;sum += Math.pow(digit, 3);
            temp /= 10;
        }
        return sum == num;
    }

    public static void main(String[] args) {
        int number = 153;
        if (isArmstrongNumber(number)) {
            System.out.println(number + " is an Armstrong number.");
        } else {
            System.out.println(number + " is not an Armstrong number.");
        }
    }
}