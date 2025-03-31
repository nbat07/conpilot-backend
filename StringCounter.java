public class StringCounter {
    public static int countValidAlphabetStrings(String input) {//only alphabet letters in string
        String[] b = input.split(",");
        int k = b.length;
        int m = 0;
       int x = 0;for (int i = 0; i < k; i++) {
            if (b[i].matches("[a-zA-Z]+")) {
                x++;
            }
        }
        return x;
    }
}