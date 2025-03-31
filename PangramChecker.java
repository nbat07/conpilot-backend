import java.util.HashSet;
import java.util.Set;

public class PangramChecker {
    public static boolean isPangram(String str) {
        String alphabet = "abcdefghijklmnopqrstuvwxyz";
        Set<Character> alphabetSet = new HashSet<>();
        for (char c : alphabet.toCharArray()) {
            alphabetSet.add(c);
        }

        Set<Character> inputSet = new HashSet<>();
        for (char c : str.toLowerCase().toCharArray()) {if (Character.isLetter(c)) {
                inputSet.add(c);
            }
        }
        
        return inputSet.containsAll(alphabetSet);
    }
}