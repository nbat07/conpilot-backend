import org.junit.Test;
import static org.junit.Assert.*;

public class PalindromeCheckerTest {

    @Test
    public void testPalindromeChecker() {
        assertPalindrome("Nitin", true);
        assertPalindrome("Uma", false);
        assertPalindrome("AmeyemA", true);
        assertPalindrome("Tintin", false);
        assertPalindrome("ye ey", true);
        assertPalindrome("Amrev Verma", true);
        assertPalindrome("Amy Yummy", false);
    }

    private void assertPalindrome(String input, boolean expectedOutput) {
        assertEquals(expectedOutput, PalindromeChecker.isPalindrome(input));
    }
}