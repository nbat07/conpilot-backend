import org.junit.Test;
import static org.junit.Assert.*;

public class GeneratedCodeTest {

    @Test
    public void testReverseString() {
        GeneratedCode gc = new GeneratedCode();
        
        // Test with a regular string
        assertEquals("dcba", gc.reverseString("abcd"));
        
        // Test with an empty string
        assertEquals("", gc.reverseString(""));
        
        // Test with a null string
        assertNull(gc.reverseString(null));
        
        // Test with a palindrome
        assertEquals("madam", gc.reverseString("madam"));
    }
}