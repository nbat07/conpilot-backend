import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Arrays;
import java.util.List;

public class MarksManagerTest {

    @Test
    public void testManageMarks() {
        assertManageMarks(4, Arrays.asList("101, CS101, 10", "101,   CS102, 20", "102, CS102  , 30", "102,CS101,-10"), "101:30;102:20");
        assertManageMarks(1, Arrays.asList("101, CS101, 10"), "101:10");
        assertManageMarks(0, Arrays.asList(), "");
        assertManageMarks(3, Arrays.asList("101, CS101, 10", "101, CS101, 20", "101, CS101, 30"), "101:60");
        assertManageMarks(2, Arrays.asList("101, CS101, 10", "102, CS101, 20"), "101:10;102:20");
    }

    private void assertManageMarks(int records, List<String> inputs, String expectedOutput) {
        assertEquals(expectedOutput, MarksManager.manageMarks(records, inputs));
    }
}