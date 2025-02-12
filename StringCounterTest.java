import org.junit.Test;
import static org.junit.Assert.*;

public class StringCounterTest {

    @Test
    public void testCountValidStrings() {
        assertCountValidStrings("abc,xyz,aba,1221,1", 3);
        assertCountValidStrings("abc, xyz , alpha", 1);
        assertCountValidStrings("www,google,.com.", 2);
        assertCountValidStrings("i am ,alba, a ,bbb", 2);
        assertCountValidStrings("aba", 1);
        assertCountValidStrings(",,,,,", 0);
        assertCountValidStrings("abc,def", 2);
    }

    private void assertCountValidStrings(String input, int expectedOutput) {
        assertEquals(expectedOutput, StringCounter.countValidAlphabetStrings(input));
    }
}