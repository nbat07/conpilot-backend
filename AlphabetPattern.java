public class AlphabetPattern {
    // Keep the answer in a format such as _A_\n_A_B_\n_A_B_C_\n
    public static String printAlphabetPattern(int n) {
        StringBuilder result = new StringBuilder();
        String a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        int i = 0;
        String j = "_";

        while (i < n && n <= 26) {int k = 0;
            while (k <= i) {
                result.append(j).append(a.charAt(k));
                k++;
            }
            result.append(j).append("\n");
            i++;
        }
        return result.toString();
    }
}