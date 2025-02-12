import org.junit.Test;
import static org.junit.Assert.*;

public class ArmstrongNumberCheckerTest {

    @Test
    public void testArmstrongNumberChecker() {
        assertArmstrongNumber(371, true);
        assertArmstrongNumber(5, false);
        assertArmstrongNumber(9223372036854775807L, false); // maximum value for a long
        assertArmstrongNumber(10203020, false);
        assertArmstrongNumber(1634, false);
        assertArmstrongNumber(407, true);
        assertArmstrongNumber(0, true);
        assertArmstrongNumber(1, true);
    }

    private void assertArmstrongNumber(long input, boolean expectedOutput) {
        assertEquals(expectedOutput, ArmstrongNumberChecker.isArmstrongNumber((int) input));
    }
}