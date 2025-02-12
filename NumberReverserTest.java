import org.junit.Test;
import static org.junit.Assert.*;

public class NumberReverserTest {

    @Test
    public void testReverseAndSum() {
        assertReverseAndSum(43, 34, 77);
        assertReverseAndSum(500, 5, 505);
        assertReverseAndSum(202, 202, 404);
        assertReverseAndSum(2, 2, 4);
        assertReverseAndSum(5, 5, 10);
        assertReverseAndSum(314159, 951413, 1265572);
        assertReverseAndSum(0, 0, 0);
    }

    private void assertReverseAndSum(int input, int expectedReverse, int expectedSum) {
        int[] result = NumberReverser.reverseAndSum(input);
        assertEquals(expectedReverse, result[0]);
        assertEquals(expectedSum, result[1]);
    }
}