import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import org.junit.Test;

public class PangramCheckerTest {
    @Test
    public void testIsPangram() {
        assertFalse(PangramChecker.isPangram("The quick brown fox jump over the lazy dog"));
        assertTrue(PangramChecker.isPangram("The quick brown fox jumps over the lazy dog"));
        assertFalse(PangramChecker.isPangram("The brown fox jump over the lazy dog"));
        assertFalse(PangramChecker.isPangram("Hi, I am Amey"));
        assertFalse(PangramChecker.isPangram("Did The quick brown fox jump over the lazy dog, hmm ..., I don't know."));
        assertFalse(PangramChecker.isPangram("This problem has no automated test cases. Add automated/pre-generated test cases to this problem."));
        assertFalse(PangramChecker.isPangram(""));
        assertFalse(PangramChecker.isPangram("..."));
        assertTrue(PangramChecker.isPangram("No, the string is NOT a pangram. Missing letter(s) is(are) a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z.\ninvisible\t"));
        assertFalse(PangramChecker.isPangram("Yes, the string is a pangram."));
    }
}