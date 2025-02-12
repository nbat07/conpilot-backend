import org.junit.Test;
import static org.junit.Assert.*;

public class AckermannFunctionTest {

    @Test
    public void testAckermannFunction() {
        assertAckermannFunction(2, 3, 9);
        assertAckermannFunction(0, 1500, 1501);
        assertAckermannFunction(1, 15, 17);
        assertAckermannFunction(2, 5, 13);
        assertAckermannFunction(2, 10, 23);
        assertAckermannFunction(3, 4, 125);
        assertAckermannFunction(1, 17, 19);
        assertAckermannFunction(2, 6, 15);
    }

    private void assertAckermannFunction(int m, int n, int expectedOutput) {
        assertEquals(expectedOutput, AckermannFunction.ackermann(m, n));
    }
}
