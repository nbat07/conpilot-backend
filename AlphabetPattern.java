public class AlphabetPattern {
    // Keep the answer in a format such as _A_\n_A_B_\n_A_B_C_\n
    public static String printAlphabetPattern(int n) {
        StringBuilder result = new StringBuilder();
        String a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        int i = 0;
        String j = "_";

        while (i < n && n <= 26) {result.append(j);
            j = j + a.charAt(i) + "_";
            result.append(a.substring(0, i + 1).replace("", "_").substring(1)).append("\n");
            i++;
        }
        return result.toString();
    }
}