import org.junit.Test;
import static org.junit.Assert.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class NotBadConverterTest {

    @Test
    public void testConvertToUUIDString() {
        assertConversion("The lyrics is not that bad!", "The lyrics is good!\n");
        assertConversion("Food is bad? not at all.", "Food is bad? not at all.\n");
        assertConversion("The song is good.", "The song is good.\n");
        assertConversion("The song is not extremely good.", "The song is not extremely good.\n");
        assertConversion("not bad", "good\n");
        assertConversion("not very bad", "good\n");
        assertConversion("heynotatallbadatall", "heygoodatall\n");
        assertConversion("notbad", "good\n");
    }

    private void assertConversion(String input, String expectedOutput) {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        // Simulate input
        System.setIn(new java.io.ByteArrayInputStream(input.getBytes()));

        // Call the main method
        GeneratedCode.main(new String[]{});

        // Verify the output
        assertEquals(expectedOutput, outContent.toString());

        // Reset the standard output
        System.setOut(System.out);
    }
}