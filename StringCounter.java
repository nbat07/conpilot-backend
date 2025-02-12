public class StringCounter {
    public static int countValidAlphabetStrings(String input) {//only alphabet letters in string
        String[] b = input.split(",");
        int k = b.length;
        int m = 0;
       int x = 0;while (m < k) {
           if (b[m].matches("^[a-zA-Z]+$")) {
               x++;
           }
           m++;
       }
       return x;
    }
}