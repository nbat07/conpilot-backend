import org.junit.Test;
import static org.junit.Assert.*;

public class TrianglePrinterTest {

    @Test
    public void testPrintTriangle() {
        assertPrintTriangle(3, "*\n**\n***\n");
        assertPrintTriangle(4, "*\n**\n***\n****\n");
        assertPrintTriangle(10, "*\n**\n***\n****\n*****\n******\n*******\n********\n*********\n**********\n");
        assertPrintTriangle(13, "*\n**\n***\n****\n*****\n******\n*******\n********\n*********\n**********\n***********\n************\n*************\n");
        assertPrintTriangle(1, "*\n");
        assertPrintTriangle(6, "*\n**\n***\n****\n*****\n******\n");
        assertPrintTriangle(16, "*\n**\n***\n****\n*****\n******\n*******\n********\n*********\n**********\n***********\n************\n*************\n**************\n***************\n****************\n");
    }

    private void assertPrintTriangle(int input, String expectedOutput) {
        assertEquals(expectedOutput, TrianglePrinter.printTriangle(input));
    }
}
