import org.junit.Test;
import static org.junit.Assert.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class HelloWorldTest {

    @Test
    public void testMain() {
        // Set up a stream to capture the output
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        // Call the main method
        GeneratedCode.main(new String[]{});

        // Verify the output
        assertEquals("Hello, World!", outContent.toString());

        // Reset the standard output
        System.setOut(System.out);
    }
}
